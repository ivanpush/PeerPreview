"""Analyzes figure placement in document flow."""

import re
from typing import Dict, List, Optional
import pymupdf


class FigurePlacementAnalyzer:
    """Determines where figure appears in document flow and suggests handling."""

    # Patterns for detecting figure references in text
    REFERENCE_PATTERNS = [
        r'(?i)(figure|fig\.?)\s*\d+[a-z]?',
        r'(?i)(shown|displayed|illustrated|depicted)\s+(in|below|above)',
        r'(?i)(see|refer to)\s+(figure|fig)',
        r'(?i)as\s+(shown|seen|illustrated)',
    ]

    def __init__(self, doc: pymupdf.Document):
        self.doc = doc

    def analyze_placement(
        self,
        figure_bbox: Dict,
        page_num: int,
        markdown_text: str,
        section_headers: List[Dict],
        caption_text: str
    ) -> Dict:
        """
        Analyze figure placement and suggest handling.

        Args:
            figure_bbox: Image bounding box
            page_num: Page number (0-indexed)
            markdown_text: Full markdown text
            section_headers: List of section headers from BoldTextAnalyzer
            caption_text: Caption text for position finding

        Returns:
            Dict with placement metadata
        """
        # 1. Find position in markdown
        md_position = self._find_in_markdown(caption_text, markdown_text)

        # 2. Determine placement type
        placement_type = self._classify_placement(
            page_num,
            figure_bbox,
            section_headers
        )

        # 3. Extract surrounding context
        context = self._get_surrounding_context(markdown_text, md_position)

        # 4. Find section
        section_id = self._find_section(page_num, section_headers)

        # 5. Generate recommendation
        suggestion = self._recommend_action(
            placement_type,
            context,
            figure_bbox
        )

        return {
            "placement_type": placement_type,
            "markdown_position": md_position,
            "surrounding_context": context,
            "section_id": section_id,
            "suggested_action": suggestion["action"],
            "move_reason": suggestion.get("reason")
        }

    def _find_in_markdown(self, caption_text: str, markdown: str) -> Optional[int]:
        """Find caption position in markdown using fuzzy matching."""
        if not caption_text:
            return None

        # Try exact match first (first 50 chars of caption)
        search_snippet = caption_text[:50].strip()
        pos = markdown.find(search_snippet)
        if pos != -1:
            return pos

        # Try fuzzy match with first sentence
        first_sentence = caption_text.split('.')[0][:80]
        pos = markdown.find(first_sentence)
        if pos != -1:
            return pos

        return None

    def _classify_placement(
        self,
        page_num: int,
        bbox: Dict,
        sections: List[Dict]
    ) -> str:
        """
        Classify as inline, end-of-section, or appendix.

        Args:
            page_num: Page number (0-indexed)
            bbox: Image bounding box
            sections: Section headers

        Returns:
            "inline" | "end_of_section" | "appendix"
        """
        # Check if in appendix/supplement section
        current_section = self._get_section_at_page(page_num, sections)
        if current_section and any(
            kw in current_section.lower()
            for kw in ['appendix', 'supplement', 'supporting', 'additional']
        ):
            return "appendix"

        # Check if clustered with other figures (end of section pattern)
        nearby_images = self._count_nearby_images(page_num, bbox)
        if nearby_images >= 2:  # Multiple figures grouped
            return "end_of_section"

        # Check vertical position - if bottom 20% of page
        page = self.doc[page_num]
        page_height = page.rect.height
        if bbox['y1'] > page_height * 0.8:
            return "end_of_section"

        return "inline"

    def _get_section_at_page(
        self,
        page_num: int,
        sections: List[Dict]
    ) -> Optional[str]:
        """Get section title at given page."""
        current_section = None
        for section in sections:
            if section.get('page_num', 0) <= page_num:
                current_section = section.get('text', '')
            else:
                break
        return current_section

    def _count_nearby_images(self, page_num: int, bbox: Dict) -> int:
        """Count images near this image (within 200 pts vertically)."""
        page = self.doc[page_num]
        images = page.get_images()
        count = 0

        for img in images:
            try:
                # Get image bbox
                img_bbox = self._get_image_bbox_from_ref(page, img)
                if not img_bbox:
                    continue

                # Check vertical proximity
                vertical_distance = min(
                    abs(img_bbox['y0'] - bbox['y1']),
                    abs(bbox['y0'] - img_bbox['y1'])
                )

                if vertical_distance < 200:  # Within 200 pts
                    count += 1
            except:
                continue

        return count - 1  # Exclude self

    def _get_image_bbox_from_ref(self, page: pymupdf.Page, img_ref) -> Optional[Dict]:
        """Get bounding box for image reference."""
        try:
            xref = img_ref[0]
            img_list = page.get_image_info(xrefs=True)
            for img_info in img_list:
                if img_info.get('xref') == xref:
                    rect = img_info.get('bbox')
                    if rect:
                        return {
                            'x0': rect[0],
                            'y0': rect[1],
                            'x1': rect[2],
                            'y1': rect[3]
                        }
        except:
            pass
        return None

    def _get_surrounding_context(
        self,
        markdown: str,
        position: Optional[int],
        context_size: int = 200
    ) -> Optional[str]:
        """Extract surrounding context from markdown."""
        if position is None:
            return None

        start = max(0, position - context_size)
        end = min(len(markdown), position + context_size)

        context = markdown[start:end]
        return context.strip()

    def _find_section(
        self,
        page_num: int,
        sections: List[Dict]
    ) -> Optional[str]:
        """Find section ID for this page."""
        section_name = self._get_section_at_page(page_num, sections)
        if section_name:
            # Create simple ID from section name
            section_id = re.sub(r'\W+', '_', section_name.lower()).strip('_')
            return section_id
        return None

    def _recommend_action(
        self,
        placement_type: str,
        context: Optional[str],
        bbox: Dict
    ) -> Dict:
        """
        Suggest whether to keep inline or move.

        Args:
            placement_type: Classification result
            context: Surrounding text
            bbox: Image bbox

        Returns:
            Dict with action and reason
        """
        if placement_type == "inline":
            # Check if text references figure nearby
            has_nearby_reference = self._check_reference_proximity(context)

            if has_nearby_reference:
                return {
                    "action": "keep_inline",
                    "reason": "Referenced in surrounding text"
                }
            else:
                return {
                    "action": "move_to_end",
                    "reason": "No nearby reference, may break flow"
                }

        elif placement_type == "end_of_section":
            return {
                "action": "group_with_figures",
                "reason": "Already grouped at section end"
            }

        else:  # appendix
            return {
                "action": "keep_inline",
                "reason": "In appendix/supplement section"
            }

    def _check_reference_proximity(self, context: Optional[str]) -> bool:
        """Check if figure is referenced in nearby text."""
        if not context:
            return False

        for pattern in self.REFERENCE_PATTERNS:
            if re.search(pattern, context):
                return True
        return False
