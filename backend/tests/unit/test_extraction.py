"""Unit tests for text extraction stage."""

import pytest
import pymupdf
from services.parser.pipeline.stages.extraction import (
    extract_markdown,
    extract_text_by_page,
    extract_text_raw
)


def create_test_pdf() -> pymupdf.Document:
    """Create a simple test PDF."""
    doc = pymupdf.open()

    # Page 1
    page1 = doc.new_page()
    page1.insert_text((72, 72), "Page 1: Test content", fontsize=12)
    page1.insert_text((72, 100), "This is the first page.", fontsize=10)

    # Page 2
    page2 = doc.new_page()
    page2.insert_text((72, 72), "Page 2: More content", fontsize=12)
    page2.insert_text((72, 100), "This is the second page.", fontsize=10)

    return doc


class TestExtractMarkdown:
    """Tests for markdown extraction."""

    def test_extract_markdown_basic(self):
        """Should extract markdown from PDF."""
        doc = create_test_pdf()

        markdown = extract_markdown(doc)

        assert markdown is not None
        assert len(markdown) > 0
        assert isinstance(markdown, str)

        doc.close()

    def test_extract_markdown_contains_content(self):
        """Should extract actual PDF content."""
        doc = create_test_pdf()

        markdown = extract_markdown(doc)

        # Should contain text from the PDF
        assert "Page 1" in markdown or "Test content" in markdown

        doc.close()

    def test_extract_empty_pdf(self):
        """Should handle empty PDF gracefully."""
        doc = pymupdf.open()
        doc.new_page()  # Empty page

        markdown = extract_markdown(doc)

        # Should return empty or minimal markdown
        assert isinstance(markdown, str)

        doc.close()


class TestExtractTextByPage:
    """Tests for page-by-page text extraction."""

    def test_extract_text_by_page(self):
        """Should extract text from each page separately."""
        doc = create_test_pdf()

        pages = extract_text_by_page(doc)

        assert len(pages) == 2  # Two pages
        assert isinstance(pages[0], str)
        assert isinstance(pages[1], str)

        doc.close()

    def test_page_text_contains_content(self):
        """Should extract actual page content."""
        doc = create_test_pdf()

        pages = extract_text_by_page(doc)

        # Each page should have some content
        assert len(pages[0]) > 0
        assert len(pages[1]) > 0

        # Pages should be different
        assert pages[0] != pages[1]

        doc.close()

    def test_extract_single_page(self):
        """Should handle single page PDF."""
        doc = pymupdf.open()
        page = doc.new_page()
        page.insert_text((72, 72), "Single page content", fontsize=12)

        pages = extract_text_by_page(doc)

        assert len(pages) == 1
        assert "Single page" in pages[0]

        doc.close()

    def test_extract_empty_pages(self):
        """Should handle empty pages."""
        doc = pymupdf.open()
        doc.new_page()  # Empty page
        doc.new_page()  # Another empty page

        pages = extract_text_by_page(doc)

        assert len(pages) == 2
        # Empty pages should return empty strings
        assert pages[0] == ""
        assert pages[1] == ""

        doc.close()


class TestExtractTextRaw:
    """Tests for raw text extraction."""

    def test_extract_text_raw(self):
        """Should extract all text as single string."""
        doc = create_test_pdf()

        text = extract_text_raw(doc)

        assert isinstance(text, str)
        assert len(text) > 0

        doc.close()

    def test_raw_text_combines_pages(self):
        """Should combine text from all pages."""
        doc = create_test_pdf()

        text = extract_text_raw(doc)

        # Should contain content from both pages
        # (exact format depends on PDF rendering)
        assert len(text) > 20  # Some content extracted

        doc.close()

    def test_raw_text_empty_pdf(self):
        """Should handle empty PDF."""
        doc = pymupdf.open()
        doc.new_page()

        text = extract_text_raw(doc)

        assert isinstance(text, str)
        # Empty page returns empty or whitespace

        doc.close()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
