"""Artifact cleanup stage for removing PDF extraction artifacts.

MINIMAL APPROACH: Only remove what we're sure is garbage.
Build up carefully to avoid deleting real content.
"""

import re
import logging

from ..config import CleanupConfig

logger = logging.getLogger(__name__)


def remove_short_gibberish_lines(text: str) -> str:
    """Remove very short lines that are likely gibberish.

    Removes lines with 1-3 characters that aren't valid list markers.
    Preserves: "a.", "1.", "-", "*", "(a)", etc.

    Args:
        text: Input text

    Returns:
        Text with short gibberish lines removed
    """
    lines = text.split('\n')
    filtered = []

    for line in lines:
        stripped = line.strip()

        # Keep empty lines
        if not stripped:
            filtered.append(line)
            continue

        # Keep lines longer than 3 chars
        if len(stripped) > 3:
            filtered.append(line)
            continue

        # Keep valid list markers
        # a. b. c. / 1. 2. 3. / - / * / (a) / (1)
        if re.match(r'^[a-z]\.$|^\d+\.$|^[-*]$|^\([a-z0-9]+\)$', stripped):
            filtered.append(line)
            continue

        # Otherwise skip this short gibberish line
        logger.debug(f"Removed short line: '{stripped}'")

    return '\n'.join(filtered)


def normalize_whitespace(text: str) -> str:
    """Normalize excessive whitespace.

    Args:
        text: Input text

    Returns:
        Text with normalized whitespace
    """
    # Collapse excessive newlines (>3 becomes 3)
    text = re.sub(r'\n{4,}', '\n\n\n', text)

    # Collapse excessive spaces (>2 becomes 1)
    text = re.sub(r' {3,}', ' ', text)

    return text.strip()


def remove_scattered_chars(text: str) -> str:
    """Remove lines with scattered single characters (figure axis labels).

    Removes lines like: "a", "b", "c", "d" or "0 5 10 15 20 25"
    These are typically axis labels from figures.

    Args:
        text: Input text

    Returns:
        Text with scattered character lines removed
    """
    lines = text.split('\n')
    filtered = []

    for line in lines:
        stripped = line.strip()

        # Keep empty lines
        if not stripped:
            filtered.append(line)
            continue

        # Keep lines longer than 50 chars (likely real content)
        if len(stripped) > 50:
            filtered.append(line)
            continue

        # Check if line is just single letters with spaces: "a b c d"
        tokens = stripped.split()
        if len(tokens) >= 3:
            # If all tokens are single chars, it's likely figure labels
            if all(len(t) == 1 for t in tokens):
                logger.debug(f"Removed scattered chars: '{stripped}'")
                continue

            # If line is mostly numbers with spaces: "0 5 10 15 20 25"
            # Check if >70% of tokens are pure numbers
            number_tokens = sum(1 for t in tokens if t.replace('.', '').replace('-', '').isdigit())
            if len(tokens) >= 4 and number_tokens / len(tokens) > 0.7:
                logger.debug(f"Removed number sequence: '{stripped}'")
                continue

        # Keep the line
        filtered.append(line)

    return '\n'.join(filtered)


def remove_table_remnants(text: str) -> str:
    """Remove obvious table formatting remnants.

    Removes lines that are clearly table markup:
    - Lines with only pipes and dashes: |---|---|---|
    - Lines with only pipes: ||||||||
    - Lines with multiple pipe separators (likely table rows)

    Args:
        text: Input text

    Returns:
        Text with table remnants removed
    """
    lines = text.split('\n')
    filtered = []

    for line in lines:
        stripped = line.strip()

        # Skip empty lines
        if not stripped:
            filtered.append(line)
            continue

        # Remove lines that are just pipes and dashes: |---|---|
        if re.match(r'^[\|\-\s]+$', stripped):
            logger.debug(f"Removed table divider: '{stripped[:60]}'")
            continue

        # Remove lines with >4 pipe characters (likely table rows)
        pipe_count = stripped.count('|')
        if pipe_count > 4:
            # Check if line has actual sentence-like content
            # Real content has multiple words in at least one cell
            content_between_pipes = [s.strip() for s in stripped.split('|')]
            content_parts = [s for s in content_between_pipes if s]

            # If no cell has >2 words, it's likely a table row with just labels/numbers
            has_real_content = any(len(s.split()) > 2 for s in content_parts)

            if not has_real_content:
                logger.debug(f"Removed table row: '{stripped[:60]}'")
                continue

        # Keep the line
        filtered.append(line)

    return '\n'.join(filtered)


def remove_url_lines(text: str) -> str:
    """Remove lines containing URLs or web addresses.

    Removes lines with: http://, https://, www., .com, .org, .edu, .gov

    Args:
        text: Input text

    Returns:
        Text with URL lines removed
    """
    lines = text.split('\n')
    filtered = []

    url_patterns = [
        r'https?://',      # http:// or https://
        r'www\.',          # www.
        r'\.com\b',        # .com
        r'\.org\b',        # .org
        r'\.edu\b',        # .edu
        r'\.gov\b',        # .gov
    ]

    for line in lines:
        has_url = False
        for pattern in url_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                has_url = True
                logger.debug(f"Removed URL line: '{line.strip()[:80]}'")
                break

        if not has_url:
            filtered.append(line)

    return '\n'.join(filtered)


def cleanup_all(text: str, config: CleanupConfig = None) -> str:
    """Apply minimal cleanup operations.

    Args:
        text: Input text
        config: Cleanup configuration

    Returns:
        Cleaned text
    """
    if config is None:
        config = CleanupConfig()

    original_length = len(text)

    # 1. Remove short gibberish lines
    text = remove_short_gibberish_lines(text)

    # 2. Remove scattered characters (figure labels)
    text = remove_scattered_chars(text)

    # 3. Remove table remnants
    text = remove_table_remnants(text)

    # 4. Remove URL lines
    text = remove_url_lines(text)

    # 5. Normalize whitespace
    text = normalize_whitespace(text)

    logger.info(f"Cleanup: {original_length} -> {len(text)} chars ({len(text)/original_length*100:.1f}% retained)")

    return text
