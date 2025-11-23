# Figure Detection & Text Filtering Implementation Plan

## Problem Statement

Current redaction in `extraction.py` (lines 180-209) doesn't prevent figure garbage from appearing in output:
- Axis labels (scattered "a b c d", "0 5 10 15 20")
- Text fragments from within figures
- Figure-related artifacts mixed with body text

We need comprehensive figure detection and smart text filtering.

## Solution Overview

Multi-stage approach that detects figures through multiple methods and intelligently filters text while preserving captions and body content.

## Implementation Phases

### Phase 1: Update Data Models

**File:** `backend/services/parser/pipeline/models.py`

Add new dataclasses:

```python
@dataclass
class FigureCaption:
    """Detected figure caption with spatial metadata."""
    text: str                    # Full caption text
    figure_type: str            # 'Figure', 'Fig', 'Table', 'Scheme'
    figure_num: str             # '1', '2A', 'S3', etc.
    page: int                   # Page number
    bbox: Tuple[float, float, float, float]  # Bounding box
    y_position: float           # Vertical position for proximity matching
    is_bold: bool              # Whether caption is bold
    confidence: float          # Detection confidence (0-1)
    is_standalone: bool        # True if caption is on its own line

@dataclass
class FigureRegion:
    """Detected or inferred figure region for exclusion."""
    bbox: Tuple[float, float, float, float]  # Exclusion zone
    page: int                   # Page number
    detection_method: str       # 'image', 'drawing', 'caption_inferred', 'synthetic'
    confidence: float          # Detection confidence (0-1)
    has_actual_figure: bool    # True if real image/drawing found
    associated_caption: Optional[FigureCaption] = None
    exclusion_margin: Tuple[float, float, float, float] = (10, 30, 5, 5)  # top, bottom, left, right
```

Update existing models:

```python
@dataclass
class StructureInfo:
    # ... existing fields ...
    figure_captions: List[FigureCaption] = field(default_factory=list)  # NEW

@dataclass
class GeometryInfo:
    # ... existing fields ...
    figure_regions: List[FigureRegion] = field(default_factory=list)  # NEW
```

---

### Phase 2: Caption Detection (Stage 2)

**File:** `backend/services/parser/pipeline/stages/analysis.py`

Add robust caption detection to existing structure analysis:

#### Key Functions to Add:

```python
def detect_captions(doc: pymupdf.Document) -> List[FigureCaption]:
    """
    Detect figure captions with robust pattern matching.

    Handles:
    - Figure/Fig/Table/Scheme variations
    - Case-insensitive matching
    - Unicode spaces (non-breaking, etc.)
    - Subfigures (1A, 2B-D)
    - Supplementary figures (S1, Supplementary Figure 1)
    """
    captions = []

    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            caption = detect_caption_in_block(block, page_num)
            if caption:
                captions.append(caption)

    return captions

def detect_caption_in_block(block: dict, page_num: int) -> Optional[FigureCaption]:
    """
    Check if block contains a standalone caption.

    Returns None if:
    - No caption pattern found
    - Caption is inline (e.g., "as shown in Figure 1")
    - Not at start of line/block
    """
    text = extract_block_text(block).strip()

    # Normalize text (handle unicode, ligatures)
    normalized = normalize_text_for_caption_check(text)

    # Try caption patterns
    match = match_caption_pattern(normalized)
    if not match:
        return None

    # Check if standalone (not inline reference)
    if not is_standalone_caption(block, text):
        return None

    # Extract metadata
    return FigureCaption(
        text=text,
        figure_type=match['type'],
        figure_num=match['number'],
        page=page_num,
        bbox=tuple(block['bbox']),
        y_position=block['bbox'][1],  # top y coordinate
        is_bold=check_if_bold(block),
        confidence=calculate_caption_confidence(match, block),
        is_standalone=True
    )
```

#### Caption Patterns:

```python
CAPTION_PATTERNS = [
    # Standard: "Figure 1", "Fig. 1", case-insensitive
    r'^(?i)(Figure|Fig\.?)\s+(\d+)([A-Za-z]?)(?:[.:]|\s)',

    # Handle unicode spaces (\xa0, etc.)
    r'^(?i)(Figure|Fig\.?)\p{Z}+(\d+)([A-Za-z]?)(?:[.:]|\p{Z})',

    # Tables, Schemes, Charts
    r'^(?i)(Table|Scheme|Chart)\s+(\d+)(?:[.:]|\s)',

    # Supplementary: "Figure S1", "Supplementary Figure 1"
    r'^(?i)(Supplementary\s+)?(Figure|Fig\.?|Table)\s*([S]?\d+)',

    # Bold with separate punctuation: **Figure 1** .
    r'^(?i)\*\*(Figure|Fig\.?)\s+(\d+)\*\*\s*[.:]',
]
```

#### Standalone vs Inline Detection:

```python
def is_standalone_caption(block: dict, text: str) -> bool:
    """
    Distinguish standalone captions from inline references.

    Standalone: "Figure 1: Distribution of..." (own line/paragraph)
    Inline: "as shown in Figure 1, the results..." (embedded in sentence)
    """
    lines = block.get("lines", [])

    for line_idx, line in enumerate(lines):
        spans = line.get("spans", [])

        for span_idx, span in enumerate(spans):
            span_text = span.get("text", "").strip()

            # Caption pattern found
            if not match_caption_pattern(span_text):
                continue

            # CASE 1: First span in line = standalone
            if span_idx == 0:
                # Must have descriptive text following (>10 chars)
                remaining = get_remaining_line_text(line, span_idx)
                next_line = get_next_line_text(lines, line_idx)
                if len(remaining + next_line) > 10:
                    return True

            # CASE 2: Not first span - check what comes before
            else:
                prev_text = get_previous_spans_text(spans, span_idx)

                # Substantial text before = inline reference
                if len(prev_text.strip()) > 5:
                    return False

                # Only whitespace/punctuation before = standalone
                if prev_text.strip() in ['', '.', ',', ';', ':']:
                    return True

    return False
```

#### Integration:

```python
def analyze_structure(doc: pymupdf.Document, config) -> StructureInfo:
    """Extract structure including figure captions."""
    logger.info("Analyzing document structure")

    # Existing detection
    bold_spans = extract_bold_spans(doc)
    title = detect_title(bold_spans, doc)
    abstract = detect_abstract(doc, bold_spans)
    section_headers = detect_section_headers(bold_spans)

    # NEW: Detect captions
    figure_captions = detect_captions(doc)
    logger.info(f"Detected {len(figure_captions)} figure captions")

    return StructureInfo(
        title=title,
        abstract=abstract,
        section_headers=section_headers,
        bold_spans=bold_spans,
        figure_captions=figure_captions  # NEW
    )
```

---

### Phase 3: Figure Detection (Stage 3)

**New File:** `backend/services/parser/pipeline/stages/figures.py`

Create comprehensive figure detection module.

#### Main Function:

```python
def detect_figure_regions(
    doc: pymupdf.Document,
    captions: List[FigureCaption],
    config
) -> List[FigureRegion]:
    """
    Detect figure regions using multiple methods.

    Methods:
    1. Embedded images (get_images)
    2. Vector drawings (get_drawings with clustering)
    3. Caption-based inference (proximity matching)
    4. Synthetic zones (orphan captions)
    """
    logger.info("Detecting figure regions")
    regions = []

    for page_num, page in enumerate(doc):
        page_captions = [c for c in captions if c.page == page_num]

        # Method 1: Find embedded images
        image_regions = detect_image_regions(page, page_num)

        # Method 2: Find vector drawings (charts, plots)
        drawing_regions = detect_drawing_regions(page, page_num)

        # Method 3: Pair captions with detected figures
        paired_regions = pair_captions_with_figures(
            page_captions,
            image_regions + drawing_regions,
            page
        )

        # Method 4: Handle orphan captions (no paired figure)
        orphan_regions = handle_orphan_captions(
            page_captions,
            paired_regions,
            page,
            page_num
        )

        regions.extend(paired_regions + orphan_regions)

    logger.info(f"Detected {len(regions)} figure regions total")
    return regions
```

#### Image Detection:

```python
def detect_image_regions(page: pymupdf.Page, page_num: int) -> List[FigureRegion]:
    """Detect embedded images using pymupdf."""
    regions = []
    images = page.get_images(full=True)

    for img in images:
        try:
            xref = img[0]
            rects = page.get_image_rects(xref)

            for rect in rects:
                # Filter by size (avoid small icons, decorations)
                width = rect.width
                height = rect.height
                area = width * height

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
```

#### Vector Drawing Detection:

```python
def detect_drawing_regions(page: pymupdf.Page, page_num: int) -> List[FigureRegion]:
    """
    Detect vector graphics (charts, plots) using drawing clustering.

    Challenge: get_drawings() is noisy (includes lines, borders, etc.)
    Solution: Cluster nearby drawings, only keep clusters with sufficient density
    """
    drawings = page.get_drawings()

    if len(drawings) < 5:  # Too few for a real figure
        return []

    # Cluster drawings by proximity
    clusters = cluster_drawings(drawings, proximity_threshold=20)

    regions = []
    for cluster in clusters:
        # Only keep clusters with enough elements
        if len(cluster) < 5:
            continue

        # Calculate cluster bounding box
        bbox = calculate_cluster_bbox(cluster)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]

        # Filter by size
        if width >= 150 and height >= 100:
            regions.append(FigureRegion(
                bbox=bbox,
                page=page_num,
                detection_method='drawing',
                confidence=0.7,  # Lower confidence than images
                has_actual_figure=True
            ))

    return regions
```

#### Caption-Figure Pairing:

```python
def pair_captions_with_figures(
    captions: List[FigureCaption],
    detected_figures: List[FigureRegion],
    page: pymupdf.Page
) -> List[FigureRegion]:
    """
    Pair captions with nearby detected figures.

    Spatial relationships:
    - Figure usually ABOVE caption (most common)
    - Sometimes BELOW (less common)
    - Proximity threshold: ±100pt vertically
    - Horizontal alignment: same column or spanning
    """
    paired_regions = []
    used_figures = set()

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

            # Check horizontal alignment (same column or spanning)
            if not is_horizontally_aligned(caption_bbox, figure.bbox, page):
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
```

#### Orphan Caption Handling:

```python
def handle_orphan_captions(
    captions: List[FigureCaption],
    paired_regions: List[FigureRegion],
    page: pymupdf.Page,
    page_num: int
) -> List[FigureRegion]:
    """
    Create synthetic exclusion zones for captions without paired figures.

    These could be:
    - Pure vector figures (get_drawings didn't detect)
    - Tables (just formatted text)
    - Figures that span columns in weird ways

    Strategy: Assume figure is ABOVE caption (most common)
    """
    paired_captions = {r.associated_caption for r in paired_regions if r.associated_caption}
    orphan_captions = [c for c in captions if c not in paired_captions]

    synthetic_regions = []

    for caption in orphan_captions:
        caption_bbox = caption.bbox

        # Create synthetic bbox above caption
        # Assume reasonable figure size: 200pt wide, 150pt tall
        synthetic_bbox = (
            caption_bbox[0],           # x0: same left edge as caption
            caption_bbox[1] - 160,     # y0: 150pt figure + 10pt gap
            caption_bbox[2],           # x1: same right edge as caption
            caption_bbox[1] - 10       # y1: 10pt gap before caption
        )

        # Validate bbox (don't go off page)
        page_bbox = page.rect
        synthetic_bbox = clip_bbox_to_page(synthetic_bbox, page_bbox)

        synthetic_regions.append(FigureRegion(
            bbox=synthetic_bbox,
            page=page_num,
            detection_method='caption_inferred',
            confidence=0.5,  # Lower confidence for synthetic
            has_actual_figure=False,
            associated_caption=caption,
            exclusion_margin=(10, 30, 5, 5)
        ))

    logger.info(f"Created {len(synthetic_regions)} synthetic regions for orphan captions")
    return synthetic_regions
```

**Update File:** `backend/services/parser/pipeline/stages/geometry.py`

Add figure detection call:

```python
def apply_geometric_cleaning(
    doc: pymupdf.Document,
    config,
    structure_info: StructureInfo  # NEW parameter
) -> Tuple[pymupdf.Document, GeometryInfo]:
    """Apply geometric cleaning with figure detection."""
    logger.info("Applying geometric cleaning")

    # Existing margin detection
    geom_info = analyze_geometry(doc, config)
    bottom_margin = detect_footer_height(doc)

    # Apply crops
    logger.info(f"Cropping margins: top={config.top_margin}pt, bottom={bottom_margin}pt, left={geom_info.left_margin_cutoff}pt")
    doc = crop_margins(doc, config.top_margin, bottom_margin, geom_info.left_margin_cutoff)

    # NEW: Detect figures using captions from Stage 2
    from .figures import detect_figure_regions
    geom_info.figure_regions = detect_figure_regions(
        doc,
        structure_info.figure_captions,
        config
    )

    return doc, geom_info
```

---

### Phase 4: Smart Text Filtering (Stage 4)

**File:** `backend/services/parser/pipeline/stages/extraction.py`

Replace broken redaction (lines 180-209) with intelligent filtering.

#### Updated Extraction Function:

```python
def extract_markdown(
    doc: pymupdf.Document,
    geom_info: GeometryInfo,
    structure_info: StructureInfo
) -> str:
    """
    Extract markdown with figure-aware text filtering.

    Uses:
    - Figure regions from geometry stage (exclusion zones)
    - Caption list from analysis stage (preserve these!)
    """
    logger.info(f"Extracting markdown from {len(doc)} pages")

    # REMOVE old redaction code (lines 180-209)
    # REPLACE with smart pre-filtering

    for page_num, page in enumerate(doc):
        page_figure_regions = [f for f in geom_info.figure_regions if f.page == page_num]
        page_captions = [c for c in structure_info.figure_captions if c.page == page_num]

        if page_figure_regions:
            filter_figure_text_from_page(page, page_figure_regions, page_captions)

    # Extract with pymupdf4llm (existing code)
    markdown = pymupdf4llm.to_markdown(doc)

    logger.info(f"Extracted {len(markdown)} characters total")
    return markdown
```

#### Smart Filtering Function:

```python
def filter_figure_text_from_page(
    page: pymupdf.Page,
    figure_regions: List[FigureRegion],
    captions: List[FigureCaption]
):
    """
    Filter text blocks overlapping with figure regions.

    Rules:
    1. NEVER filter caption text (preserve it)
    2. Use variable overlap thresholds:
       - Small text (<20pt tall): 50% overlap → filter (likely labels)
       - Body text (≥20pt tall): 30% overlap → filter
    3. Check bbox comparison for accuracy
    """
    blocks = page.get_text("dict")["blocks"]

    for block in blocks:
        if block.get("type") != 0:  # Not a text block
            continue

        block_bbox = tuple(block["bbox"])
        block_text = extract_block_text(block).strip()
        block_height = block_bbox[3] - block_bbox[1]

        # Check if this block is a caption (NEVER filter captions)
        if is_caption_block(block_bbox, block_text, captions):
            continue

        # Check overlap with figure regions
        for figure_region in figure_regions:
            overlap_ratio = calculate_overlap_ratio(block_bbox, figure_region.bbox)

            # Determine threshold based on text size
            threshold = 0.5 if block_height < 20 else 0.3

            if overlap_ratio > threshold:
                # Mark block for exclusion
                # (Implementation: redact or modify block in place)
                redact_block(page, block)
                break  # Already filtered, no need to check other regions
```

#### Caption Protection:

```python
def is_caption_block(
    block_bbox: Tuple[float, float, float, float],
    block_text: str,
    captions: List[FigureCaption]
) -> bool:
    """
    Check if text block matches a detected caption.

    Uses bbox comparison (most reliable) with text fallback.
    """
    for caption in captions:
        # Primary: bbox overlap (≥80% overlap = same block)
        overlap = calculate_overlap_ratio(block_bbox, caption.bbox)
        if overlap > 0.8:
            return True

        # Fallback: text comparison (first 20 chars)
        if caption.text[:20] in block_text or block_text[:20] in caption.text:
            return True

    return False
```

#### Overlap Calculation:

```python
def calculate_overlap_ratio(bbox1: Tuple, bbox2: Tuple) -> float:
    """
    Calculate overlap ratio of bbox1 with bbox2.

    Returns: overlap_area / bbox1_area (0.0 to 1.0)
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
```

---

### Phase 5: Wire Data Flow

**File:** `backend/services/parser/pipeline/builder.py`

Update pipeline to pass data between stages:

```python
def build(self, pdf_bytes: bytes, filename: str) -> ParsedDocument:
    """Build parsed document through pipeline stages."""

    # Stage 1: Load
    doc, metadata = loader.load_pdf(pdf_bytes)
    if self.capture_stages:
        self._capture_stage("1_load", f"Loaded {len(doc)} pages")

    # Stage 2: Analyze (extracts captions)
    structure_info = analysis.analyze_structure(doc, self.config)
    if self.capture_stages:
        self._capture_stage("2_analyze",
            f"Title: {structure_info.title}\n"
            f"Sections: {len(structure_info.section_headers)}\n"
            f"Captions: {len(structure_info.figure_captions)}")  # NEW

    # Stage 3: Geometry (detects figures using captions)
    doc, geom_info = geometry.apply_geometric_cleaning(
        doc,
        self.config.geometry,
        structure_info  # Pass structure info with captions
    )
    if self.capture_stages:
        self._capture_stage("3_geometry",
            f"Line numbers: {geom_info.has_line_numbers}\n"
            f"Left margin: {geom_info.left_margin_cutoff}pt\n"
            f"Figure regions: {len(geom_info.figure_regions)}")  # NEW

    # Stage 4: Extract (uses both captions and figure regions)
    markdown = extraction.extract_markdown(
        doc,
        geom_info,       # Has figure regions
        structure_info   # Has caption list
    )
    if self.capture_stages:
        self._capture_stage("4_extract", markdown)

    # Stages 5-11: Continue as before
    # ...

    return parsed_doc
```

---

## Testing Strategy

### Test Execution

For each PDF in `backend/docs/testPDFs/`:

1. **Baseline Run** (with current code):
   - Record output
   - Note all garbage artifacts
   - Note any missing captions

2. **Enhanced Run** (with figure detection):
   - Compare output to baseline
   - Verify garbage reduction
   - Verify captions preserved
   - Check no body text lost

3. **Iterate** (up to 3 attempts per PDF):
   - If issues found, adjust thresholds/logic
   - Re-test
   - Log changes and results

### Test Log Format

```
PDF: testPDFs/1.pdf
Run: 1 (Enhanced)
Issues Found:
- Still seeing axis labels "0 2 4 6 8" in Results section
- Likely cause: Drawing detection missed this figure
- Fix attempted: Lower clustering threshold from 20→15pt

Run: 2 (Enhanced)
Issues Found:
- Fixed axis labels
- NEW: Lost one sentence of body text near figure
- Likely cause: Overlap threshold too aggressive
- Fix attempted: Raise body text threshold from 0.3→0.4

Run: 3 (Enhanced)
Issues Found: None
Status: ✓ PASS
Changes Applied:
- Drawing proximity threshold: 15pt
- Body text overlap threshold: 0.4
```

### Success Criteria

For each PDF:
- ✓ No axis labels or scattered figure text
- ✓ All captions preserved with proper formatting
- ✓ No body text lost (compare word count ±5%)
- ✓ Section ordering intact
- ✓ No new artifacts introduced

---

## Files Modified Summary

### New Files
- `backend/services/parser/pipeline/stages/figures.py` - Figure detection module
- `backend/services/parser/pipeline/tests/test_figures.py` - Figure detection tests

### Modified Files
- `backend/services/parser/pipeline/models.py` - Add FigureCaption, FigureRegion dataclasses
- `backend/services/parser/pipeline/stages/analysis.py` - Add caption detection
- `backend/services/parser/pipeline/stages/geometry.py` - Call figure detection
- `backend/services/parser/pipeline/stages/extraction.py` - Replace redaction with smart filtering
- `backend/services/parser/pipeline/builder.py` - Wire data flow between stages
- `backend/services/parser/pipeline/PIPELINE_FLOW.md` - Document new stages

---

## Implementation Order

1. **Models** - Add dataclasses (FigureCaption, FigureRegion)
2. **Analysis** - Add caption detection (Stage 2)
3. **Figures** - Create figure detection module
4. **Geometry** - Integrate figure detection (Stage 3)
5. **Extraction** - Fix text filtering (Stage 4)
6. **Builder** - Wire data flow
7. **Test** - Run on all test PDFs
8. **Document** - Update PIPELINE_FLOW.md

---

## Key Design Decisions

### Why Caption Detection in Stage 2?
- Need access to original geometry before cropping
- Leverage existing bold text detection infrastructure
- Keep analysis.py nimble for future structure detection

### Why Multi-Method Figure Detection?
- Embedded images: Reliable but misses vector graphics
- Vector drawings: Handles charts but noisy
- Caption inference: Catches everything but less precise
- Combination: Robustness through redundancy

### Why Variable Overlap Thresholds?
- Small text (labels, axis numbers): Part of figure, aggressive filtering (50%)
- Body text: Might legitimately wrap near figures, conservative filtering (30%)
- Captions: Never filter (0% tolerance)

### Why Synthetic Regions for Orphan Captions?
- Some figures won't be detected (pure vector, tables)
- Better to over-filter figure area than leak garbage
- Low confidence flag allows future refinement

---

## Future Enhancements

1. **Machine Learning**: Train classifier on labeled figure regions
2. **Table Detection**: Separate handling for table structures
3. **Equation Detection**: Identify and preserve mathematical content
4. **Multi-Column Awareness**: Better handling of column-spanning figures
5. **Caption Parsing**: Extract figure numbers for reference linking

---

## Success Metrics

- **Garbage Reduction**: <5% of output should be figure artifacts
- **Caption Preservation**: 100% of captions retained
- **Body Text Retention**: >95% of non-figure text preserved
- **Processing Time**: <2x slowdown from baseline
- **False Positives**: <1% of body text incorrectly filtered

---

**Status**: Ready for implementation
**Priority**: High - Core parsing quality improvement
**Estimated Effort**: 2-3 implementation sessions + 1-2 testing/refinement sessions
