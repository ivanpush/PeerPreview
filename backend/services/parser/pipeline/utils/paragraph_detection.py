"""
Paragraph Detection Utility

Distinguishes between proper body paragraphs and figure artifacts (labels, legends, scattered text).
Used by semantic figure detection to determine where to stop boundary expansion.
"""

from typing import Dict, List, Any


def is_proper_paragraph(text_block: Dict[str, Any], page_width: float) -> bool:
    """
    Classify text block as body paragraph vs figure artifact.

    This is critical for semantic figure boundary expansion - we expand
    figure regions until hitting a "proper paragraph" (real body text).

    Args:
        text_block: pymupdf text block dict with 'bbox', 'lines', etc.
        page_width: Width of the page in points

    Returns:
        True if this is a proper paragraph (stop expansion), False if artifact (continue)

    Classification Criteria:

    PROPER PARAGRAPH (stop expansion):
    - Word count ≥20 words (real prose)
    - Multi-line ≥3 lines with ≥15 words total
    - Line height 10-16pt (standard body text)
    - Spans >40% of estimated column width
    - Contains sentence structure (period + capitals)

    FIGURE ARTIFACT (continue expansion):
    - Word count <10 words (labels, legends)
    - Line height <10pt or >20pt (tiny labels or figure titles)
    - Single line of text
    - Narrow <30% of column width (scattered labels)
    - Number-heavy >40% digits/symbols (axis values, measurements)
    - All caps or all lowercase (often labels)
    """
    # Extract text content
    text = extract_block_text_simple(text_block)
    if not text:
        return False

    words = text.split()
    word_count = len(words)
    lines = text_block.get("lines", [])
    line_count = len(lines)

    bbox = text_block.get("bbox")
    if not bbox:
        return False

    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]

    # RULE 1: Word count (most reliable indicator)
    if word_count >= 20:
        return True  # Definitely a paragraph
    if word_count < 5:
        return False  # Definitely an artifact

    # RULE 2: Multi-line prose
    # If we have 3+ lines with 15+ words, likely paragraph
    if line_count >= 3 and word_count >= 15:
        return True

    # RULE 3: Horizontal extent (relative to column width)
    # Estimate column width as ~45% of page for 2-column layout
    # Conservative estimate to avoid false positives
    column_width_estimate = page_width * 0.45

    if width < column_width_estimate * 0.3:
        # Too narrow - likely a label or scattered text
        return False

    # RULE 4: Line height consistency
    # Body text typically has consistent line height of 10-16pt
    if line_count >= 2:
        line_heights = []
        for line in lines:
            line_bbox = line.get("bbox")
            if line_bbox:
                line_heights.append(line_bbox[3] - line_bbox[1])

        if line_heights:
            avg_height = sum(line_heights) / len(line_heights)

            # Standard body text range
            if 10 <= avg_height <= 16 and word_count >= 10:
                return True

            # Too small (labels) or too large (figure titles)
            if avg_height < 8 or avg_height > 20:
                return False

    # RULE 5: Sentence structure
    # Real paragraphs have periods and capital letters (sentences)
    if '.' in text and any(c.isupper() for c in text):
        if word_count >= 10:
            return True

    # RULE 6: Number-heavy content
    # Axis labels, measurements, data tables have many digits
    # e.g., "0 5 10 15 20", "p < 0.05", "n = 47"
    char_count = len(text.replace(' ', ''))
    if char_count > 0:
        digit_count = sum(c.isdigit() for c in text)
        if digit_count / char_count > 0.4:
            # More than 40% digits - likely measurement/label
            return False

    # RULE 7: All caps or all lowercase
    # Figure labels often all caps ("FIGURE 1A") or all lowercase ("mm")
    alpha_chars = [c for c in text if c.isalpha()]
    if alpha_chars:
        if all(c.isupper() for c in alpha_chars) or all(c.islower() for c in alpha_chars):
            if word_count < 10:
                return False

    # DEFAULT: For ambiguous cases (10-20 words), lean toward "not paragraph"
    # This makes expansion more conservative (stops sooner)
    return word_count >= 15


def extract_block_text_simple(block: Dict[str, Any]) -> str:
    """
    Extract plain text from a pymupdf text block.

    Args:
        block: pymupdf text block dict

    Returns:
        Concatenated text from all spans in the block
    """
    text_parts = []

    lines = block.get("lines", [])
    for line in lines:
        spans = line.get("spans", [])
        for span in spans:
            span_text = span.get("text", "")
            if span_text:
                text_parts.append(span_text)

    return " ".join(text_parts)


def get_text_blocks_in_region(
    page: Any,  # pymupdf.Page
    region: tuple[float, float, float, float]
) -> List[Dict[str, Any]]:
    """
    Get all text blocks that overlap with a given region.

    Args:
        page: pymupdf Page object
        region: Tuple of (x0, y0, x1, y1) defining search region

    Returns:
        List of text block dicts that overlap the region
    """
    x0, y0, x1, y1 = region
    all_blocks = page.get_text("dict")["blocks"]

    matching_blocks = []
    for block in all_blocks:
        # Skip non-text blocks (images, etc.)
        if block.get("type") != 0:
            continue

        bbox = block.get("bbox")
        if not bbox:
            continue

        bx0, by0, bx1, by1 = bbox

        # Check for overlap with region
        # Boxes overlap if they don't NOT overlap
        if not (bx1 < x0 or bx0 > x1 or by1 < y0 or by0 > y1):
            matching_blocks.append(block)

    return matching_blocks


def find_table_like_text(
    page: Any,  # pymupdf.Page
    region: tuple[float, float, float, float]
) -> List[Dict[str, Any]]:
    """
    Detect table-like text structures within a region.

    Tables have characteristic patterns:
    - Multiple lines of aligned text
    - Consistent column structure (same x-positions repeated)
    - Repetitive spacing patterns

    Used for orphan captions that might be labeling tables rather than images.

    Args:
        page: pymupdf Page object
        region: Search region (x0, y0, x1, y1)

    Returns:
        List of text blocks that appear to be table content
    """
    blocks = get_text_blocks_in_region(page, region)

    table_blocks = []
    for block in blocks:
        lines = block.get("lines", [])

        # Tables typically have multiple lines (≥3)
        if len(lines) < 3:
            continue

        # Check for consistent x-alignment (indicates columns)
        x_positions = []
        for line in lines:
            for span in line.get("spans", []):
                span_bbox = span.get("bbox")
                if span_bbox:
                    x_positions.append(span_bbox[0])

        # Round to 10pt grid and count unique positions
        # Tables have 2-5 consistent column positions
        rounded_positions = set(round(x / 10) * 10 for x in x_positions)

        if 2 <= len(rounded_positions) <= 5:
            # Has column-like structure
            table_blocks.append(block)

    return table_blocks
