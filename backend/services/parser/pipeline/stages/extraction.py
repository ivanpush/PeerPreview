"""
PDF text extraction using pymupdf4llm for robust column handling.

pymupdf4llm handles:
- Automatic column detection and proper reading order
- Figure detection and caption extraction
- Text formatting and spacing
- Image text filtering
"""

import pymupdf
import pymupdf4llm
from typing import List, Tuple, Optional
import logging

from ..models import FigureCaption, FigureRegion, GeometryInfo, StructureInfo

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# ============================================================
#  FIGURE HANDLING
# ============================================================

def get_all_image_regions(page: pymupdf.Page) -> List[Tuple[float, float, float, float]]:
    """Get ALL image regions on page, for text filtering purposes.

    For now, just return empty - we're NOT filtering text based on images.
    Figure labels/captions will be handled by later cleanup stages.
    """
    # Disabled - causes too many false positives
    return []


def get_true_figures(page: pymupdf.Page) -> List[Tuple[float, float, float, float, int]]:
    """Return main figure bboxes for placeholder insertion.

    Academic papers typically have 3-8 main figures. We filter aggressively to avoid
    detecting every small chart/table element as a separate figure placeholder.
    """
    figs = []
    # Stricter thresholds to only capture main figures for [FIGURE:n] placeholders
    MIN_W = 150        # Minimum 150pt width (~2 inches)
    MIN_H = 100        # Minimum 100pt height (~1.4 inches)
    MIN_AREA = 20000   # Minimum 20k square points (e.g., 200x100pt)

    for info in page.get_images(full=True):
        xref = info[0]
        try:
            for rect in page.get_image_rects(xref):
                w = rect.x1 - rect.x0
                h = rect.y1 - rect.y0
                area = w * h
                if w >= MIN_W and h >= MIN_H and area >= MIN_AREA:
                    figs.append((rect.x0, rect.y0, rect.x1, rect.y1, xref))
        except:
            continue

    return figs


def text_overlaps_figure(bbox, image_regions, thresh=0.05) -> bool:
    """Check if text block overlaps with any image region.

    Args:
        bbox: Text block bbox (x0, y0, x1, y1)
        image_regions: List of image bboxes (x0, y0, x1, y1)
        thresh: Overlap threshold (5% of text area - very permissive to catch labels)

    Returns:
        True if text overlaps significantly with any image
    """
    tx0, ty0, tx1, ty1 = bbox
    text_area = (tx1 - tx0) * (ty1 - ty0)
    if text_area <= 0:
        return False

    for fx0, fy0, fx1, fy1 in image_regions:
        ix0 = max(tx0, fx0)
        iy0 = max(ty0, fy0)
        ix1 = min(tx1, fx1)
        iy1 = min(ty1, fy1)

        if ix1 > ix0 and iy1 > iy0:
            inter = (ix1 - ix0) * (iy1 - iy0)
            # Very low threshold (5%) with expanded regions to catch text labels
            if inter / text_area > thresh:
                return True

    return False


# ============================================================
#  COLUMN DETECTION (K-MEANS)
# ============================================================

def detect_columns(blocks: List[dict]) -> Tuple[int, Optional[float]]:
    """Detect 1 or 2 columns using simple median-based clustering."""
    if not blocks:
        return 1, None

    centers = []
    for b in blocks:
        x0, y0, x1, y1 = b["bbox"]
        if (x1 - x0) > 40 and (y1 - y0) > 5:
            centers.append((x0 + x1) / 2)

    # Need at least 4 blocks to reliably detect 2 columns
    if len(centers) < 4:
        return 1, None

    # Simple approach: split by median, compute cluster centers
    sorted_centers = sorted(centers)
    median = sorted_centers[len(sorted_centers) // 2]

    left_vals = [c for c in centers if c < median]
    right_vals = [c for c in centers if c >= median]

    if not left_vals or not right_vals:
        return 1, None

    left_c = sum(left_vals) / len(left_vals)
    right_c = sum(right_vals) / len(right_vals)

    # If centers close → single column
    # Use 80pt threshold - typical column gap in academic papers is 100-200pt
    if abs(right_c - left_c) < 80:
        return 1, None

    divider = (left_c + right_c) / 2
    return 2, divider


# ============================================================
#  TEXT EXTRACTION
# ============================================================

def extract_text_from_block(block: dict) -> str:
    """Extract clean text from a text block with correct spacing."""
    lines = []
    for line in block.get("lines", []):
        spans = line.get("spans", [])
        buf = []
        for sp in spans:
            t = sp.get("text", "")
            if not t:
                continue
            if buf and needs_space(buf[-1], t):
                buf.append(" ")
            buf.append(t)
        if buf:
            lines.append("".join(buf))
    return "\n".join(lines)


def needs_space(a: str, b: str) -> bool:
    """Decide if we need to insert a space between spans."""
    if not a:
        return False
    if a[-1].isspace():
        return False
    if b[0].isspace():
        return False
    if a.endswith("-"):
        return False
    return True


# ============================================================
#  SMART FIGURE-AWARE TEXT FILTERING
# ============================================================

def calculate_overlap_ratio(bbox1: Tuple, bbox2: Tuple) -> float:
    """Calculate overlap ratio of bbox1 with bbox2.

    Args:
        bbox1: First bbox (x0, y0, x1, y1)
        bbox2: Second bbox (x0, y0, x1, y1)

    Returns:
        Ratio of overlap (overlap_area / bbox1_area), 0.0 to 1.0
    """
    # Calculate intersection
    x0 = max(bbox1[0], bbox2[0])
    y0 = max(bbox1[1], bbox2[1])
    x1 = min(bbox1[2], bbox2[2])
    y1 = min(bbox1[3], bbox2[3])

    # No overlap
    if x1 < x0 or y1 < y0:
        return 0.0

    intersection = (x1 - x0) * (y1 - y0)
    bbox1_area = (bbox1[2] - bbox1[0]) * (bbox1[3] - bbox1[1])

    return intersection / bbox1_area if bbox1_area > 0 else 0.0


def extract_block_text_simple(block: dict) -> str:
    """Extract all text from a text block (simple version).

    Args:
        block: Text block dict from pymupdf

    Returns:
        Concatenated text from all lines/spans
    """
    texts = []
    for line in block.get("lines", []):
        for span in line.get("spans", []):
            text = span.get("text", "")
            if text:
                texts.append(text)
    return "".join(texts)


def is_caption_block(
    block_bbox: Tuple[float, float, float, float],
    block_text: str,
    captions: List[FigureCaption]
) -> bool:
    """Check if text block matches a detected caption.

    Uses bbox comparison (most reliable) with text fallback.

    Args:
        block_bbox: Block bounding box (x0, y0, x1, y1)
        block_text: Block text content
        captions: List of detected FigureCaption objects

    Returns:
        True if block is a caption
    """
    for caption in captions:
        # Primary: bbox overlap (≥80% overlap = same block)
        overlap = calculate_overlap_ratio(block_bbox, caption.bbox)
        if overlap > 0.8:
            return True

        # Fallback: text comparison (first 20 chars)
        if len(caption.text) >= 20 and len(block_text) >= 20:
            if caption.text[:20] in block_text or block_text[:20] in caption.text:
                return True

    return False


def should_filter_text(
    block: dict,
    figure_regions: List[FigureRegion],
    captions: List[FigureCaption]
) -> bool:
    """Determine if text block should be filtered (removed).

    Rules:
    1. NEVER filter caption text (preserve it)
    2. Use variable overlap thresholds:
       - Small text (<20pt tall): 50% overlap → filter (likely labels)
       - Body text (≥20pt tall): 30% overlap → filter

    Args:
        block: Text block dict from pymupdf
        figure_regions: List of FigureRegion objects for this page
        captions: List of FigureCaption objects for this page

    Returns:
        True if block should be filtered
    """
    if block.get("type") != 0:  # Not a text block
        return False

    block_bbox = tuple(block.get("bbox", [0, 0, 0, 0]))
    block_text = extract_block_text_simple(block).strip()
    block_height = block_bbox[3] - block_bbox[1]

    # Rule 1: NEVER filter captions
    if is_caption_block(block_bbox, block_text, captions):
        return False

    # Rule 2: Check overlap with figure regions
    for figure_region in figure_regions:
        overlap_ratio = calculate_overlap_ratio(block_bbox, figure_region.bbox)

        # Determine threshold based on text size
        # Small text (labels, axis numbers): 50% threshold
        # Body text: 30% threshold
        threshold = 0.5 if block_height < 20 else 0.3

        if overlap_ratio > threshold:
            return True  # Filter this block

    return False  # Don't filter


def filter_figure_text_from_page(
    page: pymupdf.Page,
    figure_regions: List[FigureRegion],
    captions: List[FigureCaption]
):
    """Filter text blocks overlapping with figure regions.

    Applies redactions to text that should be filtered.

    Args:
        page: pymupdf Page object
        figure_regions: List of FigureRegion objects for this page
        captions: List of FigureCaption objects for this page
    """
    if not figure_regions:
        return  # No figures to filter

    blocks = page.get_text("dict")["blocks"]
    redactions_applied = 0

    for block in blocks:
        if should_filter_text(block, figure_regions, captions):
            # Mark block for redaction
            bbox = pymupdf.Rect(block["bbox"])
            page.add_redact_annot(bbox)
            redactions_applied += 1

    # Apply all redactions
    if redactions_applied > 0:
        page.apply_redactions()
        logger.debug(f"Filtered {redactions_applied} text blocks from page")


# ============================================================
#  MAIN EXTRACTION FUNCTION
# ============================================================

def extract_markdown(
    doc: pymupdf.Document,
    geom_info: GeometryInfo = None,
    structure_info: StructureInfo = None
) -> str:
    """Extract markdown from PDF using pymupdf4llm with figure-aware filtering.

    Uses detected figure regions and captions to filter text while preserving
    caption content.

    Args:
        doc: pymupdf Document (after geometric cleaning)
        geom_info: Optional GeometryInfo with figure regions
        structure_info: Optional StructureInfo with caption list

    Returns:
        Markdown text with proper column handling and figure filtering
    """
    logger.info(f"Extracting markdown from {len(doc)} pages using pymupdf4llm")

    # Smart filtering if we have figure data
    if geom_info and structure_info:
        for page_num, page in enumerate(doc):
            page_figure_regions = [f for f in geom_info.figure_regions if f.page == page_num]
            page_captions = [c for c in structure_info.figure_captions if c.page == page_num]

            if page_figure_regions:
                filter_figure_text_from_page(page, page_figure_regions, page_captions)

    # Extract with pymupdf4llm (existing code works great)
    markdown = pymupdf4llm.to_markdown(doc)

    logger.info(f"Extracted {len(markdown)} characters total")
    return markdown


# ============================================================
#  TWO-COLUMN SORTING
# ============================================================

def sort_two_column(items, divider_x):
    """Sort items in two-column reading order.

    For academic papers with two columns, the standard reading order is:
    1. Spanning elements (wide titles/headings) at top
    2. ENTIRE left column top-to-bottom
    3. ENTIRE right column top-to-bottom

    This is the conventional reading order for academic papers.
    """
    left = []
    right = []
    spanning = []

    for (typ, y, payload, bbox) in items:
        x0, y0, x1, y1 = bbox
        cx = (x0 + x1) / 2
        w = x1 - x0

        # If it spans wide across both columns (titles, headings)
        if w > 300 and x0 < divider_x - 20 and x1 > divider_x + 20:
            spanning.append((typ, y, payload, bbox))
            continue

        if cx < divider_x:
            left.append((typ, y, payload, bbox))
        else:
            right.append((typ, y, payload, bbox))

    # Sort each by vertical position (y), with x as secondary sort for same-height items
    spanning.sort(key=lambda item: (item[1], item[3][0]))  # (y, x0)
    left.sort(key=lambda item: (item[1], item[3][0]))      # (y, x0)
    right.sort(key=lambda item: (item[1], item[3][0]))     # (y, x0)

    # Standard reading order: spanning, then ALL of left, then ALL of right
    return spanning + left + right


# ============================================================
#  CLI TEST
# ============================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python pdf_extractor.py <file.pdf>")
        sys.exit(1)

    path = sys.argv[1]
    doc = pymupdf.open(path)
    md = extract_markdown(doc)
    print(md[:3000])
    print("... truncated ...")
    doc.close()
