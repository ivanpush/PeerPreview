"""Unit tests for PDF loader stage."""

import pytest
import pymupdf
from services.parser.pipeline.stages.loader import (
    load_pdf,
    extract_metadata,
    validate_pdf
)


def create_test_pdf() -> bytes:
    """Create a minimal valid PDF for testing."""
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Test PDF Content", fontsize=12)
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


def create_empty_pdf() -> bytes:
    """Create a PDF with no text (should fail validation)."""
    doc = pymupdf.open()
    doc.new_page()  # Empty page
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


class TestLoadPdf:
    """Tests for load_pdf function."""

    def test_load_valid_pdf(self):
        """Should successfully load a valid PDF."""
        pdf_bytes = create_test_pdf()
        doc = load_pdf(pdf_bytes)

        assert doc is not None
        assert doc.page_count == 1
        doc.close()

    def test_load_invalid_bytes(self):
        """Should raise ValueError for invalid PDF bytes."""
        invalid_bytes = b"This is not a PDF"

        with pytest.raises(ValueError, match="Invalid PDF file"):
            load_pdf(invalid_bytes)

    def test_load_empty_bytes(self):
        """Should raise ValueError for empty bytes."""
        with pytest.raises(ValueError):
            load_pdf(b"")


class TestExtractMetadata:
    """Tests for extract_metadata function."""

    def test_extract_basic_metadata(self):
        """Should extract page count."""
        pdf_bytes = create_test_pdf()
        doc = load_pdf(pdf_bytes)

        metadata = extract_metadata(doc)

        assert 'page_count' in metadata
        assert metadata['page_count'] == 1
        doc.close()

    def test_extract_pdf_metadata(self):
        """Should extract PDF metadata fields if present."""
        # Create PDF with metadata
        doc = pymupdf.open()
        page = doc.new_page()
        page.insert_text((72, 72), "Test", fontsize=12)

        # Set metadata
        doc.set_metadata({
            'author': 'Test Author',
            'title': 'Test Title',
            'subject': 'Test Subject'
        })

        pdf_bytes = doc.tobytes()
        doc.close()

        # Load and extract
        doc = load_pdf(pdf_bytes)
        metadata = extract_metadata(doc)

        assert metadata.get('pdf_author') == 'Test Author'
        assert metadata.get('pdf_title') == 'Test Title'
        assert metadata.get('pdf_subject') == 'Test Subject'
        doc.close()


class TestValidatePdf:
    """Tests for validate_pdf function."""

    def test_validate_normal_pdf(self):
        """Should pass validation for normal PDF."""
        pdf_bytes = create_test_pdf()
        doc = load_pdf(pdf_bytes)

        assert validate_pdf(doc) is True
        doc.close()

    def test_validate_empty_pdf(self):
        """Should fail validation for PDF with no text."""
        pdf_bytes = create_empty_pdf()
        doc = load_pdf(pdf_bytes)

        with pytest.raises(ValueError, match="scanned images"):
            validate_pdf(doc)

        doc.close()

    def test_validate_multi_page_pdf(self):
        """Should pass validation for multi-page PDF."""
        doc = pymupdf.open()
        for i in range(5):
            page = doc.new_page()
            # Add more text to pass validation (needs > 10 chars)
            page.insert_text((72, 72), f"Page {i+1} content with enough text", fontsize=12)

        pdf_bytes = doc.tobytes()
        doc.close()

        doc = load_pdf(pdf_bytes)
        metadata = extract_metadata(doc)

        assert metadata['page_count'] == 5
        assert validate_pdf(doc) is True
        doc.close()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
