# Core PDF Analysis System - Implementation Plan

## Executive Summary

This document outlines the implementation of the **primary 12-phase PDF analysis system** for PeerPreview. This is NOT a fallback system - it's the core detection engine that handles both standard and non-standard scientific PDFs with confidence scoring for quality metrics.

**Key Principle:** Progressive document understanding where each phase builds on previous results, with complete text accounting to ensure nothing is lost.

---

## System Architecture

### Overview
The 12-phase system progressively analyzes PDF structure from title through unparsed content, with each phase depending on and refining results from previous phases.

### Phase Dependencies
```
Phase 1-2 (Pre-processing) → Already implemented in pipeline
    ↓
Phase 3 (Title) → REQUIRED for Phase 4
    ↓
Phase 4 (Authors) → REQUIRED for Phase 5
    ↓
Phase 5 (Affiliations) → REQUIRED for Phase 6
    ↓
Phase 6 (Abstract) → REQUIRED for Phase 7
    ↓
Phase 7 (Introduction) → Input for Phase 8
    ↓
Phase 8 (Non-bold Headers) → Feeds into Phase 9
    ↓
Phase 9 (Section Content) ← Uses column detection from extraction.py
    ↓
Phase 10 (Figures/Tables) ← Runs in parallel with Phase 9
    ↓
Phase 11 (Edge Cases) → Post-processes Phase 9
    ↓
Phase 12 (Unparsed) → Final accounting
```

---

## Pre-Processing Foundation

### Font Size Median Calculation
**Location:** Stage 2 (analysis.py) - before Phase 3

```python
def calculate_font_median(blocks: List[TextBlock]) -> float:
    """Calculate document-wide median font size for comparison baseline"""
    font_sizes = [block.font_size for block in blocks]

    # Remove outliers (top/bottom 5%)
    sorted_sizes = sorted(font_sizes)
    trim_count = len(sorted_sizes) // 20  # 5%
    trimmed = sorted_sizes[trim_count:-trim_count] if trim_count > 0 else sorted_sizes

    # Return 50th percentile
    return statistics.median(trimmed)
```

### Column Layout Detection (Early, Lightweight)
**Location:** Stage 2 (analysis.py) - before Phase 3

```python
def detect_two_column_layout(blocks: List[TextBlock]) -> bool:
    """
    Quick check: Is this likely a two-column paper?
    Check pages 1-2 for evidence of column layout.
    This runs EARLY in Stage 2 to inform all subsequent phases.
    """
    # Check first 2 pages (0 and 1 in 0-indexed)
    early_blocks = [b for b in blocks if b.page <= 1]

    if len(early_blocks) < 20:
        return False  # Not enough blocks to determine

    # Group by page and check each
    for page in [0, 1]:
        page_blocks = [b for b in early_blocks if b.page == page]
        if len(page_blocks) < 10:
            continue

        x_positions = [b.x0 for b in page_blocks]

        # Look for a significant gap in x-distribution
        sorted_x = sorted(x_positions)
        for i in range(1, len(sorted_x)):
            gap = sorted_x[i] - sorted_x[i-1]
            if gap > 40:  # Found a potential column gap
                gap_center = (sorted_x[i-1] + sorted_x[i]) / 2
                left = sum(1 for x in x_positions if x < gap_center - 20)
                right = sum(1 for x in x_positions if x > gap_center + 20)

                if left >= 5 and right >= 5:
                    return True  # Found two-column evidence

    return False  # No two-column evidence found

# Usage throughout pipeline:
# - Stage 2: Run once, store in StructureInfo.is_two_column
# - Phase 6: If is_two_column, abstract likely ends before column split
# - Phase 9: If is_two_column, apply column-aware reading (use extraction.py's precise detection)
# - Note: extraction.py still does its own per-page KMeans detection for precise text extraction
```

---

## Phase 3: Title Detection

### Algorithm
```python
def detect_title(blocks: List[TextBlock], page: int = 0) -> TitleResult:
    """
    Smart multi-line title assembly with affiliation filtering
    """
    # Candidate selection
    candidates = [
        block for block in blocks
        if block.page == page
        and block.y0 < page_height * 0.30  # Top 30% of page
        and (block.is_bold_large or block.is_regular_large)
    ]

    # Sort by vertical position
    candidates.sort(key=lambda b: b.y0)

    # Multi-line assembly
    title_blocks = []
    for block in candidates:
        if should_add_to_title(block, title_blocks):
            title_blocks.append(block)
        else:
            break

    # Combine and score
    title_text = " ".join([b.text for b in title_blocks])
    confidence = calculate_title_confidence(title_blocks, page_height)

    return TitleResult(
        text=title_text,
        detection_method=get_detection_method(title_blocks),
        confidence=confidence
    )

def should_add_to_title(block: TextBlock, current_blocks: List[TextBlock]) -> bool:
    """Multi-line assembly rules"""
    if not current_blocks:
        return True

    last_block = current_blocks[-1]

    # Assembly rules (EXACT thresholds)
    font_diff = abs(block.font_size - last_block.font_size)
    x_diff = abs(block.x0 - last_block.x0)
    vertical_gap = block.y0 - (last_block.y0 + last_block.height)
    max_gap = 1.5 * block.font_size

    # Check assembly conditions
    if font_diff > 1.5:  # Font difference threshold
        return False
    if x_diff > 15:  # Horizontal alignment threshold (px)
        return False
    if vertical_gap > max_gap:  # Vertical gap threshold
        return False

    # Stop if affiliation-like content detected
    affiliation_keywords = [
        'university', 'department', 'institute', 'college',
        'hospital', 'center', 'laboratory', '@', '.edu', '.org'
    ]
    text_lower = block.text.lower()
    if any(kw in text_lower for kw in affiliation_keywords):
        return False

    # Stop if author-like pattern (multiple commas)
    if block.text.count(',') >= 2:
        return False

    return True

def calculate_title_confidence(blocks: List[TextBlock], page_height: float) -> float:
    """Algorithmic confidence scoring"""
    if not blocks:
        return 0.0

    first_block = blocks[0]

    # Base confidence from position and typography
    if first_block.is_bold_large and first_block.y0 < page_height * 0.20:
        confidence = 1.0  # Bold, large, top 20%
    elif first_block.is_large and first_block.y0 < page_height * 0.30:
        confidence = 0.9  # Large, top 30%
    else:
        confidence = 0.7  # Location-based only

    # Apply penalties
    if not first_block.is_bold:
        confidence *= 0.95  # Small penalty for non-bold

    if len(blocks) > 3:
        confidence *= 0.95  # Unusual to have >3 line title

    return min(confidence, 1.0)

def get_detection_method(blocks: List[TextBlock]) -> str:
    if blocks and blocks[0].is_bold:
        return "heuristic_bold"
    else:
        return "heuristic_location"
```

### Data Model
```python
@dataclass
class TitleResult:
    text: str
    detection_method: str  # 'heuristic_bold' | 'heuristic_location'
    confidence: float  # 0.0-1.0
    blocks: List[TextBlock]  # Source blocks for debugging
```

---

## Phase 4: Authors Detection

### Algorithm
```python
def detect_authors(blocks: List[TextBlock], title_result: TitleResult) -> AuthorResult:
    """
    Name recognition with superscript parsing
    """
    if not title_result.blocks:
        return AuthorResult(text="", confidence=0.0)

    # Find blocks immediately after title
    last_title_block = title_result.blocks[-1]
    title_bottom = last_title_block.y0 + last_title_block.height
    max_gap = 3 * last_title_block.font_size

    candidates = [
        block for block in blocks
        if block.page == last_title_block.page
        and block.y0 > title_bottom
        and block.y0 < title_bottom + max_gap
    ]

    # Multi-line author assembly
    author_blocks = []
    for block in candidates:
        if is_author_block(block, author_blocks):
            author_blocks.append(block)
        else:
            break

    # Parse authors and superscripts
    authors = parse_author_names(author_blocks)
    confidence = calculate_author_confidence(author_blocks, authors)

    return AuthorResult(
        authors=authors,
        text=" ".join([b.text for b in author_blocks]),
        detection_method="heuristic_location",
        confidence=confidence
    )

def is_author_block(block: TextBlock, current_blocks: List[TextBlock]) -> bool:
    """Check if block contains author information"""
    text = block.text

    # Content heuristics
    has_commas = text.count(',') >= 1  # Authors separated by commas
    has_superscripts = any(c in text for c in '¹²³⁴⁵⁶⁷⁸⁹*†‡§¶')
    has_numbers = any(c in '1234567890' for c in text)  # Regular superscripts

    # Name pattern check
    name_pattern = r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b'  # First Last
    abbrev_pattern = r'\b[A-Z]\.\s*[A-Z][a-z]+\b'  # F. Last
    has_names = bool(re.search(name_pattern, text) or re.search(abbrev_pattern, text))

    # Stop conditions - affiliations detected
    affiliation_keywords = ['university', 'department', 'institute', '@', '.edu']
    if any(kw in text.lower() for kw in affiliation_keywords):
        return False

    # Must have author-like characteristics
    return has_commas or has_superscripts or has_names

def parse_author_names(blocks: List[TextBlock]) -> List[Author]:
    """Extract individual authors with superscripts"""
    authors = []
    full_text = " ".join([b.text for b in blocks])

    # Split on commas and 'and'
    tokens = re.split(r',|\sand\s', full_text)

    for token in tokens:
        token = token.strip()
        if not token:
            continue

        # Extract superscripts
        superscripts = re.findall(r'[¹²³⁴⁵⁶⁷⁸⁹*†‡§¶]+|\d+', token)
        name = re.sub(r'[¹²³⁴⁵⁶⁷⁸⁹*†‡§¶\d]+', '', token).strip()

        # Check for corresponding author marker
        is_corresponding = '*' in token or '†' in token or 'corresponding' in token.lower()

        authors.append(Author(
            name=name,
            affiliation_markers=superscripts,
            is_corresponding=is_corresponding
        ))

    return authors

def calculate_author_confidence(blocks: List[TextBlock], authors: List[Author]) -> float:
    """Algorithmic confidence scoring for authors"""
    if not blocks or not authors:
        return 0.0

    confidence = 0.8  # Base confidence for heuristic detection

    # Boost for strong signals
    if any(a.affiliation_markers for a in authors):
        confidence += 0.1  # Has superscripts

    if len(authors) >= 2:  # Multiple authors is typical
        confidence += 0.05

    # Check name pattern strength
    strong_names = sum(1 for a in authors if len(a.name.split()) >= 2)
    if strong_names / len(authors) > 0.8:
        confidence += 0.05  # Most have first+last name

    return min(confidence, 1.0)
```

### Data Model
```python
@dataclass
class Author:
    name: str
    affiliation_markers: List[str]  # ['1', '2', '*']
    is_corresponding: bool
    email: Optional[str] = None  # Filled in Phase 5

@dataclass
class AuthorResult:
    authors: List[Author]
    text: str  # Raw text for debugging
    detection_method: str
    confidence: float
```

---

## Phase 5: Affiliations Detection

### Algorithm
```python
def detect_affiliations(blocks: List[TextBlock], author_result: AuthorResult) -> AffiliationResult:
    """
    Institution extraction with email/location parsing
    """
    if not author_result.authors:
        return AffiliationResult(affiliations=[], confidence=0.0)

    # Find blocks after authors
    # ... (similar boundary detection as Phase 4)

    affiliation_blocks = []
    for block in candidates:
        if is_affiliation_block(block):
            affiliation_blocks.append(block)
        elif is_stopping_condition(block):
            break

    # Parse affiliations with markers
    affiliations = parse_affiliations(affiliation_blocks, author_result.authors)
    confidence = calculate_affiliation_confidence(affiliations)

    return AffiliationResult(
        affiliations=affiliations,
        detection_method="keyword_heuristic",
        confidence=confidence
    )

def is_affiliation_block(block: TextBlock) -> bool:
    """Check if block contains affiliation information"""
    text = block.text.lower()

    # Institution keywords
    institution_keywords = [
        'university', 'université', 'universität', 'college',
        'institute', 'department', 'school', 'hospital',
        'center', 'centre', 'laboratory', 'lab'
    ]

    # Location keywords
    location_keywords = [
        'usa', 'uk', 'china', 'germany', 'france', 'japan',
        'street', 'avenue', 'road', 'city'
    ]

    # Contact patterns
    has_email = '@' in block.text
    has_postal = bool(re.search(r'\b\d{5}(-\d{4})?\b', block.text))  # US ZIP

    return (
        any(kw in text for kw in institution_keywords) or
        any(kw in text for kw in location_keywords) or
        has_email or has_postal
    )

def is_stopping_condition(block: TextBlock) -> bool:
    """Check if we've reached the end of affiliations"""
    text_lower = block.text.lower()

    # Abstract start
    if 'abstract' in text_lower and block.is_bold:
        return True

    # Keywords section
    if 'keywords:' in text_lower:
        return True

    # Two-column transition (would need geometry info)
    # Large vertical gap (>3x font size from last block)

    return False

def parse_affiliations(blocks: List[TextBlock], authors: List[Author]) -> List[Affiliation]:
    """Extract individual affiliations with markers"""
    affiliations = []

    for block in blocks:
        # Look for markers at start (1, 2, *, †, a, b)
        marker_match = re.match(r'^([¹²³⁴⁵⁶⁷⁸⁹\d*†‡§¶a-z])\s*(.+)', block.text)

        if marker_match:
            marker = marker_match.group(1)
            text = marker_match.group(2)
        else:
            marker = None
            text = block.text

        # Extract components
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        email = email_match.group(0) if email_match else None

        # Clean text
        if email:
            text = text.replace(email, '').strip()

        affiliations.append(Affiliation(
            marker=marker,
            institution=text,
            email=email
        ))

    # Link emails back to authors
    for aff in affiliations:
        if aff.email and aff.marker:
            for author in authors:
                if aff.marker in author.affiliation_markers:
                    author.email = aff.email
                    break

    return affiliations

def calculate_affiliation_confidence(affiliations: List[Affiliation]) -> float:
    """Confidence scoring for affiliations"""
    if not affiliations:
        return 0.0

    confidence = 0.7  # Base for heuristic detection

    # Boost for strong signals
    strong_keywords = ['university', 'department', 'institute']
    for aff in affiliations:
        if any(kw in aff.institution.lower() for kw in strong_keywords):
            confidence = max(confidence, 0.9)
            break

    # Boost for marker alignment
    if all(aff.marker for aff in affiliations):
        confidence += 0.1

    return min(confidence, 1.0)
```

---

## Phase 6: Abstract Detection

### Algorithm
```python
def detect_abstract(blocks: List[TextBlock], affiliation_result: AffiliationResult) -> AbstractResult:
    """
    Intelligent paragraph identification (100-350 words)
    """
    # Find first substantial paragraph after affiliations
    # ... (boundary detection logic)

    abstract_blocks = []
    word_count = 0

    for block in candidates:
        # Content constraints
        words_in_block = len(block.text.split())

        # Check if this looks like abstract content
        if not contains_non_abstract_patterns(block):
            abstract_blocks.append(block)
            word_count += words_in_block

            # Stop conditions
            if word_count > 350:  # Max abstract size
                break
            if is_abstract_end(block):
                break

    # Validate as abstract
    if 100 <= word_count <= 350 and len(abstract_blocks) >= 1:
        confidence = calculate_abstract_confidence(word_count, abstract_blocks)
        text = " ".join([b.text for b in abstract_blocks])
    else:
        confidence = 0.0
        text = ""

    return AbstractResult(
        text=text,
        word_count=word_count,
        detection_method="heuristic_paragraph",
        confidence=confidence
    )

def contains_non_abstract_patterns(block: TextBlock) -> bool:
    """Check for patterns that indicate NOT abstract"""
    text_lower = block.text.lower()

    # Institution/author patterns
    if any(kw in text_lower for kw in ['university', 'department', '@']):
        return True

    # Figure/table references (uncommon in abstracts)
    if re.search(r'(figure|fig\.?|table)\s+\d+', text_lower):
        return True

    return False

def is_abstract_end(block: TextBlock) -> bool:
    """Check if we've reached end of abstract"""
    text_lower = block.text.lower()

    # Keywords section
    if 'keywords:' in text_lower:
        return True

    # Next section header (bold)
    if block.is_bold and any(
        kw in text_lower for kw in
        ['introduction', 'background', '1.', 'materials']
    ):
        return True

    return False

def calculate_abstract_confidence(word_count: int, blocks: List[TextBlock]) -> float:
    """Confidence scoring for abstract"""
    confidence = 0.7  # Base for position-based detection

    # Ideal word count range
    if 150 <= word_count <= 250:
        confidence += 0.1

    # Multiple sentences indicate paragraph
    text = " ".join([b.text for b in blocks])
    sentence_count = len(re.split(r'[.!?]\s+', text))
    if sentence_count >= 3:
        confidence += 0.1

    # Scientific terminology boost
    sci_terms = ['method', 'result', 'significant', 'analysis', 'study']
    if any(term in text.lower() for term in sci_terms):
        confidence += 0.1

    return min(confidence, 1.0)
```

---

## Phase 7: Introduction Detection

### Algorithm
```python
def detect_introduction(blocks: List[TextBlock], abstract_result: AbstractResult) -> SectionResult:
    """
    First body section recognition
    """
    # Find first section after abstract/keywords
    # This is straightforward - first bold or large text after abstract

    for block in blocks:
        if is_section_header(block) and is_after_abstract(block, abstract_result):
            return SectionResult(
                name="introduction",
                header_text=block.text,
                position=(block.page, block.y0),
                detection_method="heuristic_location",
                confidence=0.75 if not block.is_bold else 0.85
            )

    return SectionResult(name="introduction", confidence=0.0)

def is_section_header(block: TextBlock) -> bool:
    """Check if block looks like a section header"""
    return (
        block.is_bold_medium or
        block.is_regular_large or
        block.text.isupper() or  # ALL CAPS
        bool(re.match(r'^\d+\.?\s+', block.text))  # Numbered
    )
```

---

## Phase 8: Non-Bold Headers

### Algorithm
```python
def detect_non_bold_headers(blocks: List[TextBlock], detected_sections: List[SectionResult]) -> List[SectionResult]:
    """
    ALL CAPS and numbered section detection

    ONLY RUNS if detected_sections < 3 (indicates non-standard formatting)
    """
    if len(detected_sections) >= 3:
        return []  # Already found enough sections

    additional_headers = []

    for block in blocks:
        if is_non_bold_header(block):
            section = parse_non_bold_header(block)
            if section and section.name not in [s.name for s in detected_sections]:
                additional_headers.append(section)

    return additional_headers

def is_non_bold_header(block: TextBlock) -> bool:
    """Detect non-bold headers"""
    text = block.text.strip()

    # ALL CAPS headers
    if text.isupper() and len(text.split()) <= 4:
        return True

    # Numbered headers: "1. Introduction", "2.1 Methods"
    if re.match(r'^\d+(\.\d+)*\.?\s+[A-Z]', text):
        return True

    # Larger font (even if not bold)
    if block.font_size > document_median_font + 2:
        return True

    return False

def parse_non_bold_header(block: TextBlock) -> Optional[SectionResult]:
    """Parse and normalize non-bold header"""
    text = block.text.strip()

    # Remove numbering
    text_clean = re.sub(r'^\d+(\.\d+)*\.?\s+', '', text)

    # Normalize to lowercase
    normalized = text_clean.lower().strip()

    # Map to standard section names
    section_map = {
        'intro': 'introduction',
        'methods': 'methods',
        'materials and methods': 'materials_and_methods',
        'results': 'results',
        'discussion': 'discussion',
        'conclusion': 'conclusion',
        'conclusions': 'conclusion',
        'references': 'references',
        'bibliography': 'references'
    }

    section_name = section_map.get(normalized, normalized)

    return SectionResult(
        name=section_name,
        header_text=text,
        position=(block.page, block.y0),
        detection_method="non_bold_pattern",
        confidence=0.75
    )
```

---

## Phase 9: Section Content Extraction

### Algorithm
```python
def extract_section_content(
    blocks: List[TextBlock],
    sections: List[SectionResult],
    figure_captions: List[FigureCaption],
    is_two_column: bool  # From early detection in Stage 2
) -> Dict[str, str]:
    """
    Column-aware content assembly

    NOTE: At this stage (Phase 9), we're working with the markdown
    that extraction.py already produced with its precise KMeans column detection.
    The is_two_column flag just helps us understand the document structure.
    The actual column-aware text ordering was already handled by extraction.py.
    """
    # Sort sections by position
    sections_sorted = sorted(sections, key=lambda s: (s.position[0], s.position[1]))

    section_contents = {}

    for i, section in enumerate(sections_sorted):
        # Define section boundaries
        start_y = section.position[1] + section.header_height
        end_y = sections_sorted[i+1].position[1] if i+1 < len(sections_sorted) else float('inf')

        # Get blocks in section
        section_blocks = [
            b for b in blocks
            if b.page == section.position[0]
            and b.y0 >= start_y
            and b.y0 < end_y
            and not is_excluded_block(b, figure_captions)
        ]

        # Note: By Phase 9, we're working with already-extracted markdown
        # from extraction.py which has already handled column ordering.
        # This is more about understanding section boundaries and content assignment.

        # For raw block processing (if needed):
        if is_two_column:
            # Use simple heuristic for column division
            x_positions = [b.x0 for b in section_blocks]
            if x_positions:
                mid_x = (min(x_positions) + max(x_positions)) / 2
                left_blocks = [b for b in section_blocks if b.x0 < mid_x]
                right_blocks = [b for b in section_blocks if b.x0 >= mid_x]

                left_blocks.sort(key=lambda b: b.y0)
                right_blocks.sort(key=lambda b: b.y0)

                ordered_blocks = left_blocks + right_blocks
            else:
                ordered_blocks = []
        else:
            # Single column - simple vertical sort
            ordered_blocks = sorted(section_blocks, key=lambda b: b.y0)

        # Assemble text with de-hyphenation
        text = assemble_text_with_dehyphenation(ordered_blocks)
        section_contents[section.name] = text

    return section_contents

def is_excluded_block(block: TextBlock, figure_captions: List[FigureCaption]) -> bool:
    """
    Check if block should be excluded from section content
    Uses overlap-based exclusion for figure captions
    """
    # Check against figure captions
    for caption in figure_captions:
        overlap = calculate_overlap(block.bbox, caption.bbox)
        if overlap > 0.8:  # 80% overlap threshold
            return True

    # Check for other exclusions
    text_lower = block.text.lower()

    # Footnotes (small font, bottom of page)
    if block.font_size < 8 and block.y0 > page_height * 0.9:
        return True

    # Page numbers
    if re.match(r'^-?\s*\d+\s*-?$', block.text.strip()):
        return True

    return False

def assemble_text_with_dehyphenation(blocks: List[TextBlock]) -> str:
    """Assemble text with de-hyphenation and paragraph reconstruction"""
    lines = []

    for i, block in enumerate(blocks):
        text = block.text

        # De-hyphenation
        if text.endswith('-') and i+1 < len(blocks):
            next_text = blocks[i+1].text
            if next_text and next_text[0].islower():
                # Likely a hyphenated word
                text = text[:-1]  # Remove hyphen
                blocks[i+1].text = text + blocks[i+1].text
                continue  # Skip this block, merged with next

        lines.append(text)

    # Paragraph reconstruction
    paragraphs = []
    current_paragraph = []

    for line in lines:
        if not line.strip():
            # Empty line - paragraph break
            if current_paragraph:
                paragraphs.append(' '.join(current_paragraph))
                current_paragraph = []
        else:
            current_paragraph.append(line)

    if current_paragraph:
        paragraphs.append(' '.join(current_paragraph))

    return '\n\n'.join(paragraphs)
```

---

## Phase 10: Figures and Tables

### Algorithm
```python
def detect_figure_table_captions(blocks: List[TextBlock]) -> List[FigureCaption]:
    """
    Comprehensive caption extraction
    """
    captions = []

    for block in blocks:
        caption_match = is_caption(block.text)
        if caption_match:
            caption = parse_caption(block, caption_match)
            captions.append(caption)

    return captions

def is_caption(text: str) -> Optional[re.Match]:
    """Check if text is a figure/table caption"""
    patterns = [
        r'^(Figure|Fig\.?)\s+(\d+[A-Z]?)',
        r'^(Table)\s+(\d+[A-Z]?)',
        r'^(Scheme)\s+(\d+)',
        r'^(Figure|Fig\.?)\s+(S\d+)',  # Supplementary
    ]

    for pattern in patterns:
        match = re.match(pattern, text, re.IGNORECASE)
        if match:
            return match

    return None

def parse_caption(block: TextBlock, match: re.Match) -> FigureCaption:
    """Parse caption details"""
    caption_type = match.group(1).lower()
    if 'fig' in caption_type:
        caption_type = 'figure'
    elif 'table' in caption_type:
        caption_type = 'table'
    else:
        caption_type = 'scheme'

    number = match.group(2)

    # Full caption text (may span multiple blocks)
    full_text = block.text

    # Confidence based on typography
    confidence = 1.0 if block.is_bold else 0.8

    return FigureCaption(
        id=f"{caption_type}_{number}",
        type=caption_type,
        number=number,
        caption_text=full_text,
        page=block.page,
        bbox=block.bbox,
        confidence=confidence
    )
```

---

## Phase 11: Edge Case Handling

### Algorithm
```python
def handle_edge_cases(
    sections: Dict[str, str],
    blocks: List[TextBlock]
) -> Dict[str, Any]:
    """
    Combined sections, reference boundaries, ambiguous blocks
    """
    edge_cases = {
        'combined_sections': [],
        'references_end': None,
        'ambiguous_blocks': []
    }

    # Handle combined sections
    for section_name in sections:
        if 'results' in section_name and 'discussion' in section_name:
            # Combined Results and Discussion
            edge_cases['combined_sections'].append({
                'original': section_name,
                'split_into': ['results', 'discussion'],
                'note': 'Combined Results and Discussion section'
            })

            # Option: duplicate content to both sections
            sections['results'] = sections[section_name]
            sections['discussion'] = sections[section_name]

    # Detect true references endpoint (backward scanning)
    edge_cases['references_end'] = find_references_end(blocks)

    # Handle ambiguous blocks
    # ... (blocks that couldn't be assigned to sections)

    return edge_cases

def find_references_end(blocks: List[TextBlock]) -> Optional[int]:
    """
    Backward scanning to find true end of references
    """
    # Start from document end
    reversed_blocks = list(reversed(blocks))

    reference_pattern = re.compile(
        r'^\s*\[?\d+\]?\.?\s*'  # Number
        r'[A-Z][a-z]+.*'  # Author name
        r'\(\d{4}\)'  # Year
    )

    last_reference_index = None

    for i, block in enumerate(reversed_blocks):
        if reference_pattern.match(block.text):
            last_reference_index = len(blocks) - i - 1
        else:
            # Check if it's a section header (Supplementary, Appendix)
            if any(kw in block.text.lower() for kw in ['supplementary', 'appendix', 'supporting']):
                break

            # If we've seen references and now see non-reference content
            if last_reference_index is not None:
                # Allow a few non-matching blocks (might be formatting)
                if i - (len(blocks) - last_reference_index - 1) > 3:
                    break

    return last_reference_index
```

---

## Phase 12: Unparsed Content

### Algorithm
```python
def collect_unparsed_content(
    all_blocks: List[TextBlock],
    assigned_blocks: Set[TextBlock],
    figure_captions: List[FigureCaption]
) -> List[UnparsedBlock]:
    """
    Complete accounting of all text
    """
    unparsed = []

    for block in all_blocks:
        if block not in assigned_blocks:
            # Try to determine why it wasn't parsed
            reason = determine_unparsed_reason(block, figure_captions)

            unparsed.append(UnparsedBlock(
                text=block.text,
                page=block.page,
                bbox=block.bbox,
                possible_reason=reason
            ))

    return unparsed

def determine_unparsed_reason(block: TextBlock, captions: List[FigureCaption]) -> str:
    """Determine why a block wasn't parsed"""

    # Check if it's near a figure caption
    for caption in captions:
        if block.page == caption.page:
            distance = abs(block.y0 - caption.bbox[1])
            if distance < 50:  # Within 50pt of caption
                return "figure_artifact"

    # Check if it's a footer remnant
    if block.y0 > page_height * 0.95:
        return "footer_remnant"

    # Check if it's a header remnant
    if block.y0 < page_height * 0.05:
        return "header_remnant"

    # Check if it's between columns (gutter text)
    # ... (would need column boundaries)

    return "unknown"
```

---

## Data Models

### Core Detection Types
```python
from dataclasses import dataclass
from typing import List, Optional, Dict, Tuple

@dataclass
class DetectionResult:
    """Base class for all detection results"""
    text: str
    detection_method: str  # 'keyword', 'heuristic_bold', 'heuristic_location', etc.
    confidence: float  # 0.0-1.0

@dataclass
class TextBlock:
    """Input text block from PDF"""
    text: str
    page: int
    bbox: Tuple[float, float, float, float]  # x0, y0, x1, y1
    font_size: float
    font_name: str
    is_bold: bool
    is_italic: bool

    @property
    def is_bold_large(self) -> bool:
        return self.is_bold and self.font_size > document_median_font + 2

    @property
    def is_regular_large(self) -> bool:
        return self.font_size > document_median_font + 3

    @property
    def is_bold_medium(self) -> bool:
        return self.is_bold and self.font_size >= document_median_font

@dataclass
class SectionResult(DetectionResult):
    """Section header detection result"""
    name: str  # normalized section name
    header_text: str  # original header text
    position: Tuple[int, float]  # (page, y)
    header_height: float = 0.0
    level: int = 1  # 1=major, 2=subsection, 3=sub-subsection

@dataclass
class FigureCaption:
    """Figure/Table caption"""
    id: str  # e.g., "figure_1a"
    type: str  # 'figure', 'table', 'scheme'
    number: str  # e.g., "1A", "S2"
    caption_text: str
    page: int
    bbox: Tuple[float, float, float, float]
    confidence: float

@dataclass
class UnparsedBlock:
    """Content that couldn't be assigned"""
    text: str
    page: int
    bbox: Tuple[float, float, float, float]
    possible_reason: str  # 'figure_artifact', 'footer_remnant', 'unknown'

@dataclass
class DocumentLayout:
    """Document layout information from early detection"""
    is_two_column: bool  # True if evidence of two-column layout in pages 1-2
    # Note: extraction.py does its own precise per-page column detection later
```

### Confidence Scoring Algorithm
```python
class ConfidenceCalculator:
    """
    Unified confidence scoring algorithm
    """

    @staticmethod
    def calculate(
        base: float,
        factors: Dict[str, bool],
        penalties: Dict[str, float]
    ) -> float:
        """
        Calculate final confidence score

        Args:
            base: Starting confidence (e.g., 1.0 for exact keyword match)
            factors: Boolean conditions that affect confidence
            penalties: Multiplication penalties for negative factors

        Returns:
            Final confidence score between 0.0 and 1.0
        """
        confidence = base

        # Apply multiplicative penalties
        for factor, applies in factors.items():
            if applies and factor in penalties:
                confidence *= penalties[factor]

        return min(max(confidence, 0.0), 1.0)

    # Standard penalties
    STANDARD_PENALTIES = {
        'not_bold': 0.9,
        'wrong_location': 0.85,
        'no_keywords': 0.8,
        'ambiguous_structure': 0.9,
        'excessive_length': 0.95
    }
```

---

## Integration Strategy

### Enhancement Points in Existing Pipeline

1. **Stage 2 (analysis.py)** - Enhance `analyze_structure()`:
   - Add Phases 3-5 (Title, Authors, Affiliations detection)
   - Add confidence scoring to all detections
   - Add non-bold header detection (Phase 8)

2. **Stage 8 (formatting.py)** - Enhance `split_sections()`:
   - Use Phase 9 logic for content extraction
   - Leverage existing column detection from extraction.py
   - Add edge case handling (Phase 11)

3. **New Stage 13** - Add after Stage 12:
   - Implement Phase 12 (Unparsed Content tracking)
   - Complete accounting of all blocks

### Configuration Additions
```yaml
# In parser_config.yaml
analysis:
  # Title detection
  title_font_tolerance: 1.5  # pt
  title_x_alignment_tolerance: 15  # px
  title_vertical_gap_multiplier: 1.5

  # Author detection
  author_gap_multiplier: 3.0  # × title font size

  # Abstract constraints
  abstract_min_words: 100
  abstract_max_words: 350

  # Caption exclusion
  caption_overlap_threshold: 0.8  # 80%

  # Confidence thresholds
  min_confidence_to_accept: 0.6

  # Edge cases
  detect_combined_sections: true
  backward_scan_references: true
```

---

## Testing Strategy

### Test Categories

1. **Standard PDFs** - Should maintain 100% success rate
2. **Non-Bold Headers** - Papers with ALL CAPS or numbered sections
3. **Multi-line Titles** - Titles spanning 2-3 lines
4. **Complex Authors** - Multiple affiliations, superscripts, corresponding authors
5. **Combined Sections** - "Results and Discussion" type sections
6. **Missing Sections** - Papers without standard sections
7. **Edge Cases** - Unusual formatting, mixed columns

### Test Implementation
```python
# For each test PDF in backend/docs/testPDFs/
def test_comprehensive_analysis(pdf_path):
    """Test all 12 phases of analysis"""

    # Phase 3: Title
    assert title_result.confidence > 0.7
    assert title_result.text != ""

    # Phase 4: Authors
    assert len(author_result.authors) >= 1
    assert all(a.name for a in author_result.authors)

    # Phase 5: Affiliations
    assert len(affiliation_result.affiliations) >= 1

    # Phase 6: Abstract
    assert 100 <= abstract_result.word_count <= 350

    # Phase 9: Section content
    assert all(len(content) > 0 for content in section_contents.values())

    # Phase 10: Figures
    assert all(c.confidence > 0.7 for c in figure_captions)

    # Phase 11: Edge cases
    assert edge_cases['references_end'] is not None

    # Phase 12: Unparsed content
    unparsed_ratio = len(unparsed) / len(all_blocks)
    assert unparsed_ratio < 0.05  # Less than 5% unparsed
```

### Validation Metrics
- **Confidence Distribution**: Track average confidence per phase
- **Unparsed Ratio**: Percentage of blocks not assigned
- **Detection Success Rate**: How many papers have all required sections
- **Edge Case Frequency**: How often edge cases are triggered

---

## Implementation Phases

### Phase 1: Data Models & Confidence System (Day 1)
- Implement all dataclasses
- Create ConfidenceCalculator
- Add configuration options
- Unit tests for models

### Phase 2: Title, Authors, Affiliations (Day 2-3)
- Implement Phases 3-5 in analysis.py
- Multi-line assembly algorithms
- Superscript parsing
- Test on papers with complex author structures

### Phase 3: Abstract & Introduction (Day 4)
- Implement Phases 6-7
- Paragraph detection logic
- First body section heuristic
- Test on papers without "Abstract" header

### Phase 4: Non-Bold Headers & Content (Day 5-6)
- Implement Phase 8 (ALL CAPS, numbered)
- Enhance Phase 9 with column awareness
- Caption exclusion logic
- Test on papers with non-standard headers

### Phase 5: Edge Cases & Unparsed (Day 7)
- Implement Phases 11-12
- Reference endpoint detection
- Combined section handling
- Complete text accounting
- Test edge cases

### Phase 6: Integration & Testing (Day 8-9)
- Wire into existing pipeline
- Run full test suite
- Performance optimization
- Documentation updates

### Phase 7: Validation & Refinement (Day 10)
- Test on all PDFs in testPDFs/
- Analyze confidence scores
- Tune thresholds
- Fix edge cases
- Update PIPELINE_FLOW.md

---

## Success Criteria

1. **All test PDFs parse without errors**
2. **Confidence scores average > 0.8 across phases**
3. **Unparsed content < 5% of total blocks**
4. **Title, authors, abstract detected in 100% of papers**
5. **Section content properly extracted with column awareness**
6. **Figure captions excluded from section text**
7. **Edge cases handled gracefully with logging**

---

## Notes

- **Column detection**: We leverage pymupdf4llm's existing column detection to avoid duplicate computation
- **Confidence is quality, not fallback**: High confidence = high quality detection
- **Progressive detection**: Each phase depends on previous results
- **Complete accounting**: Phase 12 ensures nothing is lost
- **Backward compatibility**: Existing pipeline continues to work while we enhance