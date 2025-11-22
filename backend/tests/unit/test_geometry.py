"""Unit tests for geometry cleaning stage."""

import pytest
import pymupdf
from services.parser.pipeline.stages.geometry import (
    detect_line_numbers,
    crop_margins,
    analyze_geometry,
    apply_geometric_cleaning
)
from services.parser.pipeline.config import GeometryConfig


def create_pdf_with_line_numbers() -> pymupdf.Document:
    """Create a test PDF with line numbers in left margin."""
    doc = pymupdf.open()

    for page_num in range(3):
        page = doc.new_page()

        # Add line numbers (small digits in left margin)
        for line_num in range(1, 30):
            y_pos = 50 + (line_num * 15)
            page.insert_text((20, y_pos), str(line_num), fontsize=8)

        # Add main content
        page.insert_text((100, 100), "Main document content here" * 10, fontsize=12)

    return doc


def create_pdf_without_line_numbers() -> pymupdf.Document:
    """Create a test PDF without line numbers."""
    doc = pymupdf.open()

    for page_num in range(3):
        page = doc.new_page()
        # Only main content, no line numbers
        page.insert_text((72, 100), "Normal document content", fontsize=12)

    return doc


class TestDetectLineNumbers:
    """Tests for line number detection."""

    def test_detect_line_numbers_present(self):
        """Should detect line numbers when present."""
        doc = create_pdf_with_line_numbers()
        has_numbers, cutoff = detect_line_numbers(doc)

        assert has_numbers is True
        assert cutoff > 0  # Should suggest some cutoff position
        assert cutoff < 80  # Should be within expected range

        doc.close()

    def test_detect_line_numbers_absent(self):
        """Should not detect line numbers when absent."""
        doc = create_pdf_without_line_numbers()
        has_numbers, cutoff = detect_line_numbers(doc)

        assert has_numbers is False
        assert cutoff == 0

        doc.close()

    def test_detect_empty_document(self):
        """Should handle empty document gracefully."""
        doc = pymupdf.open()
        doc.new_page()  # Empty page

        has_numbers, cutoff = detect_line_numbers(doc)

        assert has_numbers is False
        assert cutoff == 0

        doc.close()


class TestCropMargins:
    """Tests for margin cropping."""

    def test_crop_margins_default(self):
        """Should crop margins with default values."""
        doc = create_pdf_without_line_numbers()
        original_rect = doc[0].rect

        doc = crop_margins(doc)

        cropped_rect = doc[0].cropbox

        # Check that cropbox was modified
        assert cropped_rect.y0 > original_rect.y0  # Top cropped
        assert cropped_rect.y1 < original_rect.y1  # Bottom cropped
        assert cropped_rect.y0 == original_rect.y0 + 60  # Default top margin
        assert cropped_rect.y1 == original_rect.y1 - 60  # Default bottom margin

        doc.close()

    def test_crop_margins_custom(self):
        """Should crop margins with custom values."""
        doc = create_pdf_without_line_numbers()
        original_rect = doc[0].rect

        doc = crop_margins(doc, top=100, bottom=50, left=30)

        cropped_rect = doc[0].cropbox

        assert cropped_rect.x0 == original_rect.x0 + 30  # Left cropped
        assert cropped_rect.y0 == original_rect.y0 + 100  # Top cropped
        assert cropped_rect.y1 == original_rect.y1 - 50  # Bottom cropped

        doc.close()

    def test_crop_margins_small_page(self):
        """Should skip cropping if page is too small."""
        # Create very small page
        doc = pymupdf.open()
        page = doc.new_page(width=200, height=150)  # Very small
        page.insert_text((50, 50), "Test", fontsize=10)

        original_rect = page.rect

        doc = crop_margins(doc, top=60, bottom=60)

        # Should not crop because page is too small
        cropped_rect = doc[0].cropbox

        # Cropbox should be same as original (not modified)
        assert abs(cropped_rect.y0 - original_rect.y0) < 1
        assert abs(cropped_rect.y1 - original_rect.y1) < 1

        doc.close()


class TestAnalyzeGeometry:
    """Tests for geometry analysis."""

    def test_analyze_geometry_with_line_numbers(self):
        """Should analyze document and detect line numbers."""
        doc = create_pdf_with_line_numbers()
        config = GeometryConfig(top_margin=60, bottom_margin=60, detect_line_numbers=True)

        geom_info = analyze_geometry(doc, config)

        assert geom_info.has_line_numbers is True
        assert geom_info.left_margin_cutoff > 0
        assert geom_info.top_margin == 60
        assert geom_info.bottom_margin == 60

        doc.close()

    def test_analyze_geometry_without_line_numbers(self):
        """Should analyze document and not detect line numbers."""
        doc = create_pdf_without_line_numbers()
        config = GeometryConfig(top_margin=50, bottom_margin=50, detect_line_numbers=True)

        geom_info = analyze_geometry(doc, config)

        assert geom_info.has_line_numbers is False
        assert geom_info.left_margin_cutoff == 0
        assert geom_info.top_margin == 50
        assert geom_info.bottom_margin == 50

        doc.close()

    def test_analyze_geometry_detection_disabled(self):
        """Should not detect line numbers when detection is disabled."""
        doc = create_pdf_with_line_numbers()
        config = GeometryConfig(detect_line_numbers=False)

        geom_info = analyze_geometry(doc, config)

        assert geom_info.has_line_numbers is False  # Detection disabled
        assert geom_info.left_margin_cutoff == 0

        doc.close()


class TestApplyGeometricCleaning:
    """Tests for complete geometric cleaning pipeline."""

    def test_apply_geometric_cleaning_full_pipeline(self):
        """Should run complete geometry cleaning pipeline."""
        doc = create_pdf_with_line_numbers()
        config = GeometryConfig(top_margin=60, bottom_margin=60, detect_line_numbers=True)

        original_rect = doc[0].rect

        cleaned_doc, geom_info = apply_geometric_cleaning(doc, config)

        # Check geometry was analyzed
        assert geom_info.has_line_numbers is True
        assert geom_info.left_margin_cutoff > 0

        # Check crops were applied
        cropped_rect = cleaned_doc[0].cropbox
        assert cropped_rect.x0 > original_rect.x0  # Left margin cropped
        assert cropped_rect.y0 > original_rect.y0  # Top margin cropped
        assert cropped_rect.y1 < original_rect.y1  # Bottom margin cropped

        cleaned_doc.close()

    def test_apply_geometric_cleaning_no_line_numbers(self):
        """Should clean document without line numbers."""
        doc = create_pdf_without_line_numbers()
        config = GeometryConfig()

        original_rect = doc[0].rect

        cleaned_doc, geom_info = apply_geometric_cleaning(doc, config)

        # No line numbers detected
        assert geom_info.has_line_numbers is False

        # But margins should still be cropped
        cropped_rect = cleaned_doc[0].cropbox
        assert cropped_rect.y0 == original_rect.y0 + 60  # Top cropped
        assert cropped_rect.y1 == original_rect.y1 - 60  # Bottom cropped
        assert cropped_rect.x0 == original_rect.x0  # Left not cropped

        cleaned_doc.close()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
