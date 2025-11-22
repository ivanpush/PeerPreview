"""Geometric cleaning stage for PDF documents.

Handles detection and removal of:
- Line numbers in left margin
- Headers and footers via margin cropping
- Future: Column detection
"""

import pymupdf
from typing import Tuple
import logging

from ..models import GeometryInfo
from ..config import GeometryConfig

logger = logging.getLogger(__name__)


def detect_line_numbers(doc: pymupdf.Document) -> Tuple[bool, float]:
    """Scan document for line numbers in left margin.

    Args:
        doc: pymupdf Document

    Returns:
        Tuple of (has_line_numbers: bool, cutoff_x: float)
        If has_line_numbers is True, cutoff_x is the suggested crop position
    """
    sample_pages = min(3, len(doc))
    line_num_candidates = []

    for i in range(sample_pages):
        try:
            # get_text("words") returns: (x0, y0, x1, y1, "word", block_no, line_no, word_no)
            words = doc[i].get_text("words")
            for w in words:
                text = w[4]
                x1 = w[2]  # The right-most edge of the word

                # Criteria:
                # 1. It is a digit (e.g., "1", "25")
                # 2. It is short (1-3 characters)
                # 3. It is in the left margin (x coordinate < 80 points)
                if text.isdigit() and len(text) <= 3 and x1 < 80:
                    line_num_candidates.append(x1)
        except Exception:
            continue

    # Threshold: If we find > 10 isolated numbers in the margin across 3 pages
    if len(line_num_candidates) > 10:
        # Find the right-most edge of the numbers found + 5pt buffer
        cut_x = max(line_num_candidates) + 5
        logger.info(f"Detected line numbers, suggested crop at {cut_x}pt")
        return True, cut_x

    logger.info("No line numbers detected")
    return False, 0


def detect_header_height(page: pymupdf.Page, is_first_page: bool = False) -> float:
    """Detect header height for a specific page.

    Args:
        page: The page to analyze
        is_first_page: True if this is page 1 (likely has larger header with title/authors)

    Returns:
        Top margin in points to crop the header
    """
    try:
        page_height = page.rect.height
        blocks = page.get_text("dict")["blocks"]

        # Find all text blocks and their y-positions
        text_y_positions = []
        for b in blocks:
            if b["type"] == 0:  # text block
                y0, y1 = b["bbox"][1], b["bbox"][3]
                text_y_positions.append((y0, y1))

        if not text_y_positions:
            return 60 if not is_first_page else 100

        # Sort by vertical position
        text_y_positions.sort()

        # For first page, look for a large gap indicating end of title/author block
        if is_first_page:
            # Check top 40% of page for gaps
            top_threshold = page_height * 0.4

            gaps = []
            for i in range(len(text_y_positions) - 1):
                y1_current = text_y_positions[i][1]
                y0_next = text_y_positions[i + 1][0]

                if y1_current < top_threshold:  # Only check gaps in top 40%
                    gap = y0_next - y1_current
                    gaps.append((gap, y1_current))

            if gaps:
                # Find largest gap in top section
                largest_gap, gap_y = max(gaps)

                # If gap > 40pt, likely separation between header and body
                if largest_gap > 40:
                    # Crop everything above the gap
                    margin = gap_y + 5  # Add 5pt buffer
                    result = min(max(margin, 60), 200)  # Clamp between 60-200pt
                    logger.info(f"Page 1: Detected large header, top margin: {result:.0f}pt")
                    return result

        # For non-first pages or if no clear gap found, use conservative default
        # Just look for very top header/page numbers
        first_text_y = text_y_positions[0][0]

        # If first text starts very high (< 50pt), likely just page number/header
        if first_text_y < 50:
            margin = min(60, first_text_y + 30)
        else:
            margin = 40  # Minimal crop

        return margin

    except Exception:
        return 60 if not is_first_page else 100


def detect_footer_height(doc: pymupdf.Document) -> float:
    """Detect footer height by finding the bottom-most content on sample pages.

    Returns the margin needed to exclude footers while keeping body text.
    """
    sample_pages = min(5, len(doc))
    footer_candidates = []

    for i in range(sample_pages):
        try:
            page = doc[i]
            page_height = page.rect.height
            blocks = page.get_text("dict")["blocks"]

            # Find all text blocks and their y-positions
            text_y_positions = []
            for b in blocks:
                if b["type"] == 0:  # text block
                    y0, y1 = b["bbox"][1], b["bbox"][3]
                    text_y_positions.append((y0, y1))

            if not text_y_positions:
                continue

            # Sort by vertical position
            text_y_positions.sort()

            # The main body text should be clustered together
            # Footer text is typically isolated at the bottom with a gap above it

            # Find the bottom-most text
            bottom_y = max(y1 for y0, y1 in text_y_positions)

            # Find gap before the bottom text
            # Look for largest vertical gap in bottom 20% of page
            bottom_threshold = page_height * 0.8

            gaps = []
            for i in range(len(text_y_positions) - 1):
                y1_current = text_y_positions[i][1]
                y0_next = text_y_positions[i + 1][0]

                if y0_next > bottom_threshold:  # Only check gaps in bottom 20%
                    gap = y0_next - y1_current
                    gaps.append((gap, y1_current))

            if gaps:
                # Find largest gap
                largest_gap, gap_y = max(gaps)

                # If gap > 30pt, likely footer separation
                if largest_gap > 30:
                    # Margin = distance from gap to page bottom
                    margin_needed = page_height - gap_y
                    footer_candidates.append(margin_needed)

        except Exception:
            continue

    if footer_candidates:
        # Use the median footer height to be conservative
        footer_candidates.sort()
        median_footer = footer_candidates[len(footer_candidates) // 2]
        # Add 5pt buffer
        result = min(max(median_footer + 5, 30), 80)  # Clamp between 30-80pt
        logger.info(f"Detected footer, suggested bottom margin: {result:.0f}pt")
        return result

    # Default: conservative 40pt
    return 40


def crop_margins(
    doc: pymupdf.Document,
    top: int = 60,
    bottom: int = 60,
    left: float = 0
) -> pymupdf.Document:
    """Crop margins from all pages in document with per-page header detection.

    Modifies the document in-place by setting cropbox on each page.

    Args:
        doc: pymupdf Document to modify
        top: Default points to crop from top (used if detection fails)
        bottom: Points to crop from bottom (footer)
        left: Points to crop from left (for line number removal)

    Returns:
        Modified document (same object, modified in-place)
    """
    logger.info(f"Cropping margins: default top={top}pt, bottom={bottom}pt, left={left}pt")

    for page_num, page in enumerate(doc):
        rect = page.rect

        # Detect page-specific top margin
        is_first = (page_num == 0)
        top_margin = detect_header_height(page, is_first_page=is_first)

        # Safety check: ensure page is tall enough to crop
        if rect.height < (top_margin + bottom + 100):
            logger.warning(f"Page {page_num+1} too short ({rect.height}pt) to crop safely. Skipping.")
            continue

        # Create new visible area
        new_rect = pymupdf.Rect(
            rect.x0 + left,              # Cut left margin
            rect.y0 + top_margin,        # Cut top (header) - page-specific
            rect.x1,                     # Keep right edge
            rect.y1 - bottom             # Cut bottom (footer)
        )

        # Apply the crop - text extractors will ignore content outside this box
        page.set_cropbox(new_rect)

    return doc


def analyze_geometry(doc: pymupdf.Document, config: GeometryConfig) -> GeometryInfo:
    """Analyze document geometry and detect structural elements.

    Args:
        doc: pymupdf Document
        config: Geometry configuration

    Returns:
        GeometryInfo with detected geometry information
    """
    has_line_numbers = False
    left_margin_cutoff = 0.0

    if config.detect_line_numbers:
        has_line_numbers, left_margin_cutoff = detect_line_numbers(doc)

    # Future: column detection
    has_columns = False
    column_count = 1

    return GeometryInfo(
        has_line_numbers=has_line_numbers,
        left_margin_cutoff=left_margin_cutoff,
        top_margin=config.top_margin,
        bottom_margin=config.bottom_margin,
        has_columns=has_columns,
        column_count=column_count
    )


def apply_geometric_cleaning(
    doc: pymupdf.Document,
    config: GeometryConfig
) -> Tuple[pymupdf.Document, GeometryInfo]:
    """Complete geometric cleaning pipeline.

    Analyzes document geometry, then applies cropping.

    Args:
        doc: pymupdf Document to clean
        config: Geometry configuration

    Returns:
        Tuple of (cleaned document, geometry info)
    """
    # Step 1: Analyze
    geom_info = analyze_geometry(doc, config)

    # Step 2: Detect footer height dynamically
    bottom_margin = detect_footer_height(doc)

    # Step 3: Apply crops
    doc = crop_margins(
        doc,
        top=config.top_margin,
        bottom=bottom_margin,
        left=geom_info.left_margin_cutoff
    )

    if geom_info.has_line_numbers:
        logger.info(f"Cropped left margin at {geom_info.left_margin_cutoff}pt for line numbers")

    return doc, geom_info
