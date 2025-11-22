"""Sentence indexing stage using NLTK.

Tokenizes section text into indexed sentences.
"""

import nltk
import hashlib
from typing import Dict
import logging

from ..models import ParsedSection, Sentence
from ..config import IndexingConfig

logger = logging.getLogger(__name__)


def ensure_nltk_data():
    """Ensure NLTK punkt tokenizer is downloaded."""
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        logger.info("Downloading NLTK punkt tokenizer...")
        nltk.download('punkt', quiet=True)


def index_sentences(
    sections: Dict[str, ParsedSection],
    config: IndexingConfig = None
) -> Dict[str, ParsedSection]:
    """Split section text into indexed sentences.

    Args:
        sections: Dictionary of sections to index
        config: Indexing configuration

    Returns:
        Updated sections with indexed sentences
    """
    if config is None:
        config = IndexingConfig()

    if not config.enable_sentence_indexing:
        return sections

    if config.use_nltk:
        ensure_nltk_data()

    indexed_sections = {}

    for section_name, section in sections.items():
        sentences = tokenize_sentences(
            section.text,
            section_name,
            use_nltk=config.use_nltk,
            language=config.language
        )

        indexed_sections[section_name] = ParsedSection(
            name=section.name,
            text=section.text,
            sentences=sentences,
            order_priority=section.order_priority
        )

    total_sentences = sum(len(s.sentences) for s in indexed_sections.values())
    logger.info(f"Indexed {total_sentences} sentences across {len(indexed_sections)} sections")

    return indexed_sections


def tokenize_sentences(
    text: str,
    section_name: str,
    use_nltk: bool = True,
    language: str = 'english'
) -> list[Sentence]:
    """Tokenize text into sentences.

    Args:
        text: Text to tokenize
        section_name: Name of section (for sentence IDs)
        use_nltk: Whether to use NLTK tokenizer
        language: Language for NLTK tokenizer

    Returns:
        List of Sentence objects
    """
    if use_nltk:
        try:
            sent_detector = nltk.data.load(f'tokenizers/punkt/{language}.pickle')
            sentence_texts = sent_detector.tokenize(text)
        except Exception as e:
            logger.warning(f"NLTK tokenization failed: {e}. Falling back to simple split.")
            sentence_texts = simple_sentence_split(text)
    else:
        sentence_texts = simple_sentence_split(text)

    # Create Sentence objects with IDs
    sentences = []
    char_pos = 0

    for para_idx, sent_text in enumerate(sentence_texts):
        sent_text = sent_text.strip()
        if not sent_text:
            continue

        # Find position in original text
        char_start = text.find(sent_text, char_pos)
        if char_start == -1:
            char_start = char_pos
        char_end = char_start + len(sent_text)
        char_pos = char_end

        # Generate unique ID
        sent_id = generate_sentence_id(section_name, para_idx, sent_text)

        sentence = Sentence(
            id=sent_id,
            section=section_name,
            text=sent_text,
            char_start=char_start,
            char_end=char_end,
            paragraph_index=para_idx
        )

        sentences.append(sentence)

    return sentences


def simple_sentence_split(text: str) -> list[str]:
    """Simple sentence splitting fallback.

    Args:
        text: Text to split

    Returns:
        List of sentence strings
    """
    # Split on sentence terminators followed by space and capital letter
    import re
    sentences = re.split(r'([.!?])\s+(?=[A-Z])', text)

    # Reconstruct sentences (split creates [sent, terminator, sent, terminator, ...])
    result = []
    for i in range(0, len(sentences) - 1, 2):
        if i + 1 < len(sentences):
            result.append(sentences[i] + sentences[i+1])
        else:
            result.append(sentences[i])

    # Add final sentence if exists
    if len(sentences) % 2 == 1:
        result.append(sentences[-1])

    return [s.strip() for s in result if s.strip()]


def generate_sentence_id(section: str, index: int, text: str) -> str:
    """Generate unique ID for sentence.

    Args:
        section: Section name
        index: Sentence index in section
        text: Sentence text

    Returns:
        Unique sentence ID
    """
    # Use hash of text to ensure uniqueness
    text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
    return f"{section}_{index}_{text_hash}"
