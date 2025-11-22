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
- Filters out figure captions from structure detection

**Output:** StructureInfo with title, abstract, section headers, bold spans

**Why before cropping:** Need to analyze original page geometry for accurate font size detection

**Note:** This stage only *detects* structure - it doesn't modify the document. The actual labeling happens in Stage 7.

---

### Stage 3: Geometric Cleaning
**Module:** `stages/geometry.py`
**Function:** `apply_geometric_cleaning(doc, config) → (Document, GeometryInfo)`

**What it does:**
- Analyzes page geometry to detect line numbers (x < 100pt threshold)
- Crops margins: top (60pt), bottom (60pt), left (if line numbers detected)
- Removes headers/footers by geometric position
- Returns cleaned document ready for text extraction

**Output:** Modified pymupdf Document with cropped pages + GeometryInfo

---

### Stage 4: Extract Markdown
**Module:** `stages/extraction.py`
**Function:** `extract_markdown(doc) → str`

**What it does:**
- Performs **intelligent column detection** using clustering to handle mixed layouts (e.g., single-column abstract followed by two-column body)
- For each page:
  - Detects main figures (≥150pt width, ≥100pt height, ≥20k area) to filter out icons/decorations
  - Removes text blocks that overlap with figures
  - Analyzes horizontal distribution of text blocks using clustering
  - Detects single vs two-column layout based on cluster separation
  - Extracts text in correct reading order (left column first, then right column for two-column layouts)
- Inserts `[FIGURE:n]` placeholders for main figures in correct vertical position
- Preserves bold formatting as `**text**` via `extract_text_from_block()`
- Handles proper spacing between text spans

**Column Detection Algorithm:**
- Collects x-centers of all text blocks (min 40pt width, 5pt height)
- Uses KMeans clustering (k=2) to find left/right cluster centers (with fallback to median-based splitting)
- If cluster centers < 120pt apart → single column
- Otherwise → two-column with divider at midpoint between cluster centers
- Handles spanning elements (>300pt wide) separately

**Figure Filtering:**
- Minimum width: 150pt (~2 inches)
- Minimum height: 100pt (~1.4 inches)
- Minimum area: 20,000 pt² (e.g., 200×100pt)
- Typical papers have 3-10 main figures detected

**Output:** Raw markdown string with text in correct reading order and figures placed (with artifacts still present)

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
