"""Unit tests for formatting stage."""

import pytest
from services.parser.pipeline.stages.formatting import (
    split_sections,
    normalize_section_name,
    validate_required_sections,
    detect_section_by_keywords,
    format_sections
)
from services.parser.pipeline.models import ParsedSection
from services.parser.pipeline.config import SectionConfig


class TestSplitSections:
    """Tests for section splitting."""

    def test_split_basic_sections(self):
        """Should split markdown by section headers."""
        markdown = """### **INTRODUCTION**

Intro content here.

### **METHODS**

Methods content here."""

        sections = split_sections(markdown)

        assert 'introduction' in sections
        assert 'methods' in sections
        assert 'Intro content' in sections['introduction'].text
        assert 'Methods content' in sections['methods'].text

    def test_handle_preamble(self):
        """Should capture content before first section."""
        markdown = """Title and preamble content.

### **INTRODUCTION**

Intro content."""

        sections = split_sections(markdown)

        assert 'preamble' in sections
        assert 'Title and preamble' in sections['preamble'].text

    def test_no_sections(self):
        """Should handle document without sections."""
        markdown = "Just plain text without sections."

        sections = split_sections(markdown)

        # Content without section headers goes into preamble
        assert 'preamble' in sections
        assert sections['preamble'].text == markdown

    def test_section_priority(self):
        """Should assign priority from config."""
        markdown = """### **ABSTRACT**

Abstract text.

### **REFERENCES**

References."""

        sections = split_sections(markdown)

        # Abstract should have lower priority (earlier) than references
        assert sections['abstract'].order_priority < sections['references'].order_priority


class TestNormalizeSectionName:
    """Tests for section name normalization."""

    def test_lowercase(self):
        """Should convert to lowercase."""
        assert normalize_section_name("INTRODUCTION") == "introduction"

    def test_replace_spaces(self):
        """Should replace spaces with underscores."""
        assert normalize_section_name("Materials and Methods") == "materials_and_methods"

    def test_replace_hyphens(self):
        """Should replace hyphens with underscores."""
        assert normalize_section_name("Results-Discussion") == "results_discussion"

    def test_handle_variations(self):
        """Should handle common variations."""
        assert normalize_section_name("acknowledgments") == "acknowledgements"
        assert normalize_section_name("conclusion") == "conclusions"
        assert normalize_section_name("reference") == "references"


class TestValidateRequiredSections:
    """Tests for section validation."""

    def test_validate_all_present(self):
        """Should validate when all required sections present."""
        sections = {
            'introduction': ParsedSection('introduction', 'text', []),
            'methods': ParsedSection('methods', 'text', []),
            'results': ParsedSection('results', 'text', []),
            'discussion': ParsedSection('discussion', 'text', [])
        }

        validation = validate_required_sections(sections)

        assert validation['has_introduction'] is True
        assert validation['has_methods'] is True
        assert validation['has_results'] is True
        assert validation['has_discussion'] is True

    def test_validate_missing_section(self):
        """Should detect missing required sections."""
        sections = {
            'introduction': ParsedSection('introduction', 'text', []),
            'results': ParsedSection('results', 'text', [])
        }

        validation = validate_required_sections(sections)

        assert validation['has_introduction'] is True
        assert validation['has_methods'] is False  # Missing
        assert validation['has_results'] is True
        assert validation['has_discussion'] is False  # Missing

    def test_accept_variations(self):
        """Should accept section name variations."""
        sections = {
            'materials_and_methods': ParsedSection('materials_and_methods', 'text', [])
        }

        validation = validate_required_sections(sections)

        # materials_and_methods should satisfy methods requirement
        assert validation['has_methods'] is True


class TestDetectSectionByKeywords:
    """Tests for keyword-based section detection."""

    def test_detect_acknowledgements(self):
        """Should detect acknowledgements by keywords."""
        text = "We thank the funding agency for support..."
        result = detect_section_by_keywords(text)

        assert result == 'acknowledgements'

    def test_detect_author_contributions(self):
        """Should detect author contributions."""
        text = "Authors contributed as follows: A designed experiments..."
        result = detect_section_by_keywords(text)

        assert result == 'author_contributions'

    def test_detect_competing_interests(self):
        """Should detect competing interests."""
        text = "The authors declare no conflict of interest."
        result = detect_section_by_keywords(text)

        assert result == 'competing_interests'

    def test_detect_data_availability(self):
        """Should detect data availability."""
        text = "Data are available in the repository..."
        result = detect_section_by_keywords(text)

        assert result == 'data_availability'

    def test_detect_funding(self):
        """Should detect funding statements."""
        text = "This work was funded by NIH grant..."
        result = detect_section_by_keywords(text)

        assert result == 'funding'

    def test_no_match(self):
        """Should return None when no keywords match."""
        text = "This is regular content without special keywords."
        result = detect_section_by_keywords(text)

        assert result is None


class TestFormatSections:
    """Tests for section formatting."""

    def test_format_basic(self):
        """Should format sections to markdown."""
        sections = {
            'introduction': ParsedSection('introduction', 'Intro text', [], order_priority=10),
            'methods': ParsedSection('methods', 'Methods text', [], order_priority=20)
        }

        result = format_sections(sections)

        assert '### **INTRODUCTION**' in result
        assert '### **METHODS**' in result
        assert 'Intro text' in result
        assert 'Methods text' in result

    def test_format_respects_priority(self):
        """Should order sections by priority."""
        sections = {
            'methods': ParsedSection('methods', 'Methods', [], order_priority=20),
            'abstract': ParsedSection('abstract', 'Abstract', [], order_priority=1)
        }

        result = format_sections(sections)

        # Abstract (priority 1) should come before Methods (priority 20)
        abstract_pos = result.find('ABSTRACT')
        methods_pos = result.find('METHODS')
        assert abstract_pos < methods_pos

    def test_format_preamble_no_header(self):
        """Should not add header for preamble."""
        sections = {
            'preamble': ParsedSection('preamble', 'Preamble text', [], order_priority=0)
        }

        result = format_sections(sections)

        # Preamble should have no header
        assert '### **PREAMBLE**' not in result
        assert 'Preamble text' in result


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
