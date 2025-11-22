"""Bibliography/references parsing."""

import re
from typing import List, Optional
import logging

from ..models import ParsedSection, BibliographyEntry

logger = logging.getLogger(__name__)


def parse_bibliography(section: Optional[ParsedSection]) -> List[BibliographyEntry]:
    """Parse bibliography section into structured entries.

    Args:
        section: References/bibliography section

    Returns:
        List of BibliographyEntry objects
    """
    if not section:
        return []

    entries = []
    lines = section.text.split('\n')
    current_entry = []
    entry_id = 1

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check if this starts a new reference
        if re.match(r'^\d+\.?\s+|\[\d+\]', line):
            if current_entry:
                # Save previous entry
                text = ' '.join(current_entry)
                entries.append(BibliographyEntry(
                    id=str(entry_id),
                    raw_text=text,
                    doi=extract_doi(text)
                ))
                entry_id += 1

            # Start new entry (remove the number)
            clean_line = re.sub(r'^\d+\.?\s+|\[\d+\]\s*', '', line)
            current_entry = [clean_line]
        else:
            current_entry.append(line)

    # Add last entry
    if current_entry:
        text = ' '.join(current_entry)
        entries.append(BibliographyEntry(
            id=str(entry_id),
            raw_text=text,
            doi=extract_doi(text)
        ))

    logger.info(f"Parsed {len(entries)} bibliography entries")
    return entries


def extract_doi(text: str) -> Optional[str]:
    """Extract DOI from reference text.

    Args:
        text: Reference text

    Returns:
        DOI string or None
    """
    match = re.search(r'10\.\d{4,}/[^\s]+', text)
    return match.group(0) if match else None
