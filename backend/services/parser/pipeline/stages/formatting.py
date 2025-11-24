"""Section formatting and validation stage.

Splits markdown into sections, validates required sections,
and handles section reordering.
"""

import re
from typing import Dict, List, Optional
import logging

from ..models import ParsedSection, Section
from ..config import SectionConfig

logger = logging.getLogger(__name__)


def split_sections(markdown: str, config: SectionConfig = None) -> Dict[str, ParsedSection]:
    """Split markdown into named sections.

    Args:
        markdown: Markdown text with section headers
        config: Section configuration

    Returns:
        Dictionary mapping section names to ParsedSection objects
    """
    if config is None:
        config = SectionConfig()

    sections = {}

    # Pattern matches: ### **SECTION NAME**
    split_pattern = r'(?m)^### \*\*(.*?)\*\*$'
    parts = re.split(split_pattern, markdown)

    # Handle preamble (content before first section)
    if parts[0].strip():
        sections['preamble'] = ParsedSection(
            name='preamble',
            text=parts[0].strip(),
            sentences=[],
            order_priority=0
        )

    # Process section pairs (name, content)
    for i in range(1, len(parts), 2):
        if i + 1 >= len(parts):
            break

        name = parts[i].strip().lower().replace(' ', '_')
        content = parts[i+1].strip()

        # Get priority from config
        priority = config.section_order.get(name, 100)

        sections[name] = ParsedSection(
            name=name,
            text=content,
            sentences=[],
            order_priority=priority
        )

    # If no sections found, treat entire document as full_text
    if not sections:
        sections['full_text'] = ParsedSection(
            name='full_text',
            text=markdown,
            sentences=[],
            order_priority=100
        )

    logger.info(f"Split document into {len(sections)} sections: {list(sections.keys())}")

    return sections


def normalize_section_name(name: str) -> str:
    """Normalize section name to standard form.

    Args:
        name: Section name

    Returns:
        Normalized section name
    """
    normalized = name.lower().strip()
    normalized = normalized.replace(' ', '_')
    normalized = normalized.replace('-', '_')

    # Handle common variations
    variations = {
        'acknowledgments': 'acknowledgements',
        'methods_and_materials': 'materials_and_methods',
        'conclusion': 'conclusions',
        'reference': 'references',
    }

    return variations.get(normalized, normalized)


def validate_required_sections(
    sections: Dict[str, ParsedSection],
    config: SectionConfig = None,
    title: str = None,
    has_authors: bool = False
) -> Dict[str, bool]:
    """Validate that required sections are present.

    Args:
        sections: Dictionary of sections
        config: Section configuration with required groups
        title: Document title (to check has_title)
        has_authors: Whether document has authors (to check has_authors)

    Returns:
        Dictionary with validation results
    """
    if config is None:
        config = SectionConfig()

    validation = {}

    for group_name, section_names in config.required_groups.items():
        # Special handling for title - check if title parameter is provided and non-empty
        if group_name == 'title':
            validation['has_title'] = bool(title and title.strip() and title != 'Unknown')
            if not validation['has_title']:
                logger.warning("Missing title")
            continue

        # Special handling for authors - use the has_authors parameter
        if group_name == 'authors':
            validation['has_authors'] = has_authors
            if not has_authors:
                logger.warning("Missing authors information")
            continue

        # Check if any section from this group exists
        has_section = any(
            section_key.lower() in section_names
            for section_key in sections.keys()
        )
        validation[f'has_{group_name}'] = has_section

        if not has_section:
            logger.warning(f"Missing required section group '{group_name}'. Expected one of: {section_names}")

    return validation


def reorder_sections(
    sections: List[Section],
    config: SectionConfig = None
) -> List[Section]:
    """Reorder sections according to configuration.

    Only moves administrative sections (references, acknowledgements) to end.
    Preserves content section order.

    Args:
        sections: List of sections
        config: Section configuration

    Returns:
        Reordered list of sections
    """
    if config is None:
        config = SectionConfig()

    if not config.reorder_admin_sections:
        return sections

    # Sections that should be at the end
    END_SECTIONS = [
        'references', 'bibliography', 'acknowledgements', 'acknowledgments',
        'author_contributions', 'competing_interests', 'data_availability',
        'funding', 'supplementary', 'appendix'
    ]

    # Separate into content sections and end sections
    content_sections = []
    end_sections = []

    for section in sections:
        section_lower = section.name.lower().replace(' ', '_')
        if section_lower in END_SECTIONS:
            end_sections.append(section)
        else:
            content_sections.append(section)

    # References should be last
    references = [s for s in end_sections if s.name.lower() in ['references', 'bibliography']]
    other_admin = [s for s in end_sections if s.name.lower() not in ['references', 'bibliography']]

    reordered = content_sections + other_admin + references

    logger.info(f"Reordered sections: {[s.name for s in reordered]}")

    return reordered


def detect_section_by_keywords(paragraph_text: str) -> Optional[str]:
    """Detect section type based on content keywords.

    Used for sections without explicit headers.

    Args:
        paragraph_text: Paragraph text to analyze

    Returns:
        Detected section type, or None
    """
    # Only check first 100 chars to avoid false positives
    check_text = paragraph_text[:100].lower()

    # Define keyword patterns for each section type
    SECTION_KEYWORDS = {
        'acknowledgements': [r'\bthank\b', r'\bgrateful\b', r'\backnowledge\b', r'\bsupported by\b'],
        'author_contributions': [r'author.{0,20}contributed', r'designed.{0,20}experiment', r'wrote.{0,20}manuscript', r'\bconceived\b'],
        'competing_interests': [r'declare.{0,20}conflict', r'competing interest', r'no.{0,20}conflict', r'authors declare'],
        'data_availability': [r'data.{0,20}available', r'deposited', r'accession number'],
        'funding': [r'funded by', r'grant', r'financial support']
    }

    for section_type, patterns in SECTION_KEYWORDS.items():
        if any(re.search(pattern, check_text) for pattern in patterns):
            logger.info(f"Detected section by keywords: {section_type}")
            return section_type

    return None


def format_sections(
    sections: Dict[str, ParsedSection],
    config: SectionConfig = None
) -> str:
    """Format sections back into markdown.

    Args:
        sections: Dictionary of sections
        config: Section configuration

    Returns:
        Formatted markdown with sections
    """
    if config is None:
        config = SectionConfig()

    # Convert to list and sort by priority
    section_list = list(sections.values())
    section_list.sort(key=lambda x: x.order_priority)

    # Build markdown
    formatted = []
    for section in section_list:
        if section.name != 'preamble':
            # Add section header
            formatted.append(f"\n### **{section.name.upper().replace('_', ' ')}**\n")
        formatted.append(section.text)

    return '\n'.join(formatted)
