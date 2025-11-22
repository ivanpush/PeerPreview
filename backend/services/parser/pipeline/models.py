"""Data models for PDF parsing pipeline.

All dataclasses used throughout the pipeline for representing
parsed document structure and metadata.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


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
class BoldSpan:
    """Represents a bold text span detected in PDF."""
    text: str
    page: int
    font_size: float
    bbox: tuple  # (x0, y0, x1, y1)
    y_position: float


@dataclass
class SectionHeader:
    """Represents a detected section header."""
    text: str
    normalized_name: str
    page: int
    confidence: float  # 0-1, how confident we are this is a section


@dataclass
class GeometryInfo:
    """Geometric information detected from PDF."""
    has_line_numbers: bool
    left_margin_cutoff: float
    top_margin: float
    bottom_margin: float
    has_columns: bool = False
    column_count: int = 1


@dataclass
class StructureInfo:
    """Structure information detected via bold text analysis."""
    title: Optional[str]
    abstract: Optional[str]
    section_headers: List[SectionHeader]
    bold_spans: List[BoldSpan]


@dataclass
class Section:
    """Intermediate section representation during parsing."""
    name: str
    content: List[str]  # List of text chunks
    priority: int  # For ordering
