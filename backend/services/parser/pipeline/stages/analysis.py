"""Structure analysis stage via bold text detection.

Analyzes PDF font metadata to detect document structure:
- Titles (largest bold text on first page)
- Section headers (bold text matching standard sections)
- Abstract fallback (first substantial paragraph)
"""

import pymupdf
import re
from typing import Dict, List, Optional
import logging

from ..models import BoldSpan, SectionHeader, StructureInfo
from ..config import AnalysisConfig

logger = logging.getLogger(__name__)


# Standard academic paper sections
STANDARD_SECTIONS = [
    'abstract', 'introduction', 'background', 'related work',
    'methods', 'materials and methods', 'experimental', 'methodology',
    'results', 'discussion', 'results and discussion',
    'conclusion', 'conclusions', 'summary',
    'references', 'bibliography', 'acknowledgments', 'acknowledgements'
]


def extract_bold_spans(doc: pymupdf.Document) -> List[BoldSpan]:
    """Extract all bold text spans from document.

    Args:
        doc: pymupdf Document

    Returns:
        List of BoldSpan objects with text, position, and font info
    """
    bold_spans = []

    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if block.get("type") != 0:  # Only text blocks
                continue

            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span.get("text", "").strip()
                    if not text:
                        continue

                    # Check if bold
                    font_name = span.get("font", "").lower()
                    font_flags = span.get("flags", 0)
                    font_size = span.get("size", 0)

                    # Bold detection: flag bit 16 (2^4) or "bold" in font name
                    is_bold = (font_flags & 16) or "bold" in font_name or "heavy" in font_name

                    if is_bold:
                        # Skip figure/table captions
                        if is_figure_caption(text):
                            continue

                        bbox = span.get("bbox", [0, 0, 0, 0])
                        bold_spans.append(BoldSpan(
                            text=text,
                            page=page_num,
                            font_size=font_size,
                            bbox=bbox,
                            y_position=bbox[1]  # Top y-coordinate
                        ))

    logger.info(f"Extracted {len(bold_spans)} bold text spans")
    return bold_spans


def is_figure_caption(text: str) -> bool:
    """Check if text is likely a figure or table caption.

    Args:
        text: Text to check

    Returns:
        True if text appears to be a figure/table caption
    """
    # Pattern 1: Starts with Figure/Fig/Table + number
    if re.match(r'^(Figure|Fig\.?|Table|Scheme)\s*\d+', text, re.IGNORECASE):
        return True

    # Pattern 2: Contains figure placeholder from extraction
    if '[Figure]' in text or ('picture' in text.lower() and 'intentionally omitted' in text.lower()):
        return True

    # Pattern 3: Starts with common caption patterns
    caption_patterns = [
        r'^\d+\s*\.?\s*(Figure|Fig|Table)',  # "1. Figure" or "1 Figure"
        r'^Supplementary (Figure|Table)',
        r'^Extended Data Figure'
    ]
    if any(re.match(pattern, text, re.IGNORECASE) for pattern in caption_patterns):
        return True

    return False


def detect_title(bold_spans: List[BoldSpan], page_height: float = 842) -> Optional[str]:
    """Extract title from first page bold text.

    Looks for largest bold text in top 30% of first page.

    Args:
        bold_spans: List of bold text spans
        page_height: Height of first page in points (default 842 = letter size)

    Returns:
        Detected title text, or None
    """
    if not bold_spans:
        return None

    # Filter to page 0, top 30%, exclude very short text (<10 chars)
    page_0_bold = [b for b in bold_spans
                   if b.page == 0
                   and b.y_position < page_height * 0.3
                   and len(b.text) > 10]

    if not page_0_bold:
        return None

    # Find the largest font size on page 0
    max_size = max(b.font_size for b in page_0_bold)

    # Skip patterns for non-systematic text
    skip_patterns = [
        r'biorxiv', r'preprint', r'doi:', r'copyright',
        r'license', r'peer review', r'manuscript', r'^\d+$',
        r'author manuscript', r'accepted', r'published',
        r'\w+@\w+',  # Email addresses
        r'university', r'department', r'institute', r'college', r'school',  # Affiliations
        r'^\d{4}$',  # Standalone years
        r'journal', r'research', r'article'  # Journal names
    ]

    candidates = [b for b in page_0_bold if b.font_size == max_size]

    for candidate in sorted(candidates, key=lambda x: x.y_position):
        text = candidate.text

        # Skip artifacts
        if any(re.search(pat, text.lower()) for pat in skip_patterns):
            continue

        # Skip if looks like author names (multiple capitalized words, all short)
        words = text.split()
        if len(words) >= 2 and all(w[0].isupper() and len(w) < 12 for w in words if w):
            continue

        logger.info(f"Detected title: {text}")
        return text

    return None


def detect_section_headers(bold_spans: List[BoldSpan]) -> List[SectionHeader]:
    """Find section headers from bold text matching standard sections.

    Args:
        bold_spans: List of bold text spans

    Returns:
        List of SectionHeader objects
    """
    headers = []

    for span in bold_spans:
        text_clean = span.text.lower().strip('*#.: ')

        # Check if matches any standard section
        for section in STANDARD_SECTIONS:
            if text_clean == section or (section in text_clean and len(text_clean) < len(section) + 10):
                normalized = section.replace(' ', '_')

                header = SectionHeader(
                    text=span.text,
                    normalized_name=normalized,
                    page=span.page,
                    confidence=1.0 if text_clean == section else 0.8
                )
                headers.append(header)
                break

    logger.info(f"Detected {len(headers)} section headers")
    return headers


def extract_abstract_fallback(doc: pymupdf.Document) -> Optional[str]:
    """Extract first substantial paragraph from page 1 as abstract fallback.

    Used when no explicit Abstract section header is found.

    Args:
        doc: pymupdf Document

    Returns:
        Abstract text, or None if not found
    """
    if len(doc) == 0:
        logger.warning("Document has no pages for abstract extraction")
        return None

    page = doc[0]
    text = page.get_text("text")
    logger.info(f"Analyzing page 1 for abstract ({len(text)} chars)")

    # Split into paragraphs
    paragraphs = re.split(r'\n\s*\n', text)

    for para in paragraphs:
        para_raw = para.strip()

        # Remove line numbers at start of each line
        para_clean = re.sub(r'(?m)^\d+\s+', '', para_raw)

        # Check if paragraph contains "Abstract" header
        if re.search(r'^\s*Abstract\s*$', para_clean, re.MULTILINE | re.IGNORECASE):
            # Extract content after Abstract header
            parts = re.split(r'^\s*Abstract\s*$', para_clean, maxsplit=1, flags=re.MULTILINE | re.IGNORECASE)
            if len(parts) > 1:
                abstract_content = parts[1].strip()

                # Clean up footer metadata
                footer_pattern = r'(biorxiv|preprint|doi:|copyright|license|peer review|manuscript|author manuscript|accepted|published).*$'
                abstract_content = re.sub(footer_pattern, '', abstract_content, flags=re.IGNORECASE | re.DOTALL)
                abstract_content = abstract_content.strip()

                if len(abstract_content) > 100:
                    logger.info(f"Found Abstract section ({len(abstract_content)} chars)")
                    return abstract_content

        # Skip if too short
        if len(para_clean) < 100:
            continue

        # Check if substantial multi-sentence paragraph
        sentence_count = para_clean.count('. ') + para_clean.count('! ') + para_clean.count('? ')
        terminator_count = para_clean.count('.') + para_clean.count('!') + para_clean.count('?')

        # Skip if starts with metadata patterns
        start_skip_patterns = [
            r'^Authors?\s+(and\s+)?Affiliations?',
            r'^Corresponding author',
            r'^\w+@',  # Email
            r'^Department of',
            r'^University of',
            r'^\d{4}$',  # Year
        ]
        if any(re.match(pat, para_clean, re.IGNORECASE) for pat in start_skip_patterns):
            continue

        # Must have multiple sentences and reasonable length
        if (100 < len(para_clean) < 3000 and
            (sentence_count >= 2 or terminator_count >= 3)):
            # Clean up footer if present
            footer_pattern = r'(biorxiv|preprint|doi:|copyright|license|peer review|manuscript|author manuscript|accepted|published).*$'
            para_clean = re.sub(footer_pattern, '', para_clean, flags=re.IGNORECASE | re.DOTALL)
            para_clean = para_clean.strip()

            if len(para_clean) > 100 and para_clean[-1] in '.!?':
                logger.info(f"Selected first multi-sentence paragraph as abstract ({len(para_clean)} chars)")
                return para_clean

    logger.warning("No suitable abstract paragraph found")
    return None


def analyze_structure(doc: pymupdf.Document, config: AnalysisConfig) -> StructureInfo:
    """Complete structure analysis pipeline.

    Args:
        doc: pymupdf Document
        config: Analysis configuration

    Returns:
        StructureInfo with detected structure elements
    """
    bold_spans = []
    title = None
    abstract = None
    section_headers = []

    if config.detect_bold_text:
        bold_spans = extract_bold_spans(doc)

        if config.extract_title:
            # Get page height for title detection
            page_height = doc[0].rect.height if len(doc) > 0 else 842
            title = detect_title(bold_spans, page_height)

        section_headers = detect_section_headers(bold_spans)

    if config.extract_abstract_fallback:
        abstract = extract_abstract_fallback(doc)

    return StructureInfo(
        title=title,
        abstract=abstract,
        section_headers=section_headers,
        bold_spans=bold_spans
    )
