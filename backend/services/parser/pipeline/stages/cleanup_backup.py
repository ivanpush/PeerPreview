"""Artifact cleanup stage for removing PDF extraction artifacts.

Removes common PDF artifacts like headers, footers, copyright notices,
figure placeholders, affiliations, DOIs, etc.
"""

import re
from collections import Counter
from typing import Set
import logging

from ..config import CleanupConfig

logger = logging.getLogger(__name__)


def remove_figure_blocks(text: str) -> str:
    """Remove figure placeholder blocks and remnants.

    Args:
        text: Input text

    Returns:
        Text with figure blocks completely removed
    """
    # Remove "picture [NxN] intentionally omitted"
    text = re.sub(
        r'picture\s*\[\d+\s*x\s*\d+\]\s*intentionally omitted',
        '',
        text,
        flags=re.IGNORECASE
    )

    # Remove "==> picture ... intentionally omitted <=="
    text = re.sub(
        r'=+>\s*picture.*?intentionally omitted\s*<==+',
        '',
        text,
        flags=re.IGNORECASE
    )

    # Remove any remaining [Figure] placeholders
    text = re.sub(r'\[Figure\]', '', text, flags=re.IGNORECASE)

    # Remove figure caption blocks - these are text remnants from figures
    # Pattern: starts with "**a**" or similar, ends with "**Fig. X |**"
    # These are figure labels and diagrams that got extracted as text
    text = re.sub(
        r'\*\*[a-z]\*\*.*?\*\*(?:Fig\.|Figure)\s+\d+[^\n]*\*\*',
        '',
        text,
        flags=re.IGNORECASE | re.DOTALL
    )

    # Also remove standalone figure captions: "Fig. 1 | Caption text..."
    # These appear as their own paragraphs
    text = re.sub(
        r'(?m)^\*\*(?:Fig\.|Figure)\s+\d+[^\n]*\*\*[^\n]*$',
        '',
        text,
        flags=re.IGNORECASE
    )

    return text


def remove_common_artifacts(text: str) -> str:
    """Remove common manuscript artifacts.

    Args:
        text: Input text

    Returns:
        Text with artifacts removed
    """
    artifacts = [
        'Author Manuscript', 'HHS Public Access', 'NIH Public Access',
        'bioRxiv preprint', 'which was not certified by peer review',
        'medRxiv preprint', 'arXiv:', 'Preprint:', 'PREPRINT'
    ]

    for artifact in artifacts:
        text = re.sub(rf'\b{re.escape(artifact)}\b', '', text, flags=re.IGNORECASE)

    return text


def remove_affiliations(text: str) -> str:
    """Remove institutional affiliation lines.

    Args:
        text: Input text

    Returns:
        Text with affiliation lines removed
    """
    affiliation_patterns = [
        r'(?m)^\d+\s*Department of.*?(?=\n|$)',  # "1Department of..."
        r'(?m)^\d+\s*Division of.*?(?=\n|$)',     # "1Division of..."
        r'(?m)^.*?Department of.*?University of.*?(?:USA|UK|CA)\s*\.?\s*(?=\n|$)',
        r'(?m)^\[\d+\]\s*.*?(?:University|Institute|School|College).*?(?=\n|$)',
        r'(?m)^.*?(?:University|Institute).*?(?:USA|UK|CA|USA\.)\s*\.?\s*\[\d+\]',
    ]

    for pattern in affiliation_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)

    return text


def remove_doi_lines(text: str) -> str:
    """Remove DOI (Digital Object Identifier) lines.

    Args:
        text: Input text

    Returns:
        Text with DOI lines removed
    """
    text = re.sub(r'(?m)^.*?doi:\s*10\.\d+/[^\n]+$', '', text)
    return text


def remove_copyright_lines(text: str) -> str:
    """Remove copyright notices.

    Args:
        text: Input text

    Returns:
        Text with copyright lines removed
    """
    text = re.sub(r'(?m)^.*?©.*?$', '', text)
    text = re.sub(r'(?m)^.*?Copyright.*?$', '', text, flags=re.IGNORECASE)
    return text


def remove_page_numbers(text: str) -> str:
    """Remove page number lines.

    Args:
        text: Input text

    Returns:
        Text with page numbers removed
    """
    text = re.sub(r'(?m)^Page\s+\d+\s*$', '', text, flags=re.IGNORECASE)
    text = re.sub(r'(?m)^\d+\s*$', '', text)  # Standalone numbers on lines
    return text


def remove_date_stamps(text: str) -> str:
    """Remove date stamp lines.

    Args:
        text: Input text

    Returns:
        Text with date stamps removed
    """
    text = re.sub(r'(?m)^.*?\d{1,2}/\d{1,2}/\d{2,4}.*?$', '', text)
    return text


def normalize_whitespace(text: str) -> str:
    """Normalize excessive whitespace.

    Args:
        text: Input text

    Returns:
        Text with normalized whitespace
    """
    # Collapse excessive newlines
    text = re.sub(r'\n{4,}', '\n\n\n', text)

    # Collapse excessive spaces
    text = re.sub(r' {3,}', ' ', text)

    return text.strip()


def remove_repeated_lines(text: str, min_repeats: int = 3, max_length: int = 100) -> str:
    """Remove lines that repeat across document (likely headers/footers).

    Args:
        text: Input text
        min_repeats: Minimum number of repetitions to consider a line repeated
        max_length: Maximum line length to consider (filters out content paragraphs)

    Returns:
        Text with repeated lines removed
    """
    lines = text.split('\n')
    line_counts = Counter(lines)

    # Find lines that repeat suspiciously often
    repeated_lines: Set[str] = {
        line for line, count in line_counts.items()
        if count > min_repeats and 0 < len(line.strip()) < max_length
    }

    # Filter out repeated lines
    filtered_lines = [line for line in lines if line not in repeated_lines]

    logger.info(f"Removed {len(lines) - len(filtered_lines)} repeated lines")

    return '\n'.join(filtered_lines)


def cleanup_all(text: str, config: CleanupConfig = None) -> str:
    """Apply all cleanup operations.

    Args:
        text: Input text
        config: Cleanup configuration

    Returns:
        Cleaned text
    """
    if config is None:
        config = CleanupConfig()

    original_length = len(text)

    if config.remove_figure_blocks:
        text = remove_figure_blocks(text)

    if config.remove_headers_footers:
        text = remove_repeated_lines(text)

    if config.remove_affiliations:
        text = remove_affiliations(text)

    if config.remove_page_numbers:
        text = remove_page_numbers(text)

    if config.remove_copyright:
        text = remove_copyright_lines(text)

    if config.remove_doi_blocks:
        text = remove_doi_lines(text)

    # Always remove common artifacts and normalize whitespace
    text = remove_common_artifacts(text)
    text = remove_date_stamps(text)
    text = normalize_whitespace(text)

    logger.info(f"Cleanup: {original_length} -> {len(text)} chars ({len(text)/original_length*100:.1f}% retained)")

    return text
