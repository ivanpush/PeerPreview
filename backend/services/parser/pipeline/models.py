"""Data models for PDF parsing pipeline.

All dataclasses used throughout the pipeline for representing
parsed document structure and metadata.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class ParsedSection:
    """Represents a document section with indexed sentences."""
    name: str
    text: str
    sentences: List['Sentence'] = field(default_factory=list)
    order_priority: int = 100  # For section reordering


@dataclass
class Sentence:
    """Represents an indexed sentence within a section."""
    id: str
    section: str
    text: str
    char_start: int
    char_end: int
    paragraph_index: int


@dataclass
class CitationRef:
    """Represents an in-text citation reference."""
    id: str
    section: str
    sentence_id: str
    sentence_text: str


@dataclass
class FigureBlock:
    """Represents a figure with caption extracted from PDF."""
    id: str
    label: str
    caption: str
    page: int


@dataclass
class FigureRef:
    """Represents a reference to a figure in text."""
    label: str
    section: str
    sentence_id: str
    sentence_text: str


@dataclass
class BibliographyEntry:
    """Represents a bibliography/reference entry."""
    id: str
    raw_text: str
    doi: Optional[str] = None


@dataclass
class ParsedDocument:
    """Complete parsed document with all extracted metadata.

    This is the final output of the parsing pipeline.
    """
    doc_id: str
    doc_hash: str
    title: str
    sections: Dict[str, ParsedSection]
    figures: List[FigureBlock]
    figure_refs: List[FigureRef]
    citations: List[CitationRef]
    bibliography: List[BibliographyEntry]
    raw_markdown: str


# Pipeline stage intermediate data structures

@dataclass
class Author:
    """Represents a parsed author with affiliation markers."""
    name: str
    affiliation_markers: List[str] = field(default_factory=list)  # ['1', '2', '*']
    is_corresponding: bool = False
    email: Optional[str] = None


@dataclass
class AuthorResult:
    """Result of author detection with confidence scoring."""
    authors: List[Author]
    text: str  # Raw text for debugging
    detection_method: str
    confidence: float
    blocks: List['BoldSpan'] = field(default_factory=list)  # Source blocks for debugging


@dataclass
class BoldSpan:
    """Represents a bold text span detected in PDF."""
    text: str
    page: int
    font_size: float
    bbox: tuple  # (x0, y0, x1, y1)
    y_position: float
    x_position: float = 0.0  # x0 from bbox
    height: float = 0.0  # bbox[3] - bbox[1]


@dataclass
class SectionHeader:
    """Represents a detected section header."""
    text: str
    normalized_name: str
    page: int
    confidence: float  # 0-1, how confident we are this is a section


@dataclass
class FigureCaption:
    """Detected figure caption with spatial metadata."""
    text: str                    # Full caption text
    figure_type: str            # 'Figure', 'Fig', 'Table', 'Scheme'
    figure_num: str             # '1', '2A', 'S3', etc.
    page: int                   # Page number
    bbox: Tuple[float, float, float, float]  # Bounding box (x0, y0, x1, y1)
    y_position: float           # Vertical position for proximity matching
    is_bold: bool              # Whether caption is bold
    confidence: float          # Detection confidence (0-1)
    is_standalone: bool        # True if caption is on its own line


@dataclass
class FigureRegion:
    """Detected or inferred figure region for exclusion."""
    bbox: Tuple[float, float, float, float]  # Exclusion zone (x0, y0, x1, y1)
    page: int                   # Page number
    detection_method: str       # 'image', 'drawing', 'caption_inferred', 'synthetic'
    confidence: float          # Detection confidence (0-1)
    has_actual_figure: bool    # True if real image/drawing found
    associated_caption: Optional['FigureCaption'] = None
    exclusion_margin: Tuple[float, float, float, float] = (10, 30, 5, 5)  # top, bottom, left, right


@dataclass
class GeometryInfo:
    """Geometric information detected from PDF."""
    has_line_numbers: bool
    left_margin_cutoff: float
    top_margin: float
    bottom_margin: float
    has_columns: bool = False
    column_count: int = 1
    figure_captions: List[FigureCaption] = field(default_factory=list)
    figure_regions: List[FigureRegion] = field(default_factory=list)


@dataclass
class StructureInfo:
    """Structure information detected via bold text analysis."""
    title: Optional[str]
    abstract: Optional[str]
    section_headers: List[SectionHeader]
    bold_spans: List[BoldSpan]
    authors: Optional['AuthorResult'] = None  # Phase 4: Detected authors


@dataclass
class Section:
    """Intermediate section representation during parsing."""
    name: str
    content: List[str]  # List of text chunks
    priority: int  # For ordering
