"""Simple caption-based figure detection.

Strategy:
1. For each caption, determine if full-width or column-width
2. Look ABOVE caption until hitting a real paragraph
3. Delete everything in that vertical region
4. Also delete text close to image/vector clusters (proximity-based)
"""

import pymupdf
import logging
from typing import List, Tuple, Optional
from ..models import FigureCaption, FigureRegion

logger = logging.getLogger(__name__)


def detect_figure_regions(
    doc: pymupdf.Document,
    captions: List[FigureCaption],
    config
) -> List[FigureRegion]:
    """
    Detect figure regions using two methods:
    1. Caption-based vertical deletion (primary)
    2. Proximity-based clusters of images/drawings (secondary)

    Args:
        doc: pymupdf Document (after geometric cleaning)
        captions: List of detected FigureCaption objects
        config: Pipeline configuration

    Returns:
        List of FigureRegion objects
    """
    logger.info(f"Detecting figure regions for {len(captions)} captions using vertical deletion + clusters")
    all_regions = []

    # Method 1: Caption-based vertical deletion
    for caption in captions:
        page = doc[caption.page]
        region = create_vertical_deletion_region(caption, page)
        if region:
            all_regions.append(region)

    # Method 2: Detect image/vector clusters for proximity filtering
    for page_num, page in enumerate(doc):
        cluster_regions = detect_image_vector_clusters(page, page_num)
        all_regions.extend(cluster_regions)

    logger.info(f"Created {len(all_regions)} figure regions total")
    return all_regions


def create_vertical_deletion_region(
    caption: FigureCaption,
    page: pymupdf.Page
) -> Optional[FigureRegion]:
    """
    Create figure region by vertical deletion above caption.

    Algorithm:
    1. Start at caption top
    2. Look ABOVE for text blocks
    3. Find first REAL paragraph (>50 chars, >10 words, has period)
    4. Delete everything between paragraph bottom and caption top
    5. Use caption's horizontal bounds (left/right)

    Args:
        caption: FigureCaption object
        page: pymupdf Page object

    Returns:
        FigureRegion or None
    """
    caption_bbox = caption.bbox
    caption_y_top = caption_bbox[1]  # Top of caption
    caption_left = caption_bbox[0]
    caption_right = caption_bbox[2]

    page_width = page.rect.width
    page_height = page.rect.height

    # Get all text blocks on page
    text_dict = page.get_text("dict")
    blocks = text_dict.get("blocks", [])
    text_blocks = [b for b in blocks if b.get("type") == 0]

    # Find blocks ABOVE caption
    blocks_above = []
    for block in text_blocks:
        bbox = block.get("bbox")
        if not bbox:
            continue

        block_bottom = bbox[3]

        # Only consider blocks that end above caption (with 10pt gap)
        if block_bottom < caption_y_top - 10:
            blocks_above.append(block)

    if not blocks_above:
        # No text above - use conservative 200pt region
        top_edge = max(0, caption_y_top - 200)
        logger.debug(f"No text above caption on page {caption.page}, using 200pt default")
    else:
        # Sort blocks by y-position (closest to caption first)
        blocks_above.sort(key=lambda b: b["bbox"][3], reverse=True)

        # Find first REAL paragraph
        paragraph_bottom = None

        for block in blocks_above:
            text = extract_text_from_block(block)
            bbox = block["bbox"]
            block_bottom = bbox[3]

            # Check if this is a REAL paragraph:
            # - More than 80 chars (raised from 50 to skip short labels)
            # - More than 15 words (raised from 10 to ensure substantial content)
            # - Has sentence ending somewhere in last 10 chars (handles superscripts)

            text_stripped = text.strip()
            word_count = len(text_stripped.split())

            if len(text_stripped) > 80 and word_count > 15:
                # Real paragraphs have multiple sentences (at least 2 periods)
                # OR end with common sentence endings
                period_count = text_stripped.count('.') + text_stripped.count('!') + text_stripped.count('?')

                # Check last 20 chars for sentence ending (handles references like "text37.")
                last_chars = text_stripped[-20:] if len(text_stripped) >= 20 else text_stripped
                ends_with_punctuation = ('.' in last_chars or '!' in last_chars or '?' in last_chars)

                # Paragraph if: has 2+ sentences OR ends with punctuation
                if period_count >= 2 or ends_with_punctuation:
                    # This is a real paragraph
                    paragraph_bottom = block_bottom
                    logger.debug(f"Found paragraph end at y={block_bottom} (periods={period_count}): '{text_stripped[:60]}...'")
                    break

        if paragraph_bottom is not None:
            # Use paragraph bottom + 10pt gap
            top_edge = paragraph_bottom + 10
        else:
            # No clear paragraph - use 300pt default (larger for figures)
            top_edge = max(0, caption_y_top - 300)
            logger.debug(f"No paragraph found, using 300pt region on page {caption.page}")

    # Determine horizontal bounds based on caption width
    # If caption is >70% of page width, it's full-width
    caption_width = caption_right - caption_left
    is_full_width = (caption_width / page_width) > 0.7

    if is_full_width:
        # Full-width figure - use most of page width
        left_edge = 30  # Leave small margin
        right_edge = page_width - 30
        logger.debug(f"Full-width caption on page {caption.page}")
    else:
        # Column-width figure - use caption bounds + small margin
        left_edge = max(20, caption_left - 20)
        right_edge = min(page_width - 20, caption_right + 20)
        logger.debug(f"Column-width caption on page {caption.page}")

    # Final bbox
    final_bbox = (
        left_edge,
        top_edge,
        right_edge,
        caption_y_top - 10  # 10pt gap above caption
    )

    # Validate
    width = final_bbox[2] - final_bbox[0]
    height = final_bbox[3] - final_bbox[1]

    if height < 20:
        logger.warning(f"Figure region too short ({height}pt), skipping")
        return None

    if width < 50:
        logger.warning(f"Figure region too narrow ({width}pt), skipping")
        return None

    return FigureRegion(
        bbox=final_bbox,
        page=caption.page,
        detection_method='vertical_deletion',
        confidence=0.9,
        has_actual_figure=True,
        associated_caption=caption,
        exclusion_margin=(0, 0, 0, 0)  # No expansion - region is precise
    )


def extract_text_from_block(block: dict) -> str:
    """Extract all text from a pymupdf block."""
    text_parts = []

    lines = block.get("lines", [])
    for line in lines:
        spans = line.get("spans", [])
        for span in spans:
            span_text = span.get("text", "")
            if span_text:
                text_parts.append(span_text)

    return " ".join(text_parts)


def detect_image_vector_clusters(
    page: pymupdf.Page,
    page_num: int
) -> List[FigureRegion]:
    """
    Detect clusters of images and vector drawings for proximity-based filtering.

    Filters out truly tiny elements, merges nearby elements into clusters.

    Args:
        page: pymupdf Page object
        page_num: Page number (0-indexed)

    Returns:
        List of FigureRegion objects for clusters
    """
    regions = []

    # Collect image bboxes (filter tiny ones)
    MIN_SIZE = 20  # Filter elements < 20pt width/height
    image_bboxes = []

    for info in page.get_images(full=True):
        xref = info[0]
        try:
            for rect in page.get_image_rects(xref):
                w = rect.x1 - rect.x0
                h = rect.y1 - rect.y0
                if w >= MIN_SIZE and h >= MIN_SIZE:
                    image_bboxes.append((rect.x0, rect.y0, rect.x1, rect.y1))
        except:
            continue

    # Collect vector drawing bboxes (filter tiny ones)
    drawing_bboxes = []
    try:
        drawings = page.get_drawings()
        for drawing in drawings:
            rect = drawing.get("rect")
            if rect:
                w = rect.x1 - rect.x0
                h = rect.y1 - rect.y0
                if w >= MIN_SIZE and h >= MIN_SIZE:
                    drawing_bboxes.append((rect.x0, rect.y0, rect.x1, rect.y1))
    except:
        pass

    # Merge all bboxes
    all_bboxes = image_bboxes + drawing_bboxes

    if not all_bboxes:
        return []

    # Merge nearby bboxes into clusters (20pt proximity)
    merged = merge_nearby_bboxes(all_bboxes, proximity=20)

    # Create FigureRegion for each cluster with small margins
    for bbox in merged:
        # Only keep clusters that are substantial (>50pt in both dimensions)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]

        if w >= 50 and h >= 50:
            # Add small margins for proximity filtering (10pt)
            expanded = (
                max(0, bbox[0] - 10),
                max(0, bbox[1] - 10),
                bbox[2] + 10,
                bbox[3] + 10
            )

            regions.append(FigureRegion(
                bbox=expanded,
                page=page_num,
                detection_method='cluster',
                confidence=0.7,
                has_actual_figure=True,
                associated_caption=None,
                exclusion_margin=(0, 0, 0, 0)
            ))

    logger.debug(f"Page {page_num}: found {len(regions)} image/vector clusters")
    return regions


def merge_nearby_bboxes(
    bboxes: List[Tuple[float, float, float, float]],
    proximity: float
) -> List[Tuple[float, float, float, float]]:
    """
    Merge bboxes that are within proximity distance of each other.

    Args:
        bboxes: List of bboxes (x0, y0, x1, y1)
        proximity: Merge distance threshold in points

    Returns:
        List of merged bboxes
    """
    if not bboxes:
        return []

    # Sort by y0 for efficient processing
    sorted_boxes = sorted(bboxes, key=lambda b: b[1])

    merged = []
    current_group = [sorted_boxes[0]]

    for bbox in sorted_boxes[1:]:
        # Check if bbox is near any bbox in current group
        is_near = False

        for group_bbox in current_group:
            if boxes_are_near(bbox, group_bbox, proximity):
                is_near = True
                break

        if is_near:
            current_group.append(bbox)
        else:
            # Finalize current group
            merged.append(merge_bbox_group(current_group))
            current_group = [bbox]

    # Don't forget last group
    if current_group:
        merged.append(merge_bbox_group(current_group))

    return merged


def boxes_are_near(
    bbox1: Tuple[float, float, float, float],
    bbox2: Tuple[float, float, float, float],
    proximity: float
) -> bool:
    """Check if two bboxes are within proximity distance."""
    x0_1, y0_1, x1_1, y1_1 = bbox1
    x0_2, y0_2, x1_2, y1_2 = bbox2

    # Check horizontal proximity
    h_gap = max(0, max(x0_1, x0_2) - min(x1_1, x1_2))
    # Check vertical proximity
    v_gap = max(0, max(y0_1, y0_2) - min(y1_1, y1_2))

    return h_gap <= proximity and v_gap <= proximity


def merge_bbox_group(
    bboxes: List[Tuple[float, float, float, float]]
) -> Tuple[float, float, float, float]:
    """Merge a group of bboxes into unified bbox."""
    x0 = min(b[0] for b in bboxes)
    y0 = min(b[1] for b in bboxes)
    x1 = max(b[2] for b in bboxes)
    y1 = max(b[3] for b in bboxes)

    return (x0, y0, x1, y1)
