"""Main figure extraction orchestrator."""

import uuid
import logging
from typing import List, Tuple, Optional, Dict
import pymupdf

from .models import FigureUnit
from .placement_analyzer import FigurePlacementAnalyzer
from .caption_detector import CaptionDetector
from .utils import (
    get_avg_line_height,
    create_search_region,
    get_image_bbox,
    extract_figure_number,
    clean_caption_text
)

logger = logging.getLogger(__name__)


class FigureExtractor:
    """
    Extract figures and captions from scientific PDFs.

    Uses image detection as anchor, then searches for nearby captions
    with adaptive proximity based on page metrics.
    """

    def __init__(self, preserve_positions: bool = True):
        """
        Initialize extractor.

        Args:
            preserve_positions: Insert [FIGURE:id] markers in markdown
        """
        self.preserve_positions = preserve_positions

    def extract(
        self,
        doc: pymupdf.Document,
        raw_markdown: str,
        section_headers: Optional[List[Dict]] = None
    ) -> Tuple[str, List[FigureUnit]]:
        """
        Extract all figures with placement context.

        Args:
            doc: PyMuPDF document
            raw_markdown: Raw markdown text (before cleanup)
            section_headers: Section headers from BoldTextAnalyzer

        Returns:
            Tuple of (cleaned_markdown, figure_units)
        """
        if section_headers is None:
            section_headers = []

        figures = []
        placement_analyzer = FigurePlacementAnalyzer(doc)

        logger.info(f"Starting figure extraction from {len(doc)} pages")

        # Process each page
        for page_num, page in enumerate(doc):
            page_figures = self._extract_page_figures(
                page,
                page_num,
                raw_markdown,
                section_headers,
                placement_analyzer
            )
            figures.extend(page_figures)

        logger.info(f"Extracted {len(figures)} figures")

        # Remove captions from markdown
        cleaned_md = self._remove_captions_from_markdown(raw_markdown, figures)

        # Optionally insert position markers
        if self.preserve_positions:
            cleaned_md = self._insert_figure_markers(cleaned_md, figures)

        return cleaned_md, figures

    def _extract_page_figures(
        self,
        page: pymupdf.Page,
        page_num: int,
        markdown: str,
        section_headers: List[Dict],
        placement_analyzer: FigurePlacementAnalyzer
    ) -> List[FigureUnit]:
        """Extract figures from a single page."""
        figures = []

        # Get average line height for adaptive proximity
        avg_line_height = get_avg_line_height(page)
        logger.debug(f"Page {page_num}: avg line height = {avg_line_height:.2f}")

        # Get images on page
        images = page.get_images()
        logger.debug(f"Page {page_num}: found {len(images)} images")

        # Create caption detector for this page
        caption_detector = CaptionDetector(page, avg_line_height)

        for img_index, img in enumerate(images):
            # Get image bbox
            img_bbox = get_image_bbox(page, img)
            if not img_bbox:
                logger.debug(f"Page {page_num}, image {img_index}: no bbox found")
                continue

            logger.debug(f"Page {page_num}, image {img_index}: bbox = {img_bbox}")

            # Create search region with adaptive margins
            search_region = create_search_region(
                img_bbox,
                avg_line_height,
                vertical_multiplier=3.0
            )

            # Find caption near image (check both below and above)
            caption_result = caption_detector.find_caption_near_image(
                search_region,
                check_above=True,
                check_below=True
            )

            if not caption_result:
                logger.debug(f"Page {page_num}, image {img_index}: no caption found")
                # Still create figure unit for unlabeled image
                figure_unit = self._create_unlabeled_figure(
                    page_num,
                    img_bbox,
                    img_index,
                    markdown,
                    section_headers,
                    placement_analyzer
                )
                figures.append(figure_unit)
                continue

            caption_text, caption_bbox = caption_result
            logger.debug(f"Page {page_num}, image {img_index}: found caption '{caption_text[:50]}...'")

            # Create figure unit with full context
            figure_unit = self._create_figure_unit(
                caption_text,
                page_num,
                img_bbox,
                img_index,
                caption_bbox,
                markdown,
                section_headers,
                placement_analyzer
            )

            figures.append(figure_unit)

        return figures

    def _create_figure_unit(
        self,
        caption_text: str,
        page_num: int,
        img_bbox: Dict,
        img_index: int,
        caption_bbox: Dict,
        markdown: str,
        section_headers: List[Dict],
        placement_analyzer: FigurePlacementAnalyzer
    ) -> FigureUnit:
        """Create FigureUnit with all metadata."""
        # Extract figure number
        fig_number = extract_figure_number(caption_text)

        # Clean caption (remove "Figure X:" prefix)
        cleaned_caption = clean_caption_text(caption_text)

        # Analyze placement
        placement_info = placement_analyzer.analyze_placement(
            img_bbox,
            page_num,
            markdown,
            section_headers,
            cleaned_caption
        )

        # Create unit
        return FigureUnit(
            id=str(uuid.uuid4()),
            figure_number=fig_number,
            caption_text=cleaned_caption,
            raw_caption=caption_text,
            page_number=page_num,
            image_bbox=img_bbox,
            image_index=img_index,
            caption_bbox=caption_bbox,
            image_bytes=None,  # Future: extract actual image
            **placement_info
        )

    def _create_unlabeled_figure(
        self,
        page_num: int,
        img_bbox: Dict,
        img_index: int,
        markdown: str,
        section_headers: List[Dict],
        placement_analyzer: FigurePlacementAnalyzer
    ) -> FigureUnit:
        """Create FigureUnit for unlabeled image."""
        # Analyze placement without caption
        placement_info = placement_analyzer.analyze_placement(
            img_bbox,
            page_num,
            markdown,
            section_headers,
            ""  # No caption
        )

        return FigureUnit(
            id=str(uuid.uuid4()),
            figure_number=None,
            caption_text="[Unlabeled figure]",
            raw_caption="",
            page_number=page_num,
            image_bbox=img_bbox,
            image_index=img_index,
            caption_bbox=None,
            image_bytes=None,
            **placement_info
        )

    def _remove_captions_from_markdown(
        self,
        markdown: str,
        figures: List[FigureUnit]
    ) -> str:
        """
        Remove caption text from markdown using fuzzy matching.

        Args:
            markdown: Original markdown
            figures: Extracted figures

        Returns:
            Markdown with captions removed
        """
        cleaned = markdown

        for fig in figures:
            if not fig.raw_caption:
                continue

            # Try to remove caption
            cleaned = self._fuzzy_remove_caption(cleaned, fig.raw_caption)

        return cleaned

    def _fuzzy_remove_caption(self, markdown: str, caption: str) -> str:
        """
        Remove caption from markdown with fuzzy matching.

        Handles cases where markdown reflows paragraphs differently.
        """
        # Try exact match first
        if caption in markdown:
            return markdown.replace(caption, '', 1)

        # Try matching first 40 chars (fuzzy)
        caption_start = caption[:40].strip()
        if caption_start in markdown:
            # Find full caption by looking for paragraph boundary
            start_idx = markdown.find(caption_start)
            end_idx = self._find_paragraph_end(markdown, start_idx)

            # Remove paragraph
            return markdown[:start_idx] + markdown[end_idx:]

        # Try matching first sentence
        first_sentence = caption.split('.')[0]
        if len(first_sentence) > 20 and first_sentence in markdown:
            start_idx = markdown.find(first_sentence)
            end_idx = self._find_paragraph_end(markdown, start_idx)
            return markdown[:start_idx] + markdown[end_idx:]

        # Could not find caption to remove
        logger.debug(f"Could not remove caption: {caption[:50]}...")
        return markdown

    def _find_paragraph_end(self, text: str, start_idx: int) -> int:
        """
        Find end of paragraph starting at start_idx.

        Paragraph ends at double newline or end of text.
        """
        # Look for double newline
        double_newline = text.find('\n\n', start_idx)
        if double_newline != -1:
            return double_newline + 2  # Include the newlines

        # No double newline, go to end
        return len(text)

    def _insert_figure_markers(
        self,
        markdown: str,
        figures: List[FigureUnit]
    ) -> str:
        """
        Insert [FIGURE:id] markers where figures were located.

        Args:
            markdown: Cleaned markdown (captions removed)
            figures: Figure units with position info

        Returns:
            Markdown with position markers
        """
        # Sort figures by position (descending) to avoid offset issues
        positioned_figures = [
            f for f in figures
            if f.markdown_position is not None
        ]
        positioned_figures.sort(key=lambda f: f.markdown_position, reverse=True)

        result = markdown

        for fig in positioned_figures:
            pos = fig.markdown_position
            if pos > len(result):
                continue

            marker = f"[FIGURE:{fig.id}]"

            # Insert marker at position
            result = result[:pos] + marker + result[pos:]

        return result
