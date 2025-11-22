"""PDF Parser - Backward Compatibility Facade.

This module maintains backward compatibility with the existing API
while using the new modular pipeline architecture internally.

The legacy monolithic implementation has been refactored into:
- services/parser/pipeline/

See REFACTOR_STATUS.md for details.
"""

from .pipeline import PipelineBuilder, default_config, ParsedDocument

# Backward compatibility aliases
EnhancedDocumentBuilder = PipelineBuilder
DocumentBuilder = PipelineBuilder


# Legacy PdfParser class for test_parser.py compatibility
class PdfParser:
    """Legacy parser interface that returns raw markdown."""

    def __init__(self):
        self.builder = PipelineBuilder(default_config())

    def parse(self, pdf_bytes: bytes) -> str:
        """Parse PDF and return markdown string.

        Args:
            pdf_bytes: Raw PDF file bytes

        Returns:
            Markdown string
        """
        # Use pipeline to get full ParsedDocument
        parsed_doc = self.builder.build(pdf_bytes, "document.pdf")

        # Return just the raw markdown for backward compatibility
        return parsed_doc.raw_markdown


# Expose key classes for external imports
__all__ = [
    'PdfParser',
    'DocumentBuilder',
    'EnhancedDocumentBuilder',
    'PipelineBuilder',
    'ParsedDocument',
]
