# PDF Parser Pipeline Flow



Current flow:
1. Load PDF
2. Analyze Structure (+ Authors & Affiliations)
3. Geometric Cleaning & Figure Detection
4. Extract Markdown
5. Reflow Text
6. Cleanup Artifacts (+ Editor Notes Detection)
7. Inject Section Labels
8. Split into Sections (+ Heading Classification & Nesting)
9. Validate Sections
10. Index Sentences
11. Extract Metadata (Citations, Figures, Bibliography)
12. Normalize Document Structure (Reorganize sections, separate meta/body/references)

## Overview

This document describes the complete execution flow of the PDF parsing pipeline, from raw PDF bytes to normalized, structured `ParsedDocument`.

**Output Structure:**
The pipeline produces a standardized document with:
1. **Title** - Cleaned, normalized
2. **Authors & Affiliations** - Extracted, structured (names, institutions, emails, corresponding author)
3. **Abstract** - Standalone, complete
4. **Body Sections** - Preserved in original order with hierarchical subsection nesting
5. **Meta Sections** - Author contributions, acknowledgements, conflicts (separated from body)
6. **References** - Structured bibliography
7. **Supplementary Materials** - If present

**Stored Separately:**
- Figure Captions (with figure numbers, linked to in-text references)
- Editor Notes / Significance Statements (flagged as non-manuscript content)

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

### Stage 2: Analyze Structure & Extract Authors
**Module:** `stages/analysis.py`
**Function:** `analyze_structure(doc, config) → StructureInfo`

**What it does:**
- Scans ALL pages for bold text (font metadata analysis)
- Detects paper title from largest bold text on first page
- **NEW: Extracts authors & affiliations** from first page after title:
  - Parses author names and affiliation superscripts (1, 2, *, †)
  - Extracts affiliation institutions, departments, locations
  - Detects email addresses and corresponding author markers
- **NEW: Classifies all headings** by type and level:
  - Type: 'body', 'meta', 'references', 'supplementary'
  - Level: 1 (major section), 2 (subsection), 3 (sub-subsection)
  - Uses font size, bold status, and numbering patterns
- Identifies section headers by matching bold text against standard section names (Introduction, Results, Methods, Discussion, etc.)
- Extracts abstract using fallback heuristics (looks for "Abstract" header or first substantial paragraph)

**Output:** StructureInfo with title, abstract, authors, affiliations, classified headings, section headers, bold spans

**Why before cropping:** Need to analyze original page geometry for accurate font size detection

**Note:** This stage only *detects* structure - it doesn't modify the document. Labeling happens in Stage 7, reorganization in Stage 12.

---

### Stage 3: Geometric Cleaning & Caption-Anchored Figure Detection
**Module:** `stages/geometry.py` + `stages/figures.py` + `stages/analysis.py`
**Function:** `apply_geometric_cleaning(doc, config, structure_info) → (Document, GeometryInfo)`

**What it does:**
1. Analyzes page geometry to detect line numbers (x < 100pt threshold)
2. Crops margins: top (60pt), bottom (dynamic footer detection), left (if line numbers detected)
3. Removes headers/footers by geometric position
4. Detects figure captions on CROPPED pages (after footer removal):
   - Handles Figure/Fig/Table/Scheme variations (case-insensitive)
   - Distinguishes standalone captions from inline references
   - Handles unicode spaces, subfigures (1A, 2B), supplementary figures
   - Stores caption text, type, bbox, and confidence score
5. **NEW: Dual-Method Figure Detection** (November 22, 2024):
   - **Method 1: Vertical Deletion** - Primary method using captions as anchors
   - **Method 2: Proximity Clustering** - Secondary method for uncaptioned figures

**Method 1: Vertical Deletion Above Captions:**

This is the primary detection method, using captions as reliable semantic anchors:

1. **Determine caption width type:**
   - Full-width: caption width >70% of page width
   - Column-width: caption width ≤70% of page width

2. **Set horizontal bounds:**
   - Full-width figures: Use most of page width (30pt margins)
   - Column-width figures: Use caption horizontal bounds ± 20pt

3. **Look ABOVE caption for text blocks:**
   - Find first REAL paragraph (>50 chars, >10 words, ends with period)
   - If found: Set top edge = paragraph bottom + 10pt
   - If not found: Use default 300pt deletion region above caption

4. **Create deletion region:**
   - Top: paragraph bottom (or default 300pt above caption)
   - Bottom: caption top - 10pt gap
   - Left/Right: Based on caption width type

5. **Validate region:**
   - Height ≥20pt, width ≥50pt
   - Skip regions that are too small

**Method 2: Proximity-Based Clustering:**

Secondary method to catch uncaptioned figures (charts, plots, images):

1. **Collect visual elements** (filter tiny ones <20pt):
   - Images via `get_images()` (embedded photos, renders)
   - Vector drawings via `get_drawings()` (charts, plots)

2. **Merge nearby elements** (20pt proximity):
   - Group overlapping/adjacent elements
   - Create unified bboxes for each group

3. **Filter clusters by size:**
   - Keep only substantial clusters (≥50pt width and height)
   - Add small margins (10pt) for proximity filtering

4. **Create FigureRegion for each cluster**

**Key Advantages:**
- **Simple and robust**: Relies on paragraph detection rather than complex ray-casting
- **Width-aware**: Handles both full-width and column-width figures correctly
- **Dual method**: Catches both captioned and uncaptioned figures
- **Minimal filtering**: Filters tiny elements (likely artifacts) before clustering

**Output:** Modified pymupdf Document with cropped pages + GeometryInfo with figure captions AND regions

**Why this works:** Captions are the most reliable signal. By deleting vertically above them until hitting a paragraph, we get precise figure regions without complex boundary detection. Proximity clustering catches any remaining uncaptioned figures.

---

### Stage 4: Extract Markdown with Simple Figure Filtering
**Module:** `stages/extraction.py`
**Function:** `extract_markdown(doc, geom_info, structure_info) → str`

**What it does:**
- Applies simple figure-aware text filtering using deletion regions from Stage 3:
  - Uses vertical deletion regions + proximity clusters (precise boundaries)
  - **NEVER filters caption text** (100% caption preservation via bbox comparison)
  - **Simple overlap threshold**: Any text block with >10% overlap with figure region → filter
  - Skips filtering on page 0 (title/abstract page)
  - Applies redactions to overlapping text blocks
- Uses pymupdf4llm for robust markdown extraction:
  - Intelligent column detection (handles mixed single/two-column layouts)
  - Proper reading order (left column first, then right column)
  - Bold formatting preservation (`**text**`)
  - Proper spacing between text spans

**Balanced Filtering Algorithm:**
```python
for each text block:
    if block matches a detected caption:
        PRESERVE (never filter)
    elif block overlaps figure region:
        if block_height < 10pt and overlap > 60%:
            FILTER (tiny text - axis labels)
        elif block_height < 20pt and overlap > 50%:
            FILTER (small text - legends/labels)
        elif overlap > 70%:
            FILTER (body text mostly inside figure)
    else:
        PRESERVE
```

**Why balanced thresholds work:**
- Caption-anchored regions are already precise (stopped at paragraph boundaries)
- Higher thresholds (50-70% vs old 15-20%) prevent false positives
- Only filter text that is substantially inside figure regions
- Preserves adjacent body paragraphs that merely touch figure boundaries

**Key Results (vs. old bottom-up approach):**
- ✅ 100% elimination of scattered artifacts (0 vs baseline 5)
- ✅ 100% caption preservation (caption-aware filtering)
- ✅ Minimal false positives (balanced thresholds)
- ⚠️ Slightly more lines (146 vs baseline 98) - but these are correct paragraph breaks

**Output:** Clean markdown string with figure artifacts removed and captions preserved

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

### Stage 6: Cleanup Artifacts & Detect Editor Notes
**Module:** `stages/cleanup.py`
**Function:** `cleanup_all(markdown, config) → (str, Optional[str])`

**What it does:**
- **MINIMAL APPROACH**: Only removes what we're confident is garbage
- Removes short gibberish lines (1-3 chars, excluding valid list markers like "a.", "1.", "-")
- Removes scattered single characters (figure axis labels like "a b c d" or "0 5 10 15 20")
- Removes table formatting remnants (pipes/dashes, table rows without real content)
- Removes lines containing URLs (http://, https://, www., .com, .org, .edu, .gov)
- Normalizes whitespace (collapse >3 newlines, >2 spaces)
- **NEW: Detects and extracts editor notes**:
  - Pattern matching for: eLife Digest, Editor's Summary, Significance Statement, Plain Language Summary
  - Extracts bioRxiv preprint warnings and disclaimers
  - Returns editor notes separately, removes from main document

**What it DOESN'T remove (to preserve content):**
- Unicode symbols (±, °C, μm) - might be real scientific notation
- Number-heavy lines - might be measurements, references, data
- Excessive caps - might be author names, chemical formulas
- Tables with actual content (>2 words per cell)

**Output:** (Clean markdown, Editor notes or None) with minimal content loss (~90-95% retention)

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

### Stage 8: Split into Sections & Build Hierarchy
**Module:** `stages/formatting.py`
**Function:** `split_sections(markdown, headings, config) → Dict[str, ParsedSection]`

**What it does:**
- Splits markdown on section headers: `### **Section Name**`
- Normalizes section names to snake_case (`Materials and Methods` → `materials_and_methods`)
- Assigns priority order (abstract=1, intro=10, methods=20, results=30, etc.)
- Detects unlabeled sections by keyword analysis
- Text before first section goes into `preamble`
- **NEW: Builds hierarchical subsection nesting**:
  - Uses heading level from Stage 2 (1, 2, 3)
  - Nests level 2 headings under level 1
  - Nests level 3 headings under level 2
  - Creates recursive `NestedSection` structure

**Output:** Dictionary of section_name → ParsedSection objects (with nested subsections)

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

### Stage 12: Normalize Document Structure
**Module:** `stages/normalization.py`
**Function:** `normalize_document(sections, headings, authors, editor_notes) → NormalizedDocument`

**What it does:**
- **Reorganizes sections into standardized structure:**
  1. Separates body sections from meta sections (contributions, acknowledgements, conflicts, funding)
  2. Preserves original order of body sections (Introduction → Results → Discussion → Methods, etc.)
  3. Moves meta sections after body content
  4. Separates references and supplementary materials
- **Builds hierarchical structure:**
  - Nests subsections under parent sections
  - Preserves level 1 → level 2 → level 3 hierarchy
- **Attaches metadata:**
  - Authors & affiliations from Stage 2
  - Figure captions (linked to in-text references)
  - Editor notes (if detected in Stage 6)
- **Classifies sections by type:**
  - Body: Introduction, Results, Methods, Discussion, etc.
  - Meta: Contributions, Acknowledgements, Conflicts, Funding
  - References: Bibliography entries
  - Supplementary: Appendices, supplementary materials

**Output:** `NormalizedDocument` with standardized, hierarchical structure

---

### Stage 13: Assemble Final Document
**Module:** `builder.py`
**Function:** Internal assembly in `build()` method

**What it does:**
- Generates document ID (UUID) and hash (SHA256 of PDF bytes)
- Selects title (from structure analysis OR PDF metadata OR filename)
- Wraps NormalizedDocument in ParsedDocument envelope
- Stores raw markdown for backward compatibility
- Closes pymupdf Document to free memory

**Output:** Complete `ParsedDocument` object with embedded `NormalizedDocument`

---

## Data Flow Diagram

```
PDF Bytes (input)
    ↓
[1. Load] → pymupdf.Document + metadata
    ↓
[2. Analyze] → StructureInfo (title, abstract, authors, affiliations, classified headings, bold spans)
    ↓
[3. Geometry] → Crop margins/footers FIRST
    ↓         → Detect captions on CLEAN pages
    ↓         → Detect figure regions
    ↓         → GeometryInfo (figure_captions, figure_regions)
    ↓
[4. Extract] → Raw Markdown (with figure filtering using captions from Step 3)
    ↓
[5. Reflow] → Reflowed Markdown (paragraphs reconstructed)
    ↓
[6. Cleanup] → (Clean Markdown, Editor Notes)
    ↓
[7. Label] → Markdown with section headers (### **Section Name**)
    ↓
[8. Split & Nest] → Dict[section_name, ParsedSection] (with nested subsections)
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
[12. Normalize] → NormalizedDocument (body/meta/references separated, hierarchical)
    ↓
[13. Assemble] → ParsedDocument (with NormalizedDocument embedded)
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

**UPDATED (November 22, 2024):**
```
Stage 2 (Analysis)
    ↓ StructureInfo (title, abstract, headers, bold spans)
Stage 3 (Geometry + Figures)
    ↓ Crop margins/footers FIRST
    ↓ Detect captions on CLEAN pages → GeometryInfo.figure_captions
    ↓ Detect figure regions → GeometryInfo.figure_regions
Stage 4 (Extraction)
    Uses captions + regions from GeometryInfo for smart filtering
```

**Key Change:** Caption detection moved from Stage 2 to Stage 3 (after cropping) to prevent footer/header text contamination.

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
- `models.py` - Added FigureCaption, FigureRegion dataclasses; moved figure_captions from StructureInfo to GeometryInfo
- `stages/analysis.py` - Added caption detection (~320 lines); kept detect_captions() function for use in Stage 3
- `stages/geometry.py` - Integrated caption detection AFTER cropping, then figure detection
- `stages/extraction.py` - Replaced redaction with smart filtering; updated to use GeometryInfo.figure_captions
- `builder.py` - Wired data flow between stages; updated stage capture output

---

## Caption Detection Refactor (November 22, 2024)

### Problem
Caption detection in Stage 2 (before cropping) caused footer/header text to merge into caption text at page boundaries. Example: a caption at the bottom of a page would pick up "bioRxiv preprint" footer text.

### Solution
Moved caption detection from Stage 2 (analysis.py) to Stage 3 (geometry.py), AFTER margin/footer cropping:

1. **Stage 2:** Detects title, abstract, sections, bold spans (NO caption detection)
2. **Stage 3:**
   - Crops margins/footers FIRST
   - THEN detects captions on clean pages
   - THEN detects figure regions
3. **Stage 4:** Uses clean captions from GeometryInfo for text filtering

### Data Model Changes
- `StructureInfo.figure_captions` → **removed**
- `GeometryInfo.figure_captions` → **added**

### Test Results (November 22, 2024)
- ✅ All 8 test PDFs processed successfully
- ✅ Caption counts unchanged (detection still works)
- ✅ No footer/header contamination in captions
- ✅ Zero parsing errors or crashes

### Files Modified
- `backend/services/parser/pipeline/models.py` - Moved figure_captions field
- `backend/services/parser/pipeline/stages/analysis.py` - Removed caption detection from analyze_structure()
- `backend/services/parser/pipeline/stages/geometry.py` - Added caption detection after cropping
- `backend/services/parser/pipeline/stages/extraction.py` - Updated to use geom_info.figure_captions
- `backend/services/parser/pipeline/builder.py` - Updated stage outputs and data flow

---

## Normalized Document Structure Implementation Plan (November 2024)

### Overview

The pipeline now includes normalization as a core stage (Stage 12) to output standardized, predictable document structure regardless of input paper format variations. This provides downstream agents (reviewers, summarizers) with consistent, clean data to work with.

### Target Output Structure

**Primary Document Sections (in order):**
1. **Title** - Cleaned, normalized
2. **Authors & Affiliations** - Extracted, structured (names, institutions, emails, corresponding author)
3. **Abstract** - Standalone, complete
4. **Body Sections** - Preserved in original order with hierarchical subsection nesting
   - Introduction
   - Results
     - 2.1 Subsection Name
     - 2.2 Subsection Name
   - Discussion
   - Methods
     - 4.1 Cell Culture
     - 4.2 Statistical Analysis
   - etc.
5. **Meta Sections** - Separated from body, always after main content
   - Author Contributions
   - Acknowledgements
   - Conflicts of Interest / Competing Interests
   - Funding / Grants
6. **References** - Structured bibliography
7. **Supplementary Materials** - If present

**Stored Separately:**
- **Figure Captions** - With figure numbers, linked to in-text references
- **Editor Notes / Significance Statements** - Flagged as non-manuscript content (e.g., eLife digests, bioRxiv warnings)

### Implementation Approach

#### Phase 1: Author & Affiliation Extraction
**New Stage or Enhancement to Stage 2:**
```python
@dataclass
class Author:
    name: str
    affiliations: List[int]  # References to affiliation indices
    email: Optional[str]
    is_corresponding: bool

@dataclass
class Affiliation:
    index: int
    institution: str
    department: Optional[str]
    location: Optional[str]  # City, country

@dataclass
class AuthorBlock:
    authors: List[Author]
    affiliations: List[Affiliation]
```

**Detection Strategy:**
- Parse first page after title for author lines
- Use superscripts for affiliation mapping (1, 2, *, †)
- Detect email addresses via regex
- Identify corresponding author markers (*, ✉, "corresponding")

#### Phase 2: Heading Classification & Nesting
**Enhancement to Stage 2 (analysis.py):**
```python
@dataclass
class Heading:
    text: str
    level: int  # 1=major section, 2=subsection, 3=sub-subsection
    page: int
    bbox: Tuple[float, float, float, float]
    section_type: str  # 'body', 'meta', 'references', 'supplementary'
    parent_heading: Optional[str]  # For nesting

# Section classification
BODY_SECTIONS = ['introduction', 'background', 'results', 'discussion',
                 'methods', 'materials', 'experimental', 'conclusions']
META_SECTIONS = ['acknowledgements', 'contributions', 'author contributions',
                 'conflicts', 'competing interests', 'funding', 'declarations',
                 'data availability', 'code availability']
END_SECTIONS = ['references', 'bibliography', 'supplementary', 'appendix']

def classify_heading(text: str) -> str:
    normalized = text.lower().strip()
    if any(s in normalized for s in END_SECTIONS):
        return 'references' if 'ref' in normalized or 'bib' in normalized else 'supplementary'
    if any(s in normalized for s in META_SECTIONS):
        return 'meta'
    return 'body'

def detect_heading_level(font_size: float, is_bold: bool, numbering: str) -> int:
    """
    Determine heading hierarchy:
    - Level 1: Major sections (16pt+, bold, often numbered "1.", "2.")
    - Level 2: Subsections (14pt, bold, numbered "1.1", "2.1")
    - Level 3: Sub-subsections (12pt, bold, numbered "1.1.1")
    """
    if numbering and numbering.count('.') >= 2:
        return 3
    if numbering and numbering.count('.') == 1:
        return 2
    if font_size >= 16 and is_bold:
        return 1
    if font_size >= 14:
        return 2
    return 3
```

#### Phase 3: Document Reorganization
**New Stage (after Stage 8 - Split Sections):**
```python
def reorganize_sections(sections: Dict[str, ParsedSection],
                       headings: List[Heading]) -> NormalizedDocument:
    """
    Reorganize sections into standardized structure:
    1. Separate body/meta/references
    2. Nest subsections under parent sections
    3. Preserve original body section order
    4. Move meta sections after body
    """
    body_sections = []
    meta_sections = []
    references = None
    supplementary = None

    for heading in headings:
        section_content = sections.get(heading.text)
        if heading.section_type == 'body':
            body_sections.append(create_nested_section(heading, section_content))
        elif heading.section_type == 'meta':
            meta_sections.append(section_content)
        elif heading.section_type == 'references':
            references = section_content
        elif heading.section_type == 'supplementary':
            supplementary = section_content

    return NormalizedDocument(
        body=body_sections,  # Original order preserved
        meta=meta_sections,
        references=references,
        supplementary=supplementary
    )
```

#### Phase 4: Editor Notes Detection
**New detection in Stage 2 or Stage 6:**
```python
EDITOR_NOTE_PATTERNS = [
    r'(?i)elife\s+digest',
    r'(?i)editor.?s?\s+summary',
    r'(?i)significance\s+statement',
    r'(?i)plain\s+language\s+summary',
    r'bioRxiv preprint.*not certified by peer review'
]

def detect_editor_notes(markdown: str) -> Tuple[str, Optional[str]]:
    """
    Separate editor-added content from manuscript content.
    Returns: (cleaned_markdown, editor_notes)
    """
    # Extract and flag non-manuscript content
    # Remove from main document, store separately
```

### Data Model Changes

**Updated ParsedDocument:**
```python
@dataclass
class NormalizedDocument:
    # Metadata
    document_id: str
    title: str
    authors: AuthorBlock
    abstract: str

    # Main content (in original order, hierarchically nested)
    body_sections: List[NestedSection]

    # Post-body metadata
    meta_sections: List[ParsedSection]  # Contributions, acknowledgements, etc.

    # References
    references: List[BibliographyEntry]

    # Optional
    supplementary: Optional[ParsedSection]

    # Separated metadata
    figures: List[FigureBlock]  # Already implemented
    editor_notes: Optional[str]  # Non-manuscript content

@dataclass
class NestedSection:
    name: str
    level: int  # 1, 2, 3
    content: str
    sentences: List[Sentence]
    subsections: List[NestedSection]  # Recursive nesting
```

### Configuration

```yaml
normalization:
  extract_authors: true
  nest_subsections: true
  separate_meta_sections: true
  detect_editor_notes: true
  preserve_body_order: true  # Keep sections in original order
```

### Benefits

1. **Predictable Structure:** Downstream agents always know where to find information
2. **Clean Content:** Meta sections separated from scientific content
3. **Hierarchical Navigation:** Nested subsections enable better citation and reference
4. **Author Extraction:** Enables authorship analysis, corresponding author identification
5. **Editor Note Separation:** Prevents contamination of manuscript content with platform-specific additions

### Backward Compatibility

- Existing `ParsedDocument` structure remains
- `NormalizedDocument` embedded within ParsedDocument
- Config flag: `normalize_output: bool` (default: `true`)
- Raw markdown preserved for backward compatibility

### Implementation Plan

**Phase 1: Author/Affiliation Extraction (Stage 2 Enhancement)**
- Add author parsing to `analyze_structure()`
- Parse names, affiliations, emails, corresponding markers
- Store in StructureInfo
- Test on test PDFs

**Phase 2: Heading Classification (Stage 2 Enhancement)**
- Classify headings by type (body/meta/references/supplementary)
- Detect heading level (1, 2, 3) using font size + numbering
- Store classified headings in StructureInfo
- Test on test PDFs

**Phase 3: Editor Notes Detection (Stage 6 Enhancement)**
- Pattern matching in `cleanup_all()`
- Extract eLife Digest, Significance, bioRxiv warnings
- Return tuple: (clean_markdown, editor_notes)
- Test on test PDFs

**Phase 4: Subsection Nesting (Stage 8 Enhancement)**
- Build hierarchical structure in `split_sections()`
- Nest level 2/3 headings under parents
- Create NestedSection dataclass
- Test on test PDFs

**Phase 5: Document Normalization (New Stage 12)**
- Create `stages/normalization.py`
- Separate body/meta/references sections
- Preserve original body order
- Attach authors, figures, editor notes
- Return NormalizedDocument
- Test on test PDFs

**Phase 6: Integration (Stage 13 Update)**
- Embed NormalizedDocument in ParsedDocument
- Update builder.py
- Full test suite run
- Validate output structure

### Testing Requirements

After each phase, run full test suite:
1. Process all PDFs in `backend/docs/testPDFs/`
2. Validate output structure
3. Check for regressions (weird characters, jumbled sections, missing content)
4. Compare before/after for each phase

### Data Models to Implement

See code examples in sections above for:
- `Author`, `Affiliation`, `AuthorBlock`
- `Heading` (enhanced)
- `NestedSection`
- `NormalizedDocument`

---

## Multi-Rect Image Merging Enhancement (November 22, 2024)

### Problem
Scientific figures often contain multiple embedded images (subfigures like Fig 1A/1B, image layers, overlays). `get_images()` returns separate rects for each image, and the original code created individual `FigureRegion` objects for each rect. This left gaps between rects where text artifacts (axis labels, scattered chars) would slip through.

**Example:** test2.pdf had 105 images on page 1, with many multi-rect figures:
- Image 48: 2 rects
- Image 50: 6 rects
- Image 51: 6 rects

Without merging, each rect got its own small exclusion zone, leaving text visible in the gaps.

### Solution
Added `merge_overlapping_rects()` function in `stages/figures.py` to consolidate nearby/overlapping image rects into unified exclusion zones:

1. Collects ALL rects from ALL images on a page
2. Filters by size (≥150x100pt, 20k area)
3. Merges rects within proximity threshold (20pt)
4. Creates single FigureRegion for each merged group

**Algorithm:**
- Sort rects by vertical position (y0)
- Group rects that overlap or are within 20pt proximity
- Calculate unified bbox encompassing entire group
- Result: Comprehensive exclusion zones covering complete figures

### Test Results (November 22, 2024)
**Before:** Hundreds of scattered character artifacts across test files
**After:** Only 1 artifact across all 8 test PDFs (test3.pdf line 351: table axis labels)

**Improvement:** ~99.5% reduction in figure text artifacts

**Examples:**
- test.pdf: 0 artifacts (10 figures)
- test2.pdf: 0 artifacts (8 figures, many multi-rect)
- test3.pdf: 1 artifact (5 figures)
- test4-7: 0 artifacts each

**Debug output shows merging working:**
```
Page X: merged 47 rects into 8 regions
```

### Performance Impact
- Minimal overhead (~0.1s per page with figures)
- No change to caption detection or pairing logic
- All existing tests pass

### Margin Expansion (November 22, 2024 - Second Pass)
After initial implementation, increased exclusion zone margins to be more aggressive:
- **Previous:** top=10pt, bottom=30pt, sides=5pt
- **Current:** top=20pt, bottom=40pt, sides=15pt

This catches axis labels, tick marks, and other scattered text around figures. No performance degradation observed.

### Files Modified
- `backend/services/parser/pipeline/stages/figures.py:20-133,321-436,488-495` - Added merge_overlapping_rects(), refactored detect_image_regions(), increased margins
- `backend/services/parser/pipeline/PIPELINE_FLOW.md:70,76-89,875-925` - Updated Stage 3 documentation
