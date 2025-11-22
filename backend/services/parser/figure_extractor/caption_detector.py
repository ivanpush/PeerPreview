"""Caption detection with boundary detection using font/gap heuristics."""

import re
from typing import Dict, List, Optional, Tuple
import pymupdf
from .utils import (
    bbox_overlaps,
    extract_text_from_block,
    is_caption_start,
    get_block_bbox,
    calculate_vertical_gap,
    get_span_font_size
)


class CaptionDetector:
    """Detects and extracts figure captions with intelligent boundary detection."""

    # Patterns for caption starts
    CAPTION_PATTERNS = [
        r'(?i)(figure|fig\.?)\s*\d+[a-z]?[\s\.:]\s*',  # Figure 1:, Fig. 2a.
        r'(?i)fig\s+\d+[a-z]?[\s\.:]\s*',              # fig 1:
    ]

    def __init__(self, page: pymupdf.Page, avg_line_height: float):
        """
        Initialize caption detector.

        Args:
            page: PyMuPDF page object
            avg_line_height: Average line height for adaptive thresholds
        """
        self.page = page
        self.avg_line_height = avg_line_height
        self.blocks = page.get_text("dict")["blocks"]

    def find_caption_near_image(
        self,
        search_region: Dict,
        check_above: bool = True,
        check_below: bool = True
    ) -> Optional[Tuple[str, Dict]]:
        """
        Find caption in search region near image.

        Args:
            search_region: Bounding box to search within
            check_above: Search above image
            check_below: Search below image

        Returns:
            Tuple of (caption_text, caption_bbox) or None
        """
        caption_candidates = []

        # Search for caption start in region
        for block in self.blocks:
            if block.get("type") != 0:  # Only text blocks
                continue

            block_bbox = get_block_bbox(block)
            if not block_bbox:
                continue

            # Check if block overlaps search region
            if not bbox_overlaps(block_bbox, search_region):
                continue

            # Check vertical position relative to image
            img_y = (search_region['y0'] + search_region['y1']) / 2
            block_y = (block_bbox[1] + block_bbox[3]) / 2

            # Filter by position
            if not check_above and block_y < img_y:
                continue
            if not check_below and block_y > img_y:
                continue

            # Extract text
            text = extract_text_from_block(block)
            if not text:
                continue

            # Check if caption start
            if is_caption_start(text, self.CAPTION_PATTERNS):
                # Found potential caption start
                caption_text, caption_bbox = self._extract_full_caption(block)
                if caption_text:
                    # Calculate distance from image
                    distance = abs(block_y - img_y)
                    caption_candidates.append((caption_text, caption_bbox, distance))

        # Return closest caption
        if caption_candidates:
            caption_candidates.sort(key=lambda x: x[2])  # Sort by distance
            return caption_candidates[0][0], caption_candidates[0][1]

        return None

    def _extract_full_caption(self, start_block: Dict) -> Tuple[str, Dict]:
        """
        Extract complete caption starting from block.

        Uses boundary detection:
        - Stop at next figure pattern
        - Stop at bold section header
        - Stop at large vertical gap (> 2× avg line height)
        - Stop at drastic font size change
        - Stop at very long paragraph (> 300 chars in single block)

        Args:
            start_block: Block containing caption start

        Returns:
            Tuple of (full_caption_text, caption_bbox)
        """
        caption_parts = []
        start_idx = self.blocks.index(start_block)

        # Get baseline font size from start block
        baseline_font_size = self._get_block_font_size(start_block)

        # Start with first block
        caption_parts.append(extract_text_from_block(start_block))

        # Track bbox
        caption_bbox = list(start_block.get('bbox', [0, 0, 0, 0]))

        # Look at subsequent blocks
        for i in range(start_idx + 1, len(self.blocks)):
            block = self.blocks[i]

            if block.get("type") != 0:  # Skip non-text blocks
                continue

            # Check stopping conditions
            text = extract_text_from_block(block)
            if not text:
                continue

            # 1. Stop at next figure pattern
            if is_caption_start(text, self.CAPTION_PATTERNS):
                break

            # 2. Stop at large vertical gap
            prev_block = self.blocks[i - 1]
            gap = calculate_vertical_gap(prev_block, block)
            if gap > 2.0 * self.avg_line_height:
                break

            # 3. Stop at drastic font size change
            block_font_size = self._get_block_font_size(block)
            if baseline_font_size > 0:
                size_ratio = block_font_size / baseline_font_size
                if size_ratio > 1.3 or size_ratio < 0.7:  # >30% change
                    break

            # 4. Stop at very long single paragraph
            if len(text) > 300:
                # Check if this looks like body text (not caption)
                # Captions are usually concise
                # Add this block and stop
                caption_parts.append(text)
                self._expand_bbox(caption_bbox, block.get('bbox'))
                break

            # 5. Check if bold (potential section header)
            if self._is_block_bold(block):
                # If bold and looks like header, stop
                if self._looks_like_header(text):
                    break

            # Continue adding to caption
            caption_parts.append(text)
            self._expand_bbox(caption_bbox, block.get('bbox'))

            # Safety: max 5 blocks for a caption
            if len(caption_parts) >= 5:
                break

        full_caption = " ".join(caption_parts)

        bbox_dict = {
            'x0': caption_bbox[0],
            'y0': caption_bbox[1],
            'x1': caption_bbox[2],
            'y1': caption_bbox[3]
        }

        return full_caption, bbox_dict

    def _get_block_font_size(self, block: Dict) -> float:
        """Get average font size in block."""
        sizes = []

        for line in block.get("lines", []):
            for span in line.get("spans", []):
                size = get_span_font_size(span)
                if size > 0:
                    sizes.append(size)

        if sizes:
            return sum(sizes) / len(sizes)
        return 0.0

    def _is_block_bold(self, block: Dict) -> bool:
        """Check if block contains predominantly bold text."""
        bold_count = 0
        total_count = 0

        for line in block.get("lines", []):
            for span in line.get("spans", []):
                total_count += 1
                font_name = span.get("font", "").lower()
                font_flags = span.get("flags", 0)

                # Bold detection
                is_bold = (font_flags & 16) or "bold" in font_name or "heavy" in font_name
                if is_bold:
                    bold_count += 1

        if total_count == 0:
            return False

        return (bold_count / total_count) > 0.5  # >50% bold

    def _looks_like_header(self, text: str) -> bool:
        """Check if text looks like a section header."""
        # Headers are typically:
        # - Short (<100 chars)
        # - Title case or ALL CAPS
        # - No ending punctuation
        # - Match common section patterns

        if len(text) > 100:
            return False

        # Check for common section keywords
        section_keywords = [
            'introduction', 'background', 'methods', 'results',
            'discussion', 'conclusion', 'abstract', 'references',
            'acknowledgment', 'appendix', 'summary'
        ]

        text_lower = text.lower().strip()
        if any(kw in text_lower for kw in section_keywords):
            return True

        # Check if title case (most words capitalized)
        words = text.split()
        if words:
            capitalized = sum(1 for w in words if w and w[0].isupper())
            if capitalized / len(words) > 0.6:  # >60% capitalized
                return True

        return False

    def _expand_bbox(self, bbox: List, new_bbox: Optional[Tuple]) -> None:
        """Expand bbox to include new_bbox (in-place)."""
        if not new_bbox:
            return

        bbox[0] = min(bbox[0], new_bbox[0])  # x0
        bbox[1] = min(bbox[1], new_bbox[1])  # y0
        bbox[2] = max(bbox[2], new_bbox[2])  # x1
        bbox[3] = max(bbox[3], new_bbox[3])  # y1
