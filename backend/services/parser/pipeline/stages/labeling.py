"""Section labeling stage - injects section headers into markdown.

Uses structure analysis results to insert explicit section labels
for title, abstract, introduction, and other detected sections.
"""

import re
import logging
from typing import Optional

from ..models import StructureInfo

logger = logging.getLogger(__name__)


def inject_section_labels(markdown: str, structure_info: StructureInfo) -> str:
    """Inject section labels into markdown based on detected structure.

    Inserts markdown headers for:
    - Title (if detected)
    - Abstract (if detected)
    - Introduction (if detected as first section)

    Args:
        markdown: Clean markdown text (after cleanup stage)
        structure_info: Structure information from analysis stage

    Returns:
        Markdown with section labels inserted
    """
    logger.info("Injecting section labels")

    # Start with clean text
    result = markdown

    # 1. Label all detected section headers by finding and replacing bold text
    # This works for all sections including abstract, introduction, etc.
    labeled_sections = set()
    for header in structure_info.section_headers:
        labeled_sections.add(header.normalized_name)

        # Clean header text (remove markdown and numbering)
        header_clean = header.text.strip('*#.: ')

        # Remove leading numbers from label (but keep for matching)
        # e.g., "1. Introduction" -> "Introduction" for label
        header_label = re.sub(r'^\d+\.?\s*', '', header_clean)

        # Look for this section's text in markdown
        # Section headers were detected as bold spans, so the text might still be bold
        # IMPORTANT: Only match if it's on its own line to avoid labeling mid-paragraph bold text

        # Pattern 1: Bold text on its own line (most common)
        # Matches: **Results** or **1. Introduction** (entire line)
        pattern1 = r'(?m)^[\s]*\*\*' + re.escape(header_clean).replace(r'\ ', r'[\s\n]*') + r'\*\*[\s]*$'
        match = re.search(pattern1, result, re.IGNORECASE)
        if match:
            # Ensure proper spacing: header needs blank line after it
            after = result[match.end():]
            if not after.startswith('\n\n'):
                after = '\n' + after.lstrip('\n')
            result = result[:match.start()] + f"### **{header_label}**\n\n" + after
            logger.info(f"Labeled section: {header.normalized_name}")
            continue

        # Pattern 2: Plain text on its own line (no bold markers)
        pattern2 = r'(?m)^[\s]*' + re.escape(header_clean) + r'[\s]*$'
        match = re.search(pattern2, result, re.IGNORECASE)
        if match:
            after = result[match.end():]
            if not after.startswith('\n\n'):
                after = '\n' + after.lstrip('\n')
            result = result[:match.start()] + f"### **{header_label}**\n\n" + after
            logger.info(f"Labeled section: {header.normalized_name}")
            continue

        # Pattern 3: Try without number prefix if original had number
        # e.g., match "**Introduction**" for header "1. Introduction"
        if header_label != header_clean:
            pattern3 = r'(?m)^[\s]*\*\*' + re.escape(header_label) + r'\*\*[\s]*$'
            match = re.search(pattern3, result, re.IGNORECASE)
            if match:
                after = result[match.end():]
                if not after.startswith('\n\n'):
                    after = '\n' + after.lstrip('\n')
                result = result[:match.start()] + f"### **{header_label}**\n\n" + after
                logger.info(f"Labeled section: {header.normalized_name}")
                continue

    # 2. Fallback: If no introduction was detected but there's content before first section,
    # label it as introduction (do this LAST after all other sections are labeled)
    if 'introduction' not in labeled_sections:
        # Find the first section header
        first_section_match = re.search(r'### \*\*', result)
        if first_section_match and first_section_match.start() > 500:
            # There's substantial content before first labeled section
            # Insert introduction header at start of substantive content
            # Skip title/author/affiliation preamble (usually in first ~300 chars)
            lines = result[:first_section_match.start()].split('\n')

            # Find first paragraph with >100 chars after initial metadata
            insert_idx = 0
            char_count = 0
            for i, line in enumerate(lines):
                char_count += len(line) + 1
                if char_count > 300 and len(line.strip()) > 100:
                    # This is a substantial paragraph - insert intro label here
                    insert_idx = i
                    break

            if insert_idx > 0:
                before_intro = '\n'.join(lines[:insert_idx])
                intro_and_after = '\n'.join(lines[insert_idx:]) + result[first_section_match.start():]
                result = before_intro + '\n\n### **Introduction**\n\n' + intro_and_after
                logger.info("Inserted Introduction label (fallback)")

    return result
