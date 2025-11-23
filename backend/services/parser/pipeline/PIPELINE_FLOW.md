# PDF Parser Pipeline Flow



Current flow:
1. Load PDF
2. Analyze Structure
3. Geometric Cleaning
4. Extract Markdown
5. Reflow Text
6. Cleanup Artifacts
7. Inject Section Labels
8. Split into Sections
9. Validate Sections
10. Index Sentences
11. Extract Metadata (Citations, Figures, Bibliography)

## Overview

This document describes the complete execution flow of the PDF parsing pipeline, from raw PDF bytes to structured `ParsedDocument`.

## Pipeline Stages (in order)

### Stage 1: Load PDF
**Module:** `stages/loader.py`
**Function:** `load_pdf(pdf_bytes) → pymupdf.Document`

**What it does:**
- Loads raw PDF bytes into pymupdf Document object
- Extracts basic PDF metadata (title, author, page count)
- Validates the PDF is readable and has content

**Output:** pymupdf Document object + metadata dict

---

### Stage 2: Analyze Structure
**Module:** `stages/analysis.py`
**Function:** `analyze_structure(doc, config) → StructureInfo`

**What it does:**
- Scans ALL pages for bold text (font metadata analysis)
- Detects paper title from largest bold text on first page
- Identifies section headers by matching bold text against standard section names (Introduction, Results, Methods, Discussion, etc.)
- Extracts abstract using fallback heuristics (looks for "Abstract" header or first substantial paragraph)
- **NEW:** Detects figure captions with robust pattern matching:
  - Handles Figure/Fig/Table/Scheme variations (case-insensitive)
  - Distinguishes standalone captions from inline references
  - Handles unicode spaces, subfigures (1A, 2B), supplementary figures
  - Stores caption text, type, bbox, and confidence score

**Output:** StructureInfo with title, abstract, section headers, bold spans, **figure captions**

**Why before cropping:** Need to analyze original page geometry for accurate font size detection and caption positioning

**Note:** This stage only *detects* structure - it doesn't modify the document. The actual labeling happens in Stage 7.

---

### Stage 3: Geometric Cleaning & Figure Detection
**Module:** `stages/geometry.py` + `stages/figures.py`
**Function:** `apply_geometric_cleaning(doc, config, structure_info) → (Document, GeometryInfo)`

**What it does:**
- Analyzes page geometry to detect line numbers (x < 100pt threshold)
- Crops margins: top (60pt), bottom (60pt), left (if line numbers detected)
- Removes headers/footers by geometric position
- **NEW:** Detects figure regions using multiple methods:
  - **Image detection:** Uses `get_images()` to find embedded images (≥150x100pt, 20k area)
  - **Vector drawing detection:** Uses `get_drawings()` with clustering for charts/plots
  - **Caption-figure pairing:** Matches detected captions with figures by proximity (±100pt)
  - **Synthetic zones:** Creates exclusion zones for orphan captions (likely tables or vector figures)
  - Expands figure bboxes with margins (top: 10pt, bottom: 30pt, sides: 5pt)

**Figure Detection Process:**
1. For each page with captions, detect embedded images
2. Cluster vector drawings to identify charts/plots (≥5 elements, density threshold)
3. Pair captions with nearby figures (vertical proximity + horizontal alignment)
4. For unpaired captions, create synthetic exclusion zones (assume figure above caption)

**Output:** Modified pymupdf Document with cropped pages + GeometryInfo **with figure regions**

---

### Stage 4: Extract Markdown with Smart Figure Filtering
**Module:** `stages/extraction.py`
**Function:** `extract_markdown(doc, geom_info, structure_info) → str`

**What it does:**
- **ENHANCED:** Applies smart figure-aware text filtering BEFORE extraction:
  - Uses figure regions from Stage 3 (both detected and synthetic)
  - Uses caption list from Stage 2 to preserve caption text
  - **NEVER filters caption text** (bbox-based comparison)
  - Variable overlap thresholds:
    - Small text (<20pt tall): 50% overlap → filter (likely axis labels)
    - Body text (≥20pt tall): 30% overlap → filter
  - Applies redactions to overlapping text blocks
- Uses pymupdf4llm for robust markdown extraction:
  - Intelligent column detection (handles mixed single/two-column layouts)
  - Proper reading order (left column first, then right column)
  - Bold formatting preservation (`**text**`)
  - Proper spacing between text spans

**Smart Filtering Algorithm:**
```python
for each text block:
    if block matches a detected caption:
        PRESERVE (never filter)
    elif block overlaps figure region:
        if block_height < 20pt and overlap > 50%:
            FILTER (likely label/axis text)
        elif overlap > 30%:
            FILTER (body text inside figure)
    else:
        PRESERVE
```

**Key Improvements:**
- Dramatically reduces figure artifacts (axis labels, scattered text)
- Preserves all caption text with proper formatting
- Reduces false positives by using caption list instead of pattern matching

**Output:** Clean markdown string with figure artifacts filtered but captions preserved

---

### Stage 5: Reflow Text
**Module:** `stages/reflow.py`
**Function:** `reflow_text(markdown, config) → str`

**What it does:**
- Merges hyphenated words across line breaks (`com-\nputer` → `computer`)
- Reconstructs paragraphs broken by PDF line wrapping
- Detects sentence boundaries (period + capital letter)
- Preserves section headers and intentional line breaks
- Handles citation markers `[1]` correctly

**Output:** Markdown with reconstructed paragraphs

---

### Stage 6: Cleanup Artifacts
**Module:** `stages/cleanup.py`
**Function:** `cleanup_all(markdown, config) → str`

**What it does:**
- **MINIMAL APPROACH**: Only removes what we're confident is garbage
- Removes short gibberish lines (1-3 chars, excluding valid list markers like "a.", "1.", "-")
- Removes scattered single characters (figure axis labels like "a b c d" or "0 5 10 15 20")
- Removes table formatting remnants (pipes/dashes, table rows without real content)
- Removes lines containing URLs (http://, https://, www., .com, .org, .edu, .gov)
- Normalizes whitespace (collapse >3 newlines, >2 spaces)

**What it DOESN'T remove (to preserve content):**
- Unicode symbols (±, °C, μm) - might be real scientific notation
- Number-heavy lines - might be measurements, references, data
- Excessive caps - might be author names, chemical formulas
- Tables with actual content (>2 words per cell)

**Output:** Clean markdown with minimal content loss (~90-95% retention)

---

### Stage 7: Inject Section Labels
**Module:** `stages/labeling.py`
**Function:** `inject_section_labels(markdown, structure_info) → str`

**What it does:**
- Uses structure information from Stage 2 to insert section headers into markdown
- Finds bold text matching detected section headers (e.g., `**1. Introduction**`)
- Replaces them with proper markdown headers (e.g., `### **Introduction**`)
- Strips leading numbers from section names for consistency
- Handles abstract specially if detected
- Supports multiple matching patterns for robustness

**Output:** Markdown with section labels inserted as `### **Section Name**` headers

**Why after cleanup:** Need clean text before pattern matching section headers

---

### Stage 8: Split into Sections
**Module:** `stages/formatting.py`
**Function:** `split_sections(markdown, config) → Dict[str, ParsedSection]`

**What it does:**
- Splits markdown on section headers: `### **Section Name**`
- Normalizes section names to snake_case (`Materials and Methods` → `materials_and_methods`)
- Assigns priority order (abstract=1, intro=10, methods=20, results=30, etc.)
- Detects unlabeled sections by keyword analysis
- Text before first section goes into `preamble`

**Output:** Dictionary of section_name → ParsedSection objects

---

### Stage 9: Validate Sections
**Module:** `stages/formatting.py`
**Function:** `validate_required_sections(sections, config) → Dict[str, bool]`

**What it does:**
- Checks for required section groups:
  - Introduction (required)
  - Methods (required: methods OR materials_and_methods OR experimental)
  - Results (required)
  - Discussion (required: discussion OR conclusion OR results_and_discussion)
- Returns validation results (warnings only, doesn't fail)

**Output:** Dict of validation checks → pass/fail

---

### Stage 10: Index Sentences
**Module:** `stages/indexing.py`
**Function:** `index_sentences(sections, config) → Dict[str, ParsedSection]`

**What it does:**
- Splits each section's text into individual sentences
- Uses NLTK sentence tokenizer (falls back to regex)
- Generates unique sentence IDs (hash-based)
- Tracks sentence position and paragraph index
- Updates ParsedSection objects with sentence arrays

**Output:** Sections with populated `sentences` field

---

### Stage 11: Extract Metadata

#### 11a. Extract Citations
**Module:** `extractors/citations.py`
**Function:** `extract_citations(sections) → List[CitationRef]`

**What it does:**
- Finds citation markers: `[1]`, `[2,3]`, `[4-6]`
- Extracts context around citation (sentence)
- Records section and sentence index
- Links citations to sentences

**Output:** List of CitationRef objects

#### 11b. Extract Figures
**Module:** `extractors/figures.py`
**Function:** `extract_figures(markdown, sections) → (List[FigureBlock], List[FigureRef])`

**What it does:**
- Finds figure references in text: `Figure 1`, `Fig. 2A`
- Extracts figure captions from markdown
- Records figure labels and captions
- Tracks where figures are referenced

**Output:** List of FigureBlock + List of FigureRef

#### 11c. Extract Bibliography
**Module:** `extractors/bibliography.py`
**Function:** `parse_bibliography(section) → List[BibliographyEntry]`

**What it does:**
- Parses `references` or `bibliography` section
- Extracts numbered entries `[1] Author et al...`
- Parses authors, year, title, journal
- Extracts DOIs if present

**Output:** List of BibliographyEntry objects

---

### Stage 12: Assemble Final Document
**Module:** `builder.py`
**Function:** Internal assembly in `build()` method

**What it does:**
- Generates document ID (UUID) and hash (SHA256 of PDF bytes)
- Selects title (from structure analysis OR PDF metadata OR filename)
- Combines all extracted data into ParsedDocument
- Stores raw markdown for backward compatibility
- Closes pymupdf Document to free memory

**Output:** Complete `ParsedDocument` object

---

## Data Flow Diagram

```
PDF Bytes (input)
    ↓
[1. Load] → pymupdf.Document + metadata
    ↓
[2. Analyze] → StructureInfo (title, abstract, headers)
    ↓
[3. Geometry] → Cropped Document (margins removed)
    ↓
[4. Extract] → Raw Markdown (with artifacts)
    ↓
[5. Reflow] → Reflowed Markdown (paragraphs reconstructed)
    ↓
[6. Cleanup] → Clean Markdown (artifacts removed)
    ↓
[7. Label] → Markdown with section headers (### **Section Name**)
    ↓
[8. Split] → Dict[section_name, ParsedSection]
    ↓
[9. Validate] → Validation results (warnings)
    ↓
[10. Index] → Sections with sentences
    ↓
[11. Extract Metadata]
    ├─ [11a. Citations] → List[CitationRef]
    ├─ [11b. Figures] → List[FigureBlock], List[FigureRef]
    └─ [11c. Bibliography] → List[BibliographyEntry]
    ↓
[12. Assemble] → ParsedDocument
    ↓
ParsedDocument (output)
```

## Configuration Points

Each stage can be configured via `PipelineConfig`:

- **Geometry:** `top_margin`, `bottom_margin`, `detect_line_numbers`
- **Analysis:** `detect_bold_text`, `extract_title`, `min_title_font_size`
- **Reflow:** `enable_reflow`, `merge_hyphenations`
- **Cleanup:** `remove_figure_blocks`, `remove_copyright`, `remove_doi_lines`, etc.
- **Sections:** `required_groups`, `section_order`
- **Indexing:** `enable_sentence_indexing`, `use_nltk`
- **Extraction:** `extract_citations`, `extract_figures`, `extract_bibliography`

See `parser_config.yaml` for full configuration template.

## Error Handling

- **Stage 1 (Load):** Raises `ValueError` if PDF is invalid
- **Stage 8 (Validate):** Logs warnings, doesn't fail
- **Stage 9 (Index):** Falls back to regex if NLTK fails
- **All stages:** Log progress at INFO level, errors at ERROR level

## Performance Notes

- **Bottlenecks:** Stage 4 (pymupdf4llm extraction) and Stage 9 (NLTK tokenization)
- **Memory:** Document closed at end to free memory
- **Stateless:** All stages are pure functions (except final assembly)
- **Parallelizable:** Stages 10a/10b/10c could run in parallel (future optimization)

## Entry Point

```python
from services.parser.pipeline import PipelineBuilder, default_config

builder = PipelineBuilder(default_config())
parsed_doc = builder.build(pdf_bytes, "paper.pdf")
```

See `USAGE.md` for detailed examples.

## Debug Mode: Pipeline Stage Viewer

The pipeline supports capturing intermediate outputs from each stage for debugging purposes.

### How to Enable

```python
builder = PipelineBuilder(default_config(), capture_stages=True)
parsed_doc = builder.build(pdf_bytes, "paper.pdf")

# Access stage outputs
for stage_id, content in builder.stage_outputs.items():
    print(f"{stage_id}: {content[:100]}...")
```

### Available Stage Outputs

When `capture_stages=True`, the following intermediate outputs are captured:

1. **2_analyze_structure**: Title, abstract preview, section count
2. **3_geometric_cleaning**: Geometry info (line numbers detected, margin crops)
3. **4_extract_markdown**: Raw markdown after extraction
4. **5_reflow_text**: Markdown after paragraph reflow
5. **6_cleanup_artifacts**: Markdown after artifact removal
6. **7_inject_section_labels**: Markdown with section headers injected
7. **8_split_sections**: Summary of split sections
8. **9_validate_sections**: Validation results (pass/fail)
9. **10_index_sentences**: Sentence counts per section
10. **11_extract_metadata**: Citation/figure/bibliography counts
11. **12_final_output**: Final markdown output

### Frontend Debug Viewer

The API endpoint `/debug/pipeline-stages/{document_id}` (debug mode only) returns all captured stages.

The frontend DocumentViewer component includes navigation controls to step through each stage:
- Left/right arrows to navigate between stages
- Stage label and position indicator
- "Show Final" button to return to final output

This allows visual debugging of the pipeline to identify where parsing issues occur.

### Performance Impact

When `capture_stages=False` (default in production), there is **zero performance impact** - the capture code is entirely skipped.

---

## Figure Detection Enhancement (November 2024)

### Overview

Enhanced the pipeline with comprehensive figure detection and smart text filtering to eliminate figure artifacts (axis labels, scattered text, figure-internal content) while preserving caption text.

### Architecture

**Three-Stage Approach:**
1. **Caption Detection (Stage 2):** Identify figure captions early using bold text analysis
2. **Figure Region Detection (Stage 3):** Locate actual figures using multiple detection methods
3. **Smart Filtering (Stage 4):** Filter text overlapping figures while protecting captions

### Key Features

**Multi-Method Figure Detection:**
- Embedded images via `get_images()` (most reliable)
- Vector drawings via `get_drawings()` with clustering (for charts/plots)
- Caption-based inference (spatial proximity matching)
- Synthetic exclusion zones for orphan captions (tables, complex vector figures)

**Smart Text Filtering:**
- Caption protection: NEVER filters text matching detected captions
- Variable thresholds: Different overlap percentages for labels (50%) vs body text (30%)
- Bbox-based comparison for accuracy

**Caption Detection:**
- Handles variations: Figure/Fig/Table/Scheme, case-insensitive
- Distinguishes standalone captions from inline references
- Unicode-aware, handles subfigures (1A, 2B), supplementary figures

### Data Flow

```
Stage 2 (Analysis)
    ↓ StructureInfo.figure_captions
Stage 3 (Geometry + Figures)
    ↓ GeometryInfo.figure_regions
Stage 4 (Extraction)
    Uses both captions + regions for smart filtering
```

### Performance

**Test Results (6 scientific papers):**
- ✅ 100% success rate (no crashes or parse errors)
- ✅ Detected 4-8 captions per paper
- ✅ Created appropriate figure regions (mix of detected + synthetic)
- ✅ Dramatically reduced figure artifacts (from hundreds to <10 instances)
- ⚠️ Edge cases: A few scattered characters remain (labels just outside synthetic regions)

**Processing Impact:**
- Minimal overhead (<2s per paper for figure detection)
- Caption detection: ~0.1s per page
- Figure region creation: ~0.2s per page with figures

### Configuration

All figure detection is automatically enabled when captions are found. No manual configuration required.

**Thresholds (configurable in future if needed):**
- Image size: min 150x100pt, 20k area
- Drawing cluster: min 5 elements
- Caption proximity: ±100pt vertical
- Overlap filtering: 30% body text, 50% small text
- Exclusion margins: top 10pt, bottom 30pt, sides 5pt

### Future Enhancements

Potential improvements:
1. **Adaptive synthetic regions:** Size based on adjacent figures
2. **Column-aware pairing:** Better handling of column-spanning figures
3. **Machine learning:** Train classifier on labeled figure regions
4. **Table-specific detection:** Separate handling for table structures
5. **Equation detection:** Preserve mathematical content

### Files Modified

**New:**
- `stages/figures.py` - Figure detection module (480 lines)

**Updated:**
- `models.py` - Added FigureCaption, FigureRegion dataclasses
- `stages/analysis.py` - Added caption detection (~320 lines)
- `stages/geometry.py` - Integrated figure detection call
- `stages/extraction.py` - Replaced redaction with smart filtering
- `builder.py` - Wired data flow between stages
