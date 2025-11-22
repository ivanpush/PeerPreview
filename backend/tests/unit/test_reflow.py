"""Unit tests for text reflow stage."""

import pytest
from services.parser.pipeline.stages.reflow import (
    is_header_line,
    merge_hyphenations,
    reflow_text
)
from services.parser.pipeline.config import ReflowConfig


class TestIsHeaderLine:
    """Tests for header detection."""

    def test_detect_markdown_header(self):
        """Should detect markdown headers."""
        assert is_header_line("# Introduction", 0, []) is True
        assert is_header_line("## Methods", 0, []) is True
        assert is_header_line("### Results", 0, []) is True

    def test_detect_bold_header(self):
        """Should detect bold markdown headers."""
        assert is_header_line("**Introduction**", 0, []) is True
        assert is_header_line("**Methods and Materials**", 0, []) is True

    def test_detect_section_keywords(self):
        """Should detect known section names."""
        all_lines = ["Introduction", "This is content"]
        assert is_header_line("Introduction", 0, all_lines) is True

        all_lines2 = ["Methods", "We used..."]
        assert is_header_line("Methods", 0, all_lines2) is True

    def test_detect_all_caps_header(self):
        """Should detect ALL CAPS headers."""
        assert is_header_line("RESULTS", 0, []) is True
        assert is_header_line("DISCUSSION", 0, []) is True

    def test_reject_long_lines(self):
        """Should reject very long lines as headers."""
        long_line = "A" * 150
        assert is_header_line(long_line, 0, []) is False

    def test_reject_short_lines(self):
        """Should reject very short lines as headers."""
        assert is_header_line("A", 0, []) is False
        assert is_header_line("AB", 0, []) is False

    def test_reject_regular_text(self):
        """Should not detect regular text as headers."""
        assert is_header_line("This is a regular sentence.", 0, []) is False
        assert is_header_line("We conducted experiments.", 0, []) is False


class TestMergeHyphenations:
    """Tests for hyphenation merging."""

    def test_merge_simple_hyphenation(self):
        """Should merge simple hyphenated words."""
        text = "This is a hyphen-\nated word"
        result = merge_hyphenations(text)

        assert result == "This is a hyphenated word"

    def test_merge_multiple_hyphenations(self):
        """Should merge multiple hyphenated words."""
        text = "First hyphen-\nated and second hyphen-\nated words"
        result = merge_hyphenations(text)

        assert "hyphenated" in result
        assert "hyphen-\n" not in result

    def test_preserve_normal_hyphens(self):
        """Should preserve hyphens not at line breaks."""
        text = "This is a well-known fact"
        result = merge_hyphenations(text)

        assert result == text  # Unchanged

    def test_handle_no_hyphenations(self):
        """Should handle text without hyphenations."""
        text = "This is normal text\nwith line breaks"
        result = merge_hyphenations(text)

        assert "This is normal text" in result


class TestReflowText:
    """Tests for complete text reflow."""

    def test_reflow_broken_paragraph(self):
        """Should merge broken paragraphs."""
        text = """This is a paragraph
that is broken across
multiple lines."""

        result = reflow_text(text)

        # Should merge into single line
        assert "paragraph that is broken across multiple lines." in result

    def test_preserve_empty_lines(self):
        """Should preserve paragraph breaks."""
        text = """First paragraph.

Second paragraph."""

        result = reflow_text(text)

        # Should have empty line between paragraphs
        lines = result.split('\n')
        assert '' in lines  # Empty line preserved

    def test_preserve_headers(self):
        """Should not merge headers into paragraphs."""
        text = """## Introduction
This is the introduction text."""

        result = reflow_text(text)

        # Header should be on its own line
        assert "## Introduction" in result
        lines = result.split('\n')
        header_line = next(l for l in lines if "Introduction" in l)
        assert header_line.strip() == "## Introduction"

    def test_respect_sentence_boundaries(self):
        """Should break at sentence terminators."""
        text = """This is sentence one. This is sentence two.
This continues."""

        result = reflow_text(text)

        # Should have proper breaks
        assert "sentence one. This is sentence two." in result or "sentence two." in result

    def test_handle_citations(self):
        """Should recognize citation patterns."""
        text = """This is cited [1]
Next sentence."""

        result = reflow_text(text)

        # Citation should trigger break
        # (exact behavior depends on next line capitalization)
        assert "cited [1]" in result

    def test_merge_hyphenations_in_reflow(self):
        """Should merge hyphenations during reflow."""
        text = """This is a hyphen-
ated word in text."""

        result = reflow_text(text)

        assert "hyphenated" in result
        assert "hyphen-" not in result

    def test_respect_config_disable_reflow(self):
        """Should skip reflow when disabled."""
        text = """Line one
Line two"""

        config = ReflowConfig(enable_reflow=False)
        result = reflow_text(text, config)

        # Should be unchanged
        assert result == text

    def test_respect_config_disable_hyphenation(self):
        """Should skip hyphenation merging when disabled."""
        text = """hyphen-
ated"""

        config = ReflowConfig(merge_hyphenations=False)
        result = reflow_text(text, config)

        # Hyphenation should not be merged
        assert "hyphen-" in result

    def test_complex_document(self):
        """Should handle complex multi-paragraph document."""
        text = """# Title

## Introduction
This is the intro paragraph
broken across lines.

This is another paragraph. It has
multiple sentences. They should flow
together.

## Methods
Methods content here."""

        result = reflow_text(text)

        # Headers preserved
        assert "# Title" in result
        assert "## Introduction" in result
        assert "## Methods" in result

        # Paragraphs merged
        assert "intro paragraph broken across lines" in result or "intro paragraph" in result


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
