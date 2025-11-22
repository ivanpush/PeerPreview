"""Figure extraction from documents."""

import re
from typing import Dict, List, Tuple
import logging

from ..models import ParsedSection, FigureBlock, FigureRef

logger = logging.getLogger(__name__)


def extract_figures(
    markdown: str,
    sections: Dict[str, ParsedSection]
) -> Tuple[List[FigureBlock], List[FigureRef]]:
    """Extract figure blocks and references.

    Args:
        markdown: Full markdown text
        sections: Parsed sections with indexed sentences

    Returns:
        Tuple of (figure blocks, figure references)
    """
    figures = extract_figure_blocks(markdown)
    refs = extract_figure_references(sections)

    logger.info(f"Extracted {len(figures)} figures and {len(refs)} figure references")

    return figures, refs


def extract_figure_blocks(markdown: str) -> List[FigureBlock]:
    """Extract figure captions from markdown.

    Args:
        markdown: Markdown text

    Returns:
        List of FigureBlock objects
    """
    figures = []

    # Pattern matches: Figure 1: Caption text...
    pattern = r'(?:Figure|Fig\.?)\s+(\d+)[.:]?\s*(.+?)(?=\n\n|(?:Figure|Fig\.?)\s+\d+|$)'

    for match in re.finditer(pattern, markdown, re.IGNORECASE | re.DOTALL):
        figures.append(FigureBlock(
            id=f"fig-{match.group(1)}",
            label=f"Figure {match.group(1)}",
            caption=match.group(2).strip(),
            page=0  # Would need page tracking for accurate page numbers
        ))

    return figures


def extract_figure_references(sections: Dict[str, ParsedSection]) -> List[FigureRef]:
    """Extract references to figures in text.

    Args:
        sections: Parsed sections with indexed sentences

    Returns:
        List of FigureRef objects
    """
    refs = []

    # Pattern matches: Fig. 1, Figure 2, etc.
    pattern = r'(?:Figure|Fig\.?)\s+(\d+)'

    for name, section in sections.items():
        for sent in section.sentences:
            for match in re.finditer(pattern, sent.text, re.IGNORECASE):
                refs.append(FigureRef(
                    label=f"Figure {match.group(1)}",
                    section=name,
                    sentence_id=sent.id,
                    sentence_text=sent.text
                ))

    return refs
