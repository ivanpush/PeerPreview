"""Figure detection stage for PDF parsing pipeline.

Detects figure regions using multiple methods:
- Embedded images (get_images)
- Vector drawings (get_drawings with clustering)
- Caption-based inference (proximity matching)
- Synthetic zones (orphan captions)
"""

import pymupdf
import logging
from typing import List, Tuple, Optional, Dict
from collections import defaultdict

from ..models import FigureCaption, FigureRegion

logger = logging.getLogger(__name__)


def detect_image_regions(page: pymupdf.Page, page_num: int) -> List[FigureRegion]:
    """Detect embedded images using pymupdf.

    Filters by size to avoid small icons and decorations.

    Args:
        page: pymupdf Page object
        page_num: Page number

    Returns:
        List of FigureRegion objects from detected images
    """
    regions = []
    images = page.get_images(full=True)

    for img in images:
        try:
            xref = img[0]
            rects = page.get_image_rects(xref)

            for rect in rects:
                width = rect.width
                height = rect.height
                area = width * height

                # Filter by size (avoid small icons, decorations)
                # Min 150x100pt, 20k area (~2x1.4 inches)
                if width >= 150 and height >= 100 and area >= 20000:
                    regions.append(FigureRegion(
                        bbox=tuple(rect),
                        page=page_num,
                        detection_method='image',
                        confidence=0.9,
                        has_actual_figure=True
                    ))
        except Exception as e:
            logger.warning(f"Error detecting image on page {page_num}: {e}")
            continue

    return regions


def cluster_drawings(drawings: List, proximity_threshold: float = 20) -> List[List]:
    """Cluster nearby drawings together.

    Args:
        drawings: List of drawing dicts from get_drawings()
        proximity_threshold: Distance threshold for clustering (pt)

    Returns:
        List of drawing clusters
    """
    if not drawings:
        return []

    # Extract bounding boxes
    bboxes = []
    for drawing in drawings:
        rect = drawing.get('rect')
        if rect:
            bboxes.append((rect, drawing))

    if not bboxes:
        return []

    # Simple clustering: group drawings within proximity
    clusters = []
    used = set()

    for i, (rect1, draw1) in enumerate(bboxes):
        if i in used:
            continue

        cluster = [draw1]
        used.add(i)

        # Find nearby drawings
        for j, (rect2, draw2) in enumerate(bboxes):
            if j in used:
                continue

            # Calculate distance between rectangles
            distance = calculate_rect_distance(rect1, rect2)

            if distance <= proximity_threshold:
                cluster.append(draw2)
                used.add(j)

        clusters.append(cluster)

    return clusters


def calculate_rect_distance(rect1: pymupdf.Rect, rect2: pymupdf.Rect) -> float:
    """Calculate minimum distance between two rectangles.

    Args:
        rect1: First rectangle
        rect2: Second rectangle

    Returns:
        Minimum distance in points
    """
    # If rectangles intersect, distance is 0
    if rect1.intersects(rect2):
        return 0.0

    # Calculate distance between closest edges
    dx = max(rect1.x0 - rect2.x1, rect2.x0 - rect1.x1, 0)
    dy = max(rect1.y0 - rect2.y1, rect2.y0 - rect1.y1, 0)

    return (dx * dx + dy * dy) ** 0.5


def calculate_cluster_bbox(cluster: List) -> Tuple[float, float, float, float]:
    """Calculate bounding box encompassing all drawings in cluster.

    Args:
        cluster: List of drawing dicts

    Returns:
        Tuple (x0, y0, x1, y1)
    """
    x0 = float('inf')
    y0 = float('inf')
    x1 = float('-inf')
    y1 = float('-inf')

    for drawing in cluster:
        rect = drawing.get('rect')
        if rect:
            x0 = min(x0, rect.x0)
            y0 = min(y0, rect.y0)
            x1 = max(x1, rect.x1)
            y1 = max(y1, rect.y1)

    return (x0, y0, x1, y1)


def detect_drawing_regions(page: pymupdf.Page, page_num: int) -> List[FigureRegion]:
    """Detect vector graphics (charts, plots) using drawing clustering.

    Challenge: get_drawings() is noisy (includes lines, borders, etc.)
    Solution: Cluster nearby drawings, only keep clusters with sufficient density

    Args:
        page: pymupdf Page object
        page_num: Page number

    Returns:
        List of FigureRegion objects from detected vector drawings
    """
    drawings = page.get_drawings()

    if len(drawings) < 5:  # Too few for a real figure
        return []

    # Cluster drawings by proximity
    clusters = cluster_drawings(drawings, proximity_threshold=15)

    regions = []
    for cluster in clusters:
        # Only keep clusters with enough elements (real figures are complex)
        if len(cluster) < 5:
            continue

        # Calculate cluster bounding box
        bbox = calculate_cluster_bbox(cluster)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]

        # Filter by size (same thresholds as images)
        if width >= 150 and height >= 100:
            regions.append(FigureRegion(
                bbox=bbox,
                page=page_num,
                detection_method='drawing',
                confidence=0.7,  # Lower confidence than images
                has_actual_figure=True
            ))

    return regions


def is_horizontally_aligned(
    caption_bbox: Tuple,
    figure_bbox: Tuple,
    page_width: float,
    tolerance: float = 50
) -> bool:
    """Check if caption and figure are horizontally aligned.

    Handles both same-column and column-spanning figures.

    Args:
        caption_bbox: Caption bounding box (x0, y0, x1, y1)
        figure_bbox: Figure bounding box (x0, y0, x1, y1)
        page_width: Page width in points
        tolerance: Horizontal alignment tolerance (pt)

    Returns:
        True if aligned
    """
    # Caption coordinates
    cap_x0, cap_y0, cap_x1, cap_y1 = caption_bbox
    cap_center = (cap_x0 + cap_x1) / 2

    # Figure coordinates
    fig_x0, fig_y0, fig_x1, fig_y1 = figure_bbox
    fig_center = (fig_x0 + fig_x1) / 2
    fig_width = fig_x1 - fig_x0

    # CASE 1: Figure spans most of page (column-spanning)
    if fig_width > page_width * 0.7:
        return True

    # CASE 2: Centers are close (same column)
    if abs(cap_center - fig_center) < tolerance:
        return True

    # CASE 3: Caption left edge aligns with figure left edge
    if abs(cap_x0 - fig_x0) < tolerance:
        return True

    return False


def expand_bbox_with_margin(
    bbox: Tuple[float, float, float, float],
    top: float = 10,
    bottom: float = 30,
    left: float = 5,
    right: float = 5
) -> Tuple[float, float, float, float]:
    """Expand bounding box with margins.

    Args:
        bbox: Original bbox (x0, y0, x1, y1)
        top, bottom, left, right: Margins to add (pt)

    Returns:
        Expanded bbox
    """
    x0, y0, x1, y1 = bbox
    return (
        x0 - left,
        y0 - top,
        x1 + right,
        y1 + bottom
    )


def clip_bbox_to_page(
    bbox: Tuple[float, float, float, float],
    page_bbox: pymupdf.Rect
) -> Tuple[float, float, float, float]:
    """Clip bounding box to page boundaries.

    Args:
        bbox: Bbox to clip (x0, y0, x1, y1)
        page_bbox: Page rectangle

    Returns:
        Clipped bbox
    """
    x0, y0, x1, y1 = bbox
    return (
        max(x0, page_bbox.x0),
        max(y0, page_bbox.y0),
        min(x1, page_bbox.x1),
        min(y1, page_bbox.y1)
    )


def pair_captions_with_figures(
    captions: List[FigureCaption],
    detected_figures: List[FigureRegion],
    page: pymupdf.Page
) -> List[FigureRegion]:
    """Pair captions with nearby detected figures.

    Spatial relationships:
    - Figure usually ABOVE caption (most common)
    - Sometimes BELOW (less common)
    - Proximity threshold: ±100pt vertically
    - Horizontal alignment: same column or spanning

    Args:
        captions: List of FigureCaption objects for this page
        detected_figures: List of detected FigureRegion objects
        page: pymupdf Page object

    Returns:
        List of FigureRegion objects with captions paired
    """
    paired_regions = []
    used_figures = set()
    page_width = page.rect.width

    for caption in captions:
        caption_y = caption.y_position
        caption_bbox = caption.bbox

        # Find closest figure within proximity
        best_match = None
        best_distance = float('inf')

        for idx, figure in enumerate(detected_figures):
            if idx in used_figures:
                continue

            # Calculate vertical distance
            figure_y = figure.bbox[1]  # top of figure
            distance = abs(figure_y - caption_y)

            # Check proximity (±100pt)
            if distance > 100:
                continue

            # Check horizontal alignment
            if not is_horizontally_aligned(caption_bbox, figure.bbox, page_width):
                continue

            if distance < best_distance:
                best_distance = distance
                best_match = (idx, figure)

        if best_match:
            idx, figure = best_match
            used_figures.add(idx)

            # Create region with expanded exclusion zone
            expanded_bbox = expand_bbox_with_margin(
                figure.bbox,
                top=10, bottom=30, left=5, right=5
            )

            paired_regions.append(FigureRegion(
                bbox=expanded_bbox,
                page=figure.page,
                detection_method=figure.detection_method,
                confidence=figure.confidence,
                has_actual_figure=True,
                associated_caption=caption,
                exclusion_margin=(10, 30, 5, 5)
            ))

    return paired_regions


def handle_orphan_captions(
    captions: List[FigureCaption],
    paired_regions: List[FigureRegion],
    page: pymupdf.Page,
    page_num: int
) -> List[FigureRegion]:
    """Create synthetic exclusion zones for captions without paired figures.

    These could be:
    - Pure vector figures (get_drawings didn't detect)
    - Tables (just formatted text)
    - Figures that span columns in weird ways

    Strategy: Assume figure is ABOVE caption (most common)

    Args:
        captions: List of all captions for this page
        paired_regions: List of already-paired regions
        page: pymupdf Page object
        page_num: Page number

    Returns:
        List of synthetic FigureRegion objects
    """
    # Get IDs of paired captions (use text + page as unique identifier)
    paired_caption_ids = {(r.associated_caption.text, r.associated_caption.page)
                          for r in paired_regions if r.associated_caption}

    orphan_captions = [c for c in captions if (c.text, c.page) not in paired_caption_ids]

    synthetic_regions = []

    for caption in orphan_captions:
        caption_bbox = caption.bbox

        # Create synthetic bbox above caption
        # Assume reasonable figure size: match caption width, 150pt tall
        synthetic_bbox = (
            caption_bbox[0],           # x0: same left edge as caption
            caption_bbox[1] - 160,     # y0: 150pt figure + 10pt gap
            caption_bbox[2],           # x1: same right edge as caption
            caption_bbox[1] - 10       # y1: 10pt gap before caption
        )

        # Validate bbox (don't go off page)
        synthetic_bbox = clip_bbox_to_page(synthetic_bbox, page.rect)

        synthetic_regions.append(FigureRegion(
            bbox=synthetic_bbox,
            page=page_num,
            detection_method='caption_inferred',
            confidence=0.5,  # Lower confidence for synthetic
            has_actual_figure=False,
            associated_caption=caption,
            exclusion_margin=(10, 30, 5, 5)
        ))

    if synthetic_regions:
        logger.info(f"Created {len(synthetic_regions)} synthetic regions for orphan captions on page {page_num}")

    return synthetic_regions


def detect_figure_regions(
    doc: pymupdf.Document,
    captions: List[FigureCaption],
    config
) -> List[FigureRegion]:
    """Detect figure regions using multiple methods.

    Methods:
    1. Embedded images (get_images)
    2. Vector drawings (get_drawings with clustering)
    3. Caption-based inference (proximity matching)
    4. Synthetic zones (orphan captions)

    Args:
        doc: pymupdf Document (after geometric cleaning)
        captions: List of detected FigureCaption objects
        config: Pipeline configuration

    Returns:
        List of FigureRegion objects
    """
    logger.info("Detecting figure regions")
    all_regions = []

    for page_num, page in enumerate(doc):
        page_captions = [c for c in captions if c.page == page_num]

        if not page_captions:
            # No captions on this page, skip figure detection
            continue

        # Method 1: Find embedded images
        image_regions = detect_image_regions(page, page_num)
        logger.debug(f"Page {page_num}: detected {len(image_regions)} images")

        # Method 2: Find vector drawings (charts, plots)
        drawing_regions = detect_drawing_regions(page, page_num)
        logger.debug(f"Page {page_num}: detected {len(drawing_regions)} drawing clusters")

        # Combine detected figures
        detected_figures = image_regions + drawing_regions

        # Method 3: Pair captions with detected figures
        paired_regions = pair_captions_with_figures(
            page_captions,
            detected_figures,
            page
        )
        logger.debug(f"Page {page_num}: paired {len(paired_regions)} captions with figures")

        # Method 4: Handle orphan captions (no paired figure)
        orphan_regions = handle_orphan_captions(
            page_captions,
            paired_regions,
            page,
            page_num
        )

        all_regions.extend(paired_regions + orphan_regions)

    logger.info(f"Detected {len(all_regions)} figure regions total ({sum(1 for r in all_regions if r.has_actual_figure)} with actual figures, {sum(1 for r in all_regions if not r.has_actual_figure)} synthetic)")
    return all_regions
