# PDF Parser Pipeline - Usage Guide

## Basic Usage

### Using Default Configuration

```python
from services.parser.pipeline import PipelineBuilder, default_config

# Create builder with defaults
builder = PipelineBuilder(default_config())

# Parse a PDF
with open("paper.pdf", "rb") as f:
    pdf_bytes = f.read()

parsed_doc = builder.build(pdf_bytes, "paper.pdf")

# Access parsed data
print(f"Title: {parsed_doc.title}")
print(f"Sections: {list(parsed_doc.sections.keys())}")
print(f"Citations: {len(parsed_doc.citations)}")
print(f"Figures: {len(parsed_doc.figures)}")
```

### Using Custom YAML Configuration

```python
from pathlib import Path
from services.parser.pipeline import PipelineBuilder, load_config_from_yaml

# Load custom config from YAML
config = load_config_from_yaml(Path("my_config.yaml"))
if config is None:
    # Fallback to defaults if YAML fails to load
    from services.parser.pipeline import default_config
    config = default_config()

builder = PipelineBuilder(config)
parsed_doc = builder.build(pdf_bytes, "paper.pdf")
```

### Using Programmatic Configuration

```python
from services.parser.pipeline import PipelineBuilder, PipelineConfig, GeometryConfig, CleanupConfig

# Create custom config
config = PipelineConfig(
    geometry=GeometryConfig(
        top_margin=100,  # More aggressive top cropping
        bottom_margin=80
    ),
    cleanup=CleanupConfig(
        remove_figure_blocks=False,  # Keep figure blocks
        remove_urls=True  # Remove URLs
    ),
    debug_logging=True
)

builder = PipelineBuilder(config)
```

## Accessing Parsed Data

### Sections

```python
# Iterate through sections
for name, section in parsed_doc.sections.items():
    print(f"\n### {section.name}")
    print(f"Length: {len(section.text)} chars")

    # Access sentences if indexing enabled
    if section.sentences:
        print(f"Sentences: {len(section.sentences)}")
        for sent in section.sentences[:3]:
            print(f"  {sent.index}: {sent.text[:50]}...")
```

### Citations

```python
# Access citation references
for citation in parsed_doc.citations:
    print(f"[{citation.ref_id}] in section '{citation.section}'")
    print(f"  Sentence {citation.sentence_idx}: {citation.context}")
```

### Figures

```python
# Access figure metadata
for fig in parsed_doc.figures:
    print(f"{fig.label}: {fig.caption[:80]}...")

# Access figure references in text
for ref in parsed_doc.figure_refs:
    print(f"Figure {ref.figure_id} referenced in {ref.section}")
```

### Bibliography

```python
# Access bibliography entries
for entry in parsed_doc.bibliography:
    print(f"[{entry.ref_num}] {entry.authors} ({entry.year})")
    print(f"  {entry.title}")
    if entry.doi:
        print(f"  DOI: {entry.doi}")
```

### Raw Markdown

```python
# Get the full cleaned markdown
markdown = parsed_doc.raw_markdown
print(markdown[:1000])
```

## Configuration Options

See `parser_config.yaml` for a complete template with all available options.

### Key Configuration Sections

**Geometry** - Control PDF cropping
- `top_margin`: Points to crop from top (default: 60)
- `bottom_margin`: Points to crop from bottom (default: 60)

**Analysis** - Structure detection
- `detect_bold_text`: Use bold text for structure (default: true)
- `extract_title`: Extract title from bold text (default: true)
- `min_title_font_size`: Minimum font size for titles (default: 14.0)

**Cleanup** - Artifact removal
- `remove_figure_blocks`: Remove figure/table blocks (default: true)
- `remove_headers_footers`: Remove repeated headers/footers (default: true)
- `remove_copyright`: Remove copyright notices (default: true)
- `remove_affiliations`: Remove author affiliations (default: true)

**Indexing** - Sentence tokenization
- `enable_sentence_indexing`: Enable sentence-level indexing (default: true)
- `use_nltk`: Use NLTK for tokenization (default: true)

**Extraction** - Metadata extraction
- `extract_citations`: Extract citation references (default: true)
- `extract_figures`: Extract figure references (default: true)
- `extract_bibliography`: Extract bibliography entries (default: true)

## Backward Compatibility

The old API is still supported:

```python
# Old PdfParser interface
from services.parser.pdf_parser import PdfParser

parser = PdfParser()
markdown = parser.parse(pdf_bytes)  # Returns raw markdown string

# Old DocumentBuilder/EnhancedDocumentBuilder interface
from services.parser.pdf_parser import DocumentBuilder

builder = DocumentBuilder()
parsed_doc = builder.build(pdf_bytes, "paper.pdf")
```

## Pipeline Stages

The pipeline runs these stages in order:

1. **Loader** - Load PDF, extract metadata, validate
2. **Analysis** - Detect structure via bold text analysis
3. **Geometry** - Crop margins, remove line numbers
4. **Extraction** - Convert PDF to markdown via pymupdf4llm
5. **Reflow** - Reconstruct paragraphs from line breaks
6. **Cleanup** - Remove 22+ artifact patterns
7. **Formatting** - Split into sections, validate structure
8. **Indexing** - Tokenize sentences with NLTK
9. **Metadata Extraction** - Extract citations, figures, bibliography
10. **Assembly** - Build final ParsedDocument

Each stage is independently testable and configurable.

## Testing

Run all pipeline tests:

```bash
# All unit tests
python -m pytest tests/unit/ -v

# Specific stage tests
python -m pytest tests/unit/test_geometry.py -v
python -m pytest tests/unit/test_cleanup.py -v
python -m pytest tests/unit/test_config.py -v

# Integration test with real PDF
python test_parser.py docs/testPDFs/test.pdf
```

## Debugging

Enable debug logging:

```python
config = PipelineConfig(debug_logging=True)
builder = PipelineBuilder(config)
```

Or in YAML:

```yaml
debug_logging: true
```

This will log each pipeline stage's progress and statistics.
