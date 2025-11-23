"""Geometric cleaning stage for PDF documents.

Handles detection and removal of:
- Line numbers in left margin
- Headers and footers via margin cropping
- Future: Column detection
"""

import pymupdf
import re
from typing import Tuple, List
import logging

from ..models import GeometryInfo, StructureInfo, FigureCaption
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

    Conservative approach: Only crop actual headers (journal info, DOIs), not body content.
    This preserves captions that may appear near the top of pages.

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
            return 40 if not is_first_page else 60  # Reduced defaults

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
                    result = min(max(margin, 40), 150)  # Reduced: clamp between 40-150pt
                    logger.info(f"Page 1: Detected large header, top margin: {result:.0f}pt")
                    return result

        # For non-first pages, be VERY conservative - only crop if we find actual header content
        # Look at top 60pt (reduced from 100pt) for header patterns
        header_blocks = []
        for b in blocks:
            if b.get("type") == 0:
                y0, y1 = b["bbox"][1], b["bbox"][3]
                if y1 < 60:  # Only check top 60pt (reduced from 100pt)
                    text = "".join(
                        span.get("text", "")
                        for line in b.get("lines", [])
                        for span in line.get("spans", [])
                    ).strip()
                    header_blocks.append((y0, y1, text))

        # Check for header patterns (DOI, journal names, etc.)
        import re
        header_patterns = [
            r'doi\.org',
            r'https?://',
            r'(nature|science|cell|plos)\s+(biomedical|communications?|medicine)',
            r'articles?',
            r'^\d+\s*$',  # Page numbers
        ]

        max_header_y = 30  # Very conservative default (reduced from 60pt)
        for y0, y1, text in header_blocks:
            if any(re.search(pat, text.lower()) for pat in header_patterns):
                max_header_y = max(max_header_y, y1 + 5)  # Crop below this block

        return min(max_header_y, 50)  # Reduced: clamp max at 50pt (was 100pt)

    except Exception:
        return 40 if not is_first_page else 60  # Reduced defaults


def detect_footer_height(doc: pymupdf.Document) -> float:
    """Conservative footer detection - only crop journal/publisher footers.

    Returns a minimal margin (20-40pt) to preserve caption continuations.
    Caption detection will filter out footer text via pattern matching.
    """
    # Just return a conservative 35pt margin
    # This preserves most caption continuations while cropping page numbers
    logger.info("Using conservative 35pt bottom margin (caption detection will filter footer text)")
    return 35


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


def _extract_block_text(block: dict) -> str:
    """Extract all text from a pymupdf block."""
    text = ""
    for line in block.get("lines", []):
        for span in line.get("spans", []):
            text += span.get("text", "")
    return text.strip()


def _check_if_bold(block: dict) -> bool:
    """Check if any text in block is bold."""
    for line in block.get("lines", []):
        for span in line.get("spans", []):
            font_flags = span.get("flags", 0)
            if font_flags & 2**4:  # Bold flag
                return True
    return False


def detect_captions(doc: pymupdf.Document) -> List[FigureCaption]:
    """Detect figure/table captions in a PDF document.

    Handles both:
    1. Journal-style short captions (Fig. 1 | Description)
    2. Word doc style long multi-block captions (Figure 1: Full paragraph...)

    Filters out inline references (Figure X shows/demonstrates/etc.)

    Args:
        doc: pymupdf Document (after cropping)

    Returns:
        List of FigureCaption objects
    """
    captions = []

    # Caption start pattern (matches "Figure 1:", "Fig. 2A", "Table 3", etc.)
    caption_start_pattern = re.compile(
        r'^\s*(Figure|Fig\.?|Table|Scheme)\s*'  # Figure/Fig/Table/Scheme
        r'(S)?'                                  # Optional 'S' for supplementary
        r'(\d+)'                                 # Number (required)
        r'([A-Z])?'                              # Optional letter for subfigures
        r'[\s\.:|\-]*',                          # Optional separators
        re.IGNORECASE
    )

    # Inline reference verbs (to exclude - these are NOT standalone captions)
    # Only match when verb comes IMMEDIATELY after figure label (within 5 chars)
    # E.g., "Figure 3 shows..." NOT "Figure 3: Results show..."
    inline_verb_pattern = re.compile(
        r'^\s*(Figure|Fig\.?|Table|Scheme)\s*'
        r'(S)?'
        r'(\d+)'
        r'([A-Z])?'
        r'\s{0,5}'  # Max 5 spaces between label and verb (no colons/dashes)
        r'(shows?|demonstrates?|illustrates?|reveals?|presents?|depicts?|'
        r'displays?|indicates?|suggests?|confirms?|contains?|provides?|'
        r'summarizes?|compares?|highlights?)',
        re.IGNORECASE
    )

    for page_num, page in enumerate(doc):
        text_dict = page.get_text("dict")
        blocks = text_dict.get("blocks", [])

        i = 0
        while i < len(blocks):
            block = blocks[i]

            if block.get("type") != 0:  # Skip non-text blocks
                i += 1
                continue

            bbox = block.get("bbox")
            if not bbox:
                i += 1
                continue

            # Extract text from current block
            block_text = _extract_block_text(block)

            # Check if it matches caption start pattern
            match = caption_start_pattern.match(block_text)
            if not match:
                i += 1
                continue

            # Check if this is an inline reference (NOT a standalone caption)
            if inline_verb_pattern.match(block_text):
                logger.debug(f"Skipping inline reference on page {page_num}: {block_text[:60]}...")
                i += 1
                continue

            # This is a caption! Extract figure metadata
            fig_type = match.group(1).lower()
            is_supplementary = bool(match.group(2))
            number = match.group(3)
            subfig = match.group(4) or ""

            # Start building full caption text and bbox
            full_caption = block_text
            caption_bbox = list(bbox)
            is_bold = _check_if_bold(block)

            # Footer patterns to stop caption continuation
            footer_stop_patterns = [
                r'(nature|science|cell|plos|elsevier|wiley|springer)\s+(biomedical|communications?)',
                r'(biorxiv|medrxiv|arxiv)\s+preprint',
                r'doi:\s*10\.',
                r'www\.(nature|science|cell)',
                r'©\s*\d{4}',
                r'macmillan\s+publishers',
                # NEW: Author/page patterns (common in journal footers)
                r'[A-Z][a-z]+\s+et\s+al\..*[Pp]age\s+\d+',  # "Author et al.Page 27"
                r'[Pp]age\s+\d+\s*$',                        # "Page 27" at end
                r'^\d+\s*$',                                  # Just "27" (page number alone)
                r'^\s*\|\s*\d+\s*$',                          # "| 131" (journal page format)
            ]

            # Continue to subsequent blocks if they're part of the same caption
            # (Important for Word doc PDFs with long captions spanning multiple blocks)
            j = i + 1
            continuation_count = 0
            MAX_CONTINUATION_BLOCKS = 20  # Safety limit to prevent runaway

            while j < len(blocks) and continuation_count < MAX_CONTINUATION_BLOCKS:
                next_block = blocks[j]

                if next_block.get("type") != 0:
                    break

                next_text = _extract_block_text(next_block)
                next_bbox = next_block["bbox"]

                # Check if this is footer content (STOP if so)
                is_footer = any(re.search(pat, next_text.lower()) for pat in footer_stop_patterns)
                if is_footer:
                    logger.debug(f"Stopping caption continuation at footer pattern: {next_text[:50]}...")
                    break

                # Check if next block starts with a new caption (STOP if so)
                if caption_start_pattern.match(next_text):
                    break

                # Check if next block is a continuation of the caption:
                # Strategy: Be more permissive with vertical gaps for caption continuations
                # Many captions have inconsistent line spacing, especially with references/superscripts

                vertical_gap = next_bbox[1] - caption_bbox[3]
                horizontal_overlap = (
                    min(caption_bbox[2], next_bbox[2]) - max(caption_bbox[0], next_bbox[0])
                ) / max(caption_bbox[2] - caption_bbox[0], 1)

                # Adaptive vertical gap tolerance:
                # - First few continuations: allow up to 40pt (handles references, superscripts)
                # - Later continuations: stricter 25pt (prevents jumping to unrelated text)
                max_gap = 40 if continuation_count < 3 else 25

                # Minimum horizontal overlap: 40% (relaxed from 50% to handle column shifts)
                min_overlap = 0.4

                # Check for special continuation patterns that override strict requirements
                starts_lowercase = next_text and next_text[0].islower()
                has_continuation_punct = next_text.startswith((',', ';', 'and', 'or'))
                is_reference = re.match(r'^\[[\d,\-]+\]', next_text.strip())  # [1,2,3]
                # NEW: Detect citation lines (Author et al. [refs])
                is_citation = re.match(r'^[A-Z][a-z]+\s+et\s+al\.', next_text)  # "Pushkarsky et al."

                # Stop if:
                # - Vertical gap too large for current position
                # - Poor horizontal alignment
                if vertical_gap > max_gap or horizontal_overlap < min_overlap:
                    # But wait - check if this might still be continuation text
                    # Sometimes there's a gap but text is clearly part of caption

                    # Special case: Citation lines (e.g., "Pushkarsky et al. [13,15,16]")
                    # These are often narrow (<30% overlap) but are clearly part of caption
                    if is_citation and vertical_gap <= 20 and horizontal_overlap > 0.2:
                        logger.debug(f"Continuing for citation line despite narrow width ({horizontal_overlap:.1%})")
                    # General continuation signals: lowercase start, punctuation, references
                    elif (starts_lowercase or has_continuation_punct or is_reference) and vertical_gap <= 60:
                        logger.debug(f"Continuing despite gap ({vertical_gap:.0f}pt) - continuation signal detected")
                    else:
                        logger.debug(f"Stopping caption: gap={vertical_gap:.0f}pt, overlap={horizontal_overlap:.2f}")
                        break

                # This is a continuation - append it
                full_caption += " " + next_text
                caption_bbox[2] = max(caption_bbox[2], next_bbox[2])  # Extend right
                caption_bbox[3] = next_bbox[3]  # Extend bottom

                # Check if continuation block is also bold
                if not is_bold:
                    is_bold = _check_if_bold(next_block)

                j += 1
                continuation_count += 1

            # Create caption object
            captions.append(FigureCaption(
                text=full_caption.strip(),
                page=page_num,
                bbox=tuple(caption_bbox),
                figure_type=fig_type,
                figure_num=number + subfig,
                y_position=caption_bbox[1],  # Top y-coordinate
                is_bold=is_bold,
                confidence=1.0 if is_bold else 0.8,
                is_standalone=True
            ))

            logger.debug(f"Captured caption on page {page_num}: {full_caption[:80]}...")

            # Skip the blocks we've consumed
            i = j

    logger.info(f"Detected {len(captions)} captions")
    return captions


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
    config: GeometryConfig,
    structure_info: StructureInfo = None
) -> Tuple[pymupdf.Document, GeometryInfo]:
    """Complete geometric cleaning pipeline.

    Analyzes document geometry, applies cropping, then detects figure captions and regions.

    Args:
        doc: pymupdf Document to clean
        config: Geometry configuration
        structure_info: Optional StructureInfo (not currently used, kept for compatibility)

    Returns:
        Tuple of (cleaned document, geometry info with captions and regions)
    """
    # Step 1: Analyze geometry
    geom_info = analyze_geometry(doc, config)

    # Step 2: Detect footer height dynamically
    bottom_margin = detect_footer_height(doc)

    # Step 3: Apply crops (removes headers/footers)
    doc = crop_margins(
        doc,
        top=config.top_margin,
        bottom=bottom_margin,
        left=geom_info.left_margin_cutoff
    )

    if geom_info.has_line_numbers:
        logger.info(f"Cropped left margin at {geom_info.left_margin_cutoff}pt for line numbers")

    # Step 4: Detect captions on CROPPED pages (after footer removal)
    geom_info.figure_captions = detect_captions(doc)
    logger.info(f"Detected {len(geom_info.figure_captions)} captions on cropped pages")

    # Step 5: Detect figure regions using captions detected above
    if geom_info.figure_captions:
        from .figures import detect_figure_regions
        geom_info.figure_regions = detect_figure_regions(
            doc,
            geom_info.figure_captions,
            config
        )

    return doc, geom_info
