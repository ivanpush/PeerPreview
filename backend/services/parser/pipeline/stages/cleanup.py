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


def remove_incomplete_sentence_fragments(text: str) -> str:
    """Remove consecutive lines that are incomplete sentence fragments.

    Detects chunks of 2+ consecutive lines where EACH line is:
    - Short to medium length (not full paragraph)
    - No proper sentence ending punctuation
    - Not a complete sentence structure

    Preserves:
    - Long complete sentences (>100 chars or ends with period)
    - Section headers (bold markdown **text**)
    - Figure captions (starts with **Fig or **Table)
    - List markers (a., 1., -, *)

    Args:
        text: Input text

    Returns:
        Text with incomplete fragments removed
    """
    lines = text.split('\n')
    filtered = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Always keep empty lines
        if not stripped:
            filtered.append(line)
            i += 1
            continue

        # Keep markdown section headers
        if stripped.startswith('#'):
            filtered.append(line)
            i += 1
            continue

        # Keep figure/table captions (they start with **Fig or **Table)
        if re.match(r'\*\*(Fig|Table|Scheme)', stripped, re.IGNORECASE):
            filtered.append(line)
            i += 1
            continue

        # Keep valid list markers
        if re.match(r'^[a-z]\.$|^\d+\.$|^[-*]$|^\([a-z0-9]+\)$', stripped):
            filtered.append(line)
            i += 1
            continue

        # Define what makes a line a "fragment" (incomplete sentence)
        def is_fragment_line(s):
            if not s:
                return False

            # Very long lines are likely complete sentences (100+ chars)
            if len(s) > 100:
                return False

            # Statistical notation (e.g., "_P_ = 0.321", "_n_ = 324 cells")
            if re.search(r'_[A-Za-z]_\s*=', s):
                return True  # Treat as fragment

            # Short lines with just numbers/symbols (e.g., "Histamine 6")
            word_count = len(s.split())
            if word_count <= 3 and not s.rstrip()[-1:] in '.!?':
                return True

            # Has sentence-ending punctuation at end AND reasonable length
            if s.rstrip()[-1:] in '.!?' and len(s) > 30:
                return False  # Complete sentence

            # Contains 3+ periods (likely multiple sentences or abbreviations)
            if s.count('.') >= 3:
                return False  # Likely real content

            # Check if line has sentence structure (has common words like "the", "is", "are", "has")
            has_sentence_words = bool(re.search(r'\b(the|is|are|was|were|has|have|had|can|will|would|should)\b', s, re.IGNORECASE))
            if has_sentence_words and len(s) > 40:
                return False  # Likely complete sentence

            # Otherwise it's a fragment
            return True

        # Check if current line is a fragment
        if is_fragment_line(stripped):
            # Look ahead and collect all consecutive fragments (skip blank lines and single bold chars)
            fragment_lines = [stripped]
            j = i + 1
            blank_count = 0

            while j < len(lines):
                next_line = lines[j].strip()

                # Skip over blank lines (up to 3)
                if not next_line:
                    blank_count += 1
                    if blank_count > 3:  # Too many blanks, stop
                        break
                    j += 1
                    continue

                # Skip over single bold characters like **a**, **b**, **c**
                if re.match(r'^\*\*[a-z0-9]\*\*$', next_line, re.IGNORECASE):
                    j += 1
                    continue

                # Stop at section headers
                if next_line.startswith('#'):
                    break

                # Stop at figure captions
                if re.match(r'\*\*(Fig|Table|Scheme)', next_line, re.IGNORECASE):
                    break

                # Check if this line is also a fragment
                if is_fragment_line(next_line):
                    fragment_lines.append(next_line)
                    blank_count = 0  # Reset blank counter
                    j += 1
                else:
                    # Hit a complete sentence, stop collecting
                    break

            # If we found 2+ consecutive fragments, remove them all
            if len(fragment_lines) >= 2:
                logger.debug(f"Removed {len(fragment_lines)} consecutive fragments:")
                for frag in fragment_lines[:3]:  # Log first 3
                    logger.debug(f"  - '{frag[:60]}...'")
                i = j  # Skip all fragments
                continue

        # Keep the line
        filtered.append(line)
        i += 1

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

    # 3. Remove incomplete sentence fragments
    text = remove_incomplete_sentence_fragments(text)

    # 4. Remove table remnants
    text = remove_table_remnants(text)

    # 5. Remove URL lines
    text = remove_url_lines(text)

    # 6. Normalize whitespace
    text = normalize_whitespace(text)

    logger.info(f"Cleanup: {original_length} -> {len(text)} chars ({len(text)/original_length*100:.1f}% retained)")

    return text
