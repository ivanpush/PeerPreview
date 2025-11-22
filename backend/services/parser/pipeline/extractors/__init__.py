"""Metadata extractors for citations, figures, and bibliography.

These extractors analyze parsed text to extract structured metadata.
"""

from .citations import extract_citations
from .figures import extract_figures, extract_figure_blocks, extract_figure_references
from .bibliography import parse_bibliography, extract_doi

__all__ = [
    'extract_citations',
    'extract_figures',
    'extract_figure_blocks',
    'extract_figure_references',
    'parse_bibliography',
    'extract_doi',
]
