"""Utility functions for figure extraction."""

import re
from typing import Dict, List, Tuple, Optional
import pymupdf


def get_avg_line_height(page: pymupdf.Page) -> float:
    """
    Calculate average line height on page for adaptive proximity.

    Args:
        page: PyMuPDF page object

    Returns:
        Average line height in PDF points
    """
    blocks = page.get_text("dict")["blocks"]
    heights = []

    for block in blocks:
        if block.get("type") != 0:  # Only text blocks
            continue

        for line in block.get("lines", []):
            line_bbox = line.get("bbox")
            if line_bbox:
                height = line_bbox[3] - line_bbox[1]  # y1 - y0
                if height > 0:
                    heights.append(height)

    if heights:
        return sum(heights) / len(heights)
    return 12.0  # Default fallback


def create_search_region(
    img_bbox: Dict,
    avg_line_height: float,
    vertical_multiplier: float = 3.0
) -> Dict:
    """
    Create search region around image using adaptive margins.

    Args:
        img_bbox: Image bounding box {x0, y0, x1, y1}
        avg_line_height: Average line height on page
        vertical_multiplier: How many line heights to search above/below

    Returns:
        Expanded bbox for searching
    """
    vertical_margin = avg_line_height * vertical_multiplier
    horizontal_margin = avg_line_height * 1.0  # 1× for horizontal

    return {
        'x0': img_bbox['x0'] - horizontal_margin,
        'y0': img_bbox['y0'] - vertical_margin,
        'x1': img_bbox['x1'] + horizontal_margin,
        'y1': img_bbox['y1'] + vertical_margin
    }


def bbox_overlaps(bbox1: Tuple, bbox2: Dict) -> bool:
    """
    Check if two bounding boxes overlap.

    Args:
        bbox1: Tuple (x0, y0, x1, y1)
        bbox2: Dict {x0, y0, x1, y1}

    Returns:
        True if boxes overlap
    """
    # Convert bbox2 to tuple for consistency
    b2 = (bbox2['x0'], bbox2['y0'], bbox2['x1'], bbox2['y1'])

    # Check for non-overlap conditions
    if bbox1[2] < b2[0]:  # bbox1 left of bbox2
        return False
    if bbox1[0] > b2[2]:  # bbox1 right of bbox2
        return False
    if bbox1[3] < b2[1]:  # bbox1 above bbox2
        return False
    if bbox1[1] > b2[3]:  # bbox1 below bbox2
        return False

    return True


def extract_text_from_block(block: Dict) -> str:
    """
    Extract text from a text block.

    Args:
        block: PyMuPDF text block dict

    Returns:
        Concatenated text from all lines
    """
    text_parts = []

    for line in block.get("lines", []):
        for span in line.get("spans", []):
            text = span.get("text", "").strip()
            if text:
                text_parts.append(text)

    return " ".join(text_parts)


def get_image_bbox(page: pymupdf.Page, img_ref) -> Optional[Dict]:
    """
    Get bounding box for an image reference.

    Args:
        page: PyMuPDF page
        img_ref: Image reference from page.get_images()

    Returns:
        Bbox dict or None if not found
    """
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
    except Exception as e:
        return None

    return None


def is_caption_start(text: str, patterns: List[str]) -> bool:
    """
    Check if text starts with a figure caption pattern.

    Args:
        text: Text to check
        patterns: List of regex patterns

    Returns:
        True if matches a pattern
    """
    text_stripped = text.strip()
    for pattern in patterns:
        if re.match(pattern, text_stripped):
            return True
    return False


def extract_figure_number(caption: str) -> Optional[str]:
    """
    Extract figure number from caption text.

    Args:
        caption: Caption text (e.g., "Figure 1: Description")

    Returns:
        Figure number (e.g., "1", "2a") or None
    """
    if not caption:
        return None

    # Patterns for figure numbers
    patterns = [
        r'(?i)figure\s+(\d+[a-z]?)',
        r'(?i)fig\.?\s+(\d+[a-z]?)',
    ]

    for pattern in patterns:
        match = re.search(pattern, caption)
        if match:
            return match.group(1)

    return None


def clean_caption_text(caption: str) -> str:
    """
    Remove 'Figure X:' prefix from caption.

    Args:
        caption: Full caption text

    Returns:
        Cleaned caption without prefix
    """
    if not caption:
        return ""

    # Remove "Figure X:" or "Fig. X:" prefix
    cleaned = re.sub(
        r'(?i)^(figure|fig\.?)\s*\d+[a-z]?[\s\.:]+',
        '',
        caption
    ).strip()

    return cleaned


def get_block_bbox(block: Dict) -> Optional[Tuple]:
    """
    Get bounding box from block dict.

    Args:
        block: PyMuPDF block dict

    Returns:
        Bbox tuple (x0, y0, x1, y1) or None
    """
    bbox = block.get('bbox')
    if bbox:
        return tuple(bbox)
    return None


def calculate_vertical_gap(block1: Dict, block2: Dict) -> float:
    """
    Calculate vertical gap between two blocks.

    Args:
        block1: First block
        block2: Second block (below block1)

    Returns:
        Vertical distance in PDF points
    """
    bbox1 = block1.get('bbox', [0, 0, 0, 0])
    bbox2 = block2.get('bbox', [0, 0, 0, 0])

    # Gap is space between bottom of block1 and top of block2
    gap = bbox2[1] - bbox1[3]  # y0_2 - y1_1

    return max(0, gap)


def get_span_font_size(span: Dict) -> float:
    """Get font size from span."""
    return span.get('size', 0)


def fuzzy_match_text(text1: str, text2: str, threshold: float = 0.85) -> bool:
    """
    Simple fuzzy matching based on character overlap.

    Args:
        text1: First text
        text2: Second text
        threshold: Similarity threshold (0-1)

    Returns:
        True if texts are similar enough
    """
    # Normalize
    t1 = text1.lower().strip()
    t2 = text2.lower().strip()

    if not t1 or not t2:
        return False

    # Exact match
    if t1 == t2:
        return True

    # Check if one contains the other (for substring matching)
    if t1 in t2 or t2 in t1:
        return True

    # Simple character-based similarity
    # Count common characters
    chars1 = set(t1)
    chars2 = set(t2)
    common = chars1.intersection(chars2)

    similarity = len(common) / max(len(chars1), len(chars2))

    return similarity >= threshold
