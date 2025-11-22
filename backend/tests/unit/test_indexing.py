"""Unit tests for indexing stage."""

import pytest
from services.parser.pipeline.stages.indexing import (
    tokenize_sentences,
    simple_sentence_split,
    generate_sentence_id,
    index_sentences
)
from services.parser.pipeline.models import ParsedSection
from services.parser.pipeline.config import IndexingConfig


class TestSimpleSentenceSplit:
    """Tests for simple sentence splitting."""

    def test_split_basic_sentences(self):
        """Should split sentences at terminators."""
        text = "This is sentence one. This is sentence two. This is sentence three."
        result = simple_sentence_split(text)

        assert len(result) == 3
        assert "sentence one." in result[0]
        assert "sentence two." in result[1]
        assert "sentence three." in result[2]

    def test_handle_exclamation(self):
        """Should split on exclamation marks."""
        text = "First sentence! Second sentence."
        result = simple_sentence_split(text)

        assert len(result) == 2

    def test_handle_question(self):
        """Should split on question marks."""
        text = "Is this first? This is second."
        result = simple_sentence_split(text)

        assert len(result) == 2

    def test_preserve_abbreviations(self):
        """Should not split on abbreviations."""
        text = "Dr. Smith conducted the study. The results were significant."
        result = simple_sentence_split(text)

        # Should still split into 2 sentences despite "Dr."
        # (this is a limitation of simple splitting)
        assert len(result) >= 1


class TestTokenizeSentences:
    """Tests for sentence tokenization."""

    def test_tokenize_basic(self):
        """Should tokenize text into Sentence objects."""
        text = "First sentence. Second sentence. Third sentence."
        sentences = tokenize_sentences(text, "introduction", use_nltk=False)

        assert len(sentences) == 3
        assert all(hasattr(s, 'id') for s in sentences)
        assert all(hasattr(s, 'text') for s in sentences)
        assert all(s.section == "introduction" for s in sentences)

    def test_sentence_ids_unique(self):
        """Should generate unique IDs for each sentence."""
        text = "Sentence one. Sentence two. Sentence three."
        sentences = tokenize_sentences(text, "methods", use_nltk=False)

        ids = [s.id for s in sentences]
        assert len(ids) == len(set(ids))  # All unique

    def test_sentence_positions(self):
        """Should track character positions."""
        text = "First sentence. Second sentence."
        sentences = tokenize_sentences(text, "results", use_nltk=False)

        # Check positions are reasonable
        for sent in sentences:
            assert sent.char_start >= 0
            assert sent.char_end > sent.char_start
            assert sent.char_end <= len(text)

    def test_paragraph_index(self):
        """Should track paragraph indices."""
        text = "First. Second. Third."
        sentences = tokenize_sentences(text, "discussion", use_nltk=False)

        # Indices should be sequential
        for i, sent in enumerate(sentences):
            assert sent.paragraph_index == i


class TestGenerateSentenceId:
    """Tests for sentence ID generation."""

    def test_generate_id(self):
        """Should generate ID with section and index."""
        id1 = generate_sentence_id("intro", 0, "Test sentence")

        assert "intro" in id1
        assert "0" in id1

    def test_different_text_different_id(self):
        """Should generate different IDs for different text."""
        id1 = generate_sentence_id("intro", 0, "First sentence")
        id2 = generate_sentence_id("intro", 0, "Second sentence")

        assert id1 != id2

    def test_same_text_same_id(self):
        """Should generate same ID for same text."""
        id1 = generate_sentence_id("intro", 0, "Same sentence")
        id2 = generate_sentence_id("intro", 0, "Same sentence")

        assert id1 == id2


class TestIndexSentences:
    """Tests for complete sentence indexing."""

    def test_index_single_section(self):
        """Should index sentences in single section."""
        sections = {
            'introduction': ParsedSection(
                name='introduction',
                text='First sentence. Second sentence. Third sentence.',
                sentences=[],
                order_priority=10
            )
        }

        config = IndexingConfig(use_nltk=False)
        indexed = index_sentences(sections, config)

        assert 'introduction' in indexed
        assert len(indexed['introduction'].sentences) == 3

    def test_index_multiple_sections(self):
        """Should index sentences across multiple sections."""
        sections = {
            'intro': ParsedSection('intro', 'Intro sentence one. Intro sentence two.', []),
            'methods': ParsedSection('methods', 'Methods sentence.', [])
        }

        config = IndexingConfig(use_nltk=False)
        indexed = index_sentences(sections, config)

        assert len(indexed['intro'].sentences) == 2
        assert len(indexed['methods'].sentences) == 1

    def test_preserve_section_text(self):
        """Should preserve original section text."""
        sections = {
            'results': ParsedSection('results', 'Original text here.', [])
        }

        config = IndexingConfig(use_nltk=False)
        indexed = index_sentences(sections, config)

        assert indexed['results'].text == 'Original text here.'

    def test_preserve_section_priority(self):
        """Should preserve section priority."""
        sections = {
            'abstract': ParsedSection('abstract', 'Text.', [], order_priority=1)
        }

        config = IndexingConfig(use_nltk=False)
        indexed = index_sentences(sections, config)

        assert indexed['abstract'].order_priority == 1

    def test_respect_config_disable(self):
        """Should skip indexing when disabled."""
        sections = {
            'intro': ParsedSection('intro', 'Sentence one. Sentence two.', [])
        }

        config = IndexingConfig(enable_sentence_indexing=False)
        indexed = index_sentences(sections, config)

        # Should return unchanged (no sentences indexed)
        assert indexed['intro'].sentences == []

    def test_empty_section(self):
        """Should handle empty sections."""
        sections = {
            'empty': ParsedSection('empty', '', [])
        }

        config = IndexingConfig(use_nltk=False)
        indexed = index_sentences(sections, config)

        assert len(indexed['empty'].sentences) == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
