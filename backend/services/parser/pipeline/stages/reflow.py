"""Text reflow stage for paragraph reconstruction.

Intelligently reconstructs paragraphs from line-broken PDF text.
"""

import re
from typing import List
import logging

from ..config import ReflowConfig

logger = logging.getLogger(__name__)


def is_header_line(line: str, index: int, all_lines: List[str]) -> bool:
    """Determine if a line is likely a section header.

    Args:
        line: Line to check
        index: Line index in document
        all_lines: All lines in document

    Returns:
        True if line appears to be a header
    """
    # Check length
    if len(line) > 100 or len(line) < 3:
        return False

    # Check for markdown headers
    if line.startswith('#'):
        return True

    # Check for bold markdown
    if line.startswith('**') and line.endswith('**'):
        return True

    # Check for known section names
    section_keywords = [
        'abstract', 'introduction', 'methods', 'results',
        'discussion', 'conclusion', 'references', 'acknowledgment',
        'keywords', 'background', 'materials', 'supplementary'
    ]

    lower_line = line.lower().strip('*# ')
    if any(keyword in lower_line for keyword in section_keywords):
        # Additional check: next line should be regular text or empty
        if index + 1 < len(all_lines):
            next_line = all_lines[index + 1].strip()
            if not next_line or (next_line and not next_line.isupper()):
                return True

    # Check if all caps (common for headers)
    if line.isupper() and len(line.split()) < 5:
        return True

    return False


def merge_hyphenations(text: str) -> str:
    """Merge hyphenated words split across lines.

    Args:
        text: Text with potential hyphenations

    Returns:
        Text with hyphenations merged
    """
    # Pattern: word- at end of line followed by continuation
    # Replace "word-\npart" with "wordpart"
    text = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', text)

    return text


def reflow_text(markdown: str, config: ReflowConfig = None) -> str:
    """Intelligently reconstruct paragraphs from line-broken text.

    Args:
        markdown: Input markdown text
        config: Reflow configuration

    Returns:
        Reflowed text with reconstructed paragraphs
    """
    if config is None:
        config = ReflowConfig()

    if not config.enable_reflow:
        return markdown

    # Merge hyphenations first
    if config.merge_hyphenations:
        markdown = merge_hyphenations(markdown)

    lines = markdown.split('\n')
    reflowed = []
    current_paragraph = []

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Empty lines separate paragraphs
        if not stripped:
            if current_paragraph:
                reflowed.append(' '.join(current_paragraph))
                current_paragraph = []
            reflowed.append('')  # Preserve empty line
            continue

        # Check if this looks like a section header
        if is_header_line(stripped, i, lines):
            # Flush current paragraph
            if current_paragraph:
                reflowed.append(' '.join(current_paragraph))
                current_paragraph = []
            reflowed.append(line)  # Keep original formatting for headers
            continue

        # Check if line ends with sentence terminator
        ends_with_terminator = any(stripped.endswith(p) for p in ['.', '!', '?', ':', ';'])
        ends_with_citation = re.search(r'\[\d+\]$|\(\d{4}\)$', stripped)

        # Check if next line starts with capital or is empty
        next_line = lines[i+1].strip() if i+1 < len(lines) else ''
        next_starts_capital = next_line and next_line[0].isupper()

        # Decide whether to break or continue
        if ends_with_terminator or ends_with_citation:
            current_paragraph.append(stripped)
            if next_starts_capital or not next_line:
                # Likely sentence/paragraph end
                reflowed.append(' '.join(current_paragraph))
                current_paragraph = []
        else:
            # Continue paragraph
            current_paragraph.append(stripped)

    # Flush remaining paragraph
    if current_paragraph:
        reflowed.append(' '.join(current_paragraph))

    result = '\n'.join(reflowed)
    logger.info(f"Reflowed text: {len(lines)} lines -> {len(reflowed)} lines")

    return result
