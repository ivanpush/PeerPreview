"""Citation extraction from parsed documents."""

import re
from typing import Dict, List
import logging

from ..models import ParsedSection, CitationRef

logger = logging.getLogger(__name__)


CITATION_PATTERNS = [
    r'\[(\d+(?:,\s*\d+)*)\]',  # [1,2,3] style
    r'\(([A-Z][a-z]+(?:\s+et\s+al\.?)?,?\s*\d{4})\)',  # (Author et al., 2023) style
]


def extract_citations(sections: Dict[str, ParsedSection]) -> List[CitationRef]:
    """Extract in-text citations from sections.

    Args:
        sections: Dictionary of parsed sections with indexed sentences

    Returns:
        List of CitationRef objects
    """
    refs = []

    for name, section in sections.items():
        if name == 'references':
            continue

        for sent in section.sentences:
            for pat in CITATION_PATTERNS:
                for match in re.finditer(pat, sent.text):
                    # Extract citation ID
                    try:
                        citation_id = match.group(1) if match.lastindex and match.lastindex >= 1 else match.group(0)
                    except (IndexError, AttributeError):
                        citation_id = match.group(0)

                    refs.append(CitationRef(
                        id=citation_id,
                        section=name,
                        sentence_id=sent.id,
                        sentence_text=sent.text
                    ))

    logger.info(f"Extracted {len(refs)} citations")
    return refs
