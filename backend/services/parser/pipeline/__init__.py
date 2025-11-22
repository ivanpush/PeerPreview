"""Modular PDF parsing pipeline for scientific papers.

This package provides a staged pipeline architecture for parsing PDF documents
into structured data with sections, sentences, citations, and figures.

Pipeline Stages:
1. Loader - PDF loading and metadata extraction
2. Geometry - Geometric cleaning (line numbers, margins)
3. Analysis - Structure detection via bold text
4. Extraction - Text extraction to markdown
5. Reflow - Paragraph reconstruction
6. Cleanup - Artifact removal
7. Formatting - Section parsing and validation
8. Indexing - Sentence tokenization and metadata extraction
"""

# Only import what exists
from .config import PipelineConfig, default_config, load_config_from_yaml
from .models import ParsedDocument, ParsedSection, Sentence

__all__ = [
    'PipelineConfig',
    'default_config',
    'load_config_from_yaml',
    'ParsedDocument',
    'ParsedSection',
    'Sentence',
]

# Import builder
from .builder import PipelineBuilder
__all__.append('PipelineBuilder')
