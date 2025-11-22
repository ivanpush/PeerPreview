"""PDF loading stage.

Handles loading PDF bytes into pymupdf Document objects
and extracting basic metadata.
"""

import pymupdf
from typing import Dict
import logging

logger = logging.getLogger(__name__)


def load_pdf(pdf_bytes: bytes) -> pymupdf.Document:
    """Load PDF from bytes into pymupdf Document.

    Args:
        pdf_bytes: Raw PDF file bytes

    Returns:
        pymupdf.Document object

    Raises:
        ValueError: If PDF is invalid or cannot be loaded
    """
    try:
        doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
        logger.info(f"Loaded PDF: {doc.page_count} pages")
        return doc
    except Exception as e:
        logger.error(f"Failed to load PDF: {e}")
        raise ValueError(f"Invalid PDF file: {e}")


def extract_metadata(doc: pymupdf.Document) -> Dict:
    """Extract basic metadata from PDF document.

    Args:
        doc: pymupdf Document

    Returns:
        Dictionary with metadata fields:
        - page_count: int
        - author: str (if available)
        - title: str (if available from PDF metadata)
        - subject: str (if available)
        - creator: str (if available)
    """
    metadata = {
        'page_count': doc.page_count
    }

    # Extract PDF metadata if available
    pdf_metadata = doc.metadata
    if pdf_metadata:
        metadata['pdf_author'] = pdf_metadata.get('author', '')
        metadata['pdf_title'] = pdf_metadata.get('title', '')
        metadata['pdf_subject'] = pdf_metadata.get('subject', '')
        metadata['pdf_creator'] = pdf_metadata.get('creator', '')

    logger.info(f"Extracted metadata: {metadata}")
    return metadata


def validate_pdf(doc: pymupdf.Document) -> bool:
    """Validate that PDF document is suitable for parsing.

    Args:
        doc: pymupdf Document

    Returns:
        True if PDF is valid and can be parsed

    Raises:
        ValueError: If PDF fails validation with error message
    """
    if doc.page_count == 0:
        raise ValueError("PDF has no pages")

    if doc.page_count > 1000:
        logger.warning(f"PDF has {doc.page_count} pages, which is unusually large")

    # Check if first page has text
    first_page = doc[0]
    text = first_page.get_text("text")

    if len(text.strip()) < 10:
        raise ValueError("PDF appears to be scanned images without extractable text")

    logger.info("PDF validation passed")
    return True
