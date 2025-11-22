# Manuscript Review Assistant - Project Architecture

## Executive Summary

Build a web application that accepts scientific manuscripts and returns deep, actionable feedback similar to Refine.ink. The system parses documents, runs parallel analysis agents, and presents structured feedback through a clean interface.

**Timeline:** 2 weeks  
**Deliverables:** GitHub repo + functional demo with working review pipeline

**Key Differentiators (What Makes This Not "Just Another GPT Wrapper"):**
1. **Track A/B Split** - Objective "desk-reject" checks vs subjective polish suggestions
2. **Citation Police** - Detects lazy/imprecise citation behavior (most tools ignore this)
3. **Figure Agent** - Explicitly reasons about figures, captions, and text references (Refine doesn't touch figures)

---

## Scope: What We're Building vs What We're Not

### ✅ IN SCOPE (Demo-Ready)

| Feature | Notes |
|---------|-------|
| PDF upload & parsing | Primary format, uses `pymupdf4llm` |
| Section-based review | Abstract, Intro, Methods, Results, Discussion |
| Track A (Objective) | Critical/Major issues that would cause desk rejection |
| Track B (Suggestive) | Polish and style improvements |
| Cross-Document Consistency | Numbers, notation, citations match across sections |
| Citation Police | Lazy citation detection with Review Paper Exception |
| Figure Agent (text-only) | Dangling refs, orphaned figures, caption-text match |
| Simple UI | Upload → Results viewer with quote-based highlighting |
| DEMO_MODE | Pre-baked results for demo paper to avoid API failures |

### ❌ OUT OF SCOPE (Deferred)

| Feature | Reason |
|---------|--------|
| .tex / LaTeX support | Accept compiled PDFs only |
| .docx support | Stub for later; PDF is primary |
| Redis/Celery queues | Use in-process `asyncio.gather` |
| Authentication | Anonymous upload with session ID |
| Payment/Stripe | Not needed for demo |
| Figure vision analysis | No image pixel analysis in V0 |
| Mobile responsive | Desktop-first for demo |
| User-selectable agents | Fixed pipeline |

---

## Technical Decisions (Locked In)

### 1. PDF Parsing Strategy
- **Primary:** `pymupdf4llm` → Markdown with structure
- **Section splitting:** Regex-based heading detection
- **Fallback:** If regex fails, single LLM call to get section boundaries

```python
SECTION_TITLES = ["abstract", "introduction", "methods", "results", "discussion"]

def split_sections(md_text: str) -> Dict[str, str]:
    # Look for markdown headings containing these keywords
    # Fallback: LLM call for boundary detection
    ...
```

### 2. Demo Mode (Avoid API Failures in Interview)
```python
DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"

def get_citation_police_report(doc_hash: str) -> CitationPoliceReport:
    if DEMO_MODE and doc_hash == DEMO_PAPER_HASH:
        return load_json("fixtures/demo_citation_police.json")
    return call_semantic_scholar_live(...)
```

### 3. No Line Numbers (Avoid Hallucinations)
```python
class TextLocation(BaseModel):
    section: str
    paragraph_index: int
    quote: str  # Exact excerpt - frontend does fuzzy matching
    # NO line_number field!
```

Frontend uses `findClosestMatch(quote, sectionText)` for highlighting.

### 4. Agent Architecture: Section + Ability Hybrid

**Vertical (Section) Reviewers:**
- AbstractReviewer
- IntroductionReviewer  
- MethodsReviewer
- ResultsReviewer
- DiscussionReviewer

**Horizontal (Ability) Specialists:**
- CrossDocConsistency
- CitationPolice
- FigureAgent

Each returns both Track A and Track B in the same response.

---

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND (Next.js)                             │
│  ┌─────────────┐  ┌─────────────┐  ┌───────────────────────────────────────┐│
│  │   Landing   │  │   Upload    │  │         Results Viewer                ││
│  │    Page     │  │   (drag &   │  │  Left: Text    Right: Issues by Card  ││
│  │             │  │    drop)    │  │  Quote-based highlighting             ││
│  └─────────────┘  └─────────────┘  └───────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              API LAYER (FastAPI)                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────────────────┐  │
│  │   /upload   │  │  /review    │  │  /results/{id}                      │  │
│  │  (PDF→MD)   │  │  (trigger)  │  │  (get FullReviewOutput)             │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PROCESSING PIPELINE                               │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  DOCUMENT PARSER: pymupdf4llm → Markdown → Section Split              │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                      │                                      │
│                                      ▼                                      │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  AGENT ORCHESTRATOR: asyncio.gather (no Redis/Celery)                 │  │
│  │                                                                       │  │
│  │   SECTION REVIEWERS              SPECIALIZED AGENTS                   │  │
│  │   ┌─────────┐ ┌─────────┐        ┌─────────────────────────────────┐  │  │
│  │   │Abstract │ │  Intro  │        │ CrossDocConsistency             │  │  │
│  │   │Reviewer │ │Reviewer │        │ (numbers, notation, terms)      │  │  │
│  │   └─────────┘ └─────────┘        └─────────────────────────────────┘  │  │
│  │   ┌─────────┐ ┌─────────┐        ┌─────────────────────────────────┐  │  │
│  │   │ Methods │ │ Results │        │ CitationPolice ⭐                │  │  │
│  │   │Reviewer │ │Reviewer │        │ (lazy/imprecise citations)      │  │  │
│  │   └─────────┘ └─────────┘        └─────────────────────────────────┘  │  │
│  │   ┌─────────┐                    ┌─────────────────────────────────┐  │  │
│  │   │  Disc   │                    │ FigureAgent ⭐                  │  │  │
│  │   │Reviewer │                    │ (refs, captions, text-only)     │  │  │
│  │   └─────────┘                    └─────────────────────────────────┘  │  │
│  │                                                                       │  │
│  │   Each reviewer returns: track_a_issues + track_b_suggestions         │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                              │                                              │
│                              ▼                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                      RESULT SYNTHESIZER                               │  │
│  │   Deduplication  │  Priority Scoring  │  Output Formatting            │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  OUTPUT: FullReviewOutput JSON                                        │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DATA LAYER (Simplified for Demo)                    │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  In-Memory Storage + Local Filesystem (no Redis/Postgres for demo)  │    │
│  │  - Uploaded PDFs: /tmp/uploads/{session_id}/                        │    │
│  │  - Results cache: Python dict (or SQLite if persistence needed)     │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase Breakdown (Interview-Ready Timeline)

### Phase 0: Foundation (Day 1)
**Goal:** Upload PDF, see it parsed into sections

#### Tasks
- [ ] **P0.1** Initialize GitHub repo with monorepo structure
- [ ] **P0.2** Set up Next.js frontend with Tailwind + shadcn/ui
- [ ] **P0.3** Set up FastAPI backend
- [ ] **P0.4** Create `/upload` endpoint: PDF → `pymupdf4llm` → Markdown
- [ ] **P0.5** Implement section splitter (regex + fallback LLM call)
- [ ] **P0.6** Return `ParsedDocument` JSON to frontend
- [ ] **P0.7** Basic UI: show sections in tabs/accordion

#### Deliverable
Upload a PDF → see extracted sections on screen

---

### Phase 2: Specialized Agents (Days 4-5)
**Goal:** CrossDoc + FigureAgent + CitationPolice stub

#### Tasks
- [ ] **P2.1** Implement `CrossDocConsistency` agent (Track A only)
  - Citation-bibliography matching
  - Number consistency across sections
  - Terminology consistency
- [ ] **P2.2** Implement `FigureAgent` (Track A + B, text-only)
  - Sequential numbering check
  - Dangling references
  - Orphaned figures
  - Caption-text consistency
- [ ] **P2.3** Implement `CitationPolice` with DEMO_MODE
  - If demo paper: return pre-baked JSON from fixtures
  - If other paper: run in local mode (pattern detection without Semantic Scholar)
- [ ] **P2.4** Add Citation Police Card and Figure Card to frontend

#### Deliverable
Full Track A pipeline working for all agents

---

### Phase 3: Remaining Reviewers + Polish (Days 6-7)
**Goal:** Complete all section reviewers, polish UI

#### Tasks
- [ ] **P3.1** Implement `AbstractReviewer` (Track A + B)
- [ ] **P3.2** Implement `IntroductionReviewer` (Track A + B)
- [ ] **P3.3** Implement `DiscussionReviewer` (Track A + B)
- [ ] **P3.4** Build quote-based highlighting in frontend
  - `findClosestMatch(quote, sectionText)` function
  - Click issue → scroll to highlighted text
- [ ] **P3.5** Add Track A / Track B filter toggle
- [ ] **P3.6** Loading states and error handling

#### Deliverable
All 8 reviewers working, UI is polished enough for demo

---

### Phase 4: Demo Prep (Days 8-10)
**Goal:** Lock in demo, prepare talking points

#### Tasks
- [ ] **P4.1** Create demo paper with known issues
  - Missing IRB
  - Dangling figure reference
  - Lazy citation (general claim + primary source)
- [ ] **P4.2** Pre-bake `CitationPoliceReport` for demo paper
- [ ] **P4.3** Test full pipeline end-to-end
- [ ] **P4.4** Deploy to Vercel (frontend) + Railway/Render (backend)
- [ ] **P4.5** Write README with architecture explanation
- [ ] **P4.6** Prepare demo script and talking points

#### Deliverable
Live URL, working demo, clear story to tell

---

## Core Data Models

These are the types everything else revolves around. All models use Pydantic.

### Document Structure Models

```python
from pydantic import BaseModel
from typing import Optional, List, Dict
from enum import Enum

class Sentence(BaseModel):
    """Individual sentence with precise location for highlighting."""
    id: str                    # Unique ID: "methods-s3"
    section: str               # "methods", "results", etc.
    text: str
    char_start: int            # Offset in section text
    char_end: int
    paragraph_index: int

class ParsedSection(BaseModel):
    """A single section of the paper."""
    name: str                  # "abstract", "methods", etc.
    text: str                  # Full text of section
    sentences: List[Sentence]  # Indexed sentences

class FigureBlock(BaseModel):
    """A figure with its caption."""
    id: str                    # "fig-1"
    label: str                 # "Figure 1", "Fig. 2"
    caption: str
    page: int
    image_path: Optional[str]  # For future vision pass

class FigureRef(BaseModel):
    """An in-text reference to a figure."""
    label: str                 # "Figure 1"
    section: str
    sentence_id: str
    sentence_text: str

class CitationRef(BaseModel):
    """An in-text citation."""
    id: str                    # "[3]" or "Smith 2020"
    section: str
    sentence_id: str
    sentence_text: str         # The claim being supported

class BibliographyEntry(BaseModel):
    """A bibliography/references entry."""
    id: str                    # Normalized key matching CitationRef.id
    raw_text: str
    doi: Optional[str]
    is_review_paper: Optional[bool]  # From Semantic Scholar or mock

class ParsedDocument(BaseModel):
    """Complete parsed representation of a paper."""
    doc_id: str
    doc_hash: str              # SHA-256 for DEMO_MODE matching
    title: str
    sections: Dict[str, ParsedSection]
    figures: List[FigureBlock]
    figure_refs: List[FigureRef]
    citations: List[CitationRef]
    bibliography: List[BibliographyEntry]
    raw_markdown: str          # Original pymupdf4llm output
```

### Issue & Report Models

```python
class Severity(str, Enum):
    CRITICAL = "critical"      # Would cause desk rejection
    MAJOR = "major"            # Significant problem
    MINOR = "minor"            # Should fix but not fatal
    SUGGESTION = "suggestion"  # Optional improvement

class TextLocation(BaseModel):
    """Where an issue was found - NO LINE NUMBERS (avoids hallucinations)."""
    section: str
    sentence_id: Optional[str]
    paragraph_index: Optional[int]
    quote: str                 # Exact excerpt for fuzzy matching

class Issue(BaseModel):
    """A single issue found by an agent."""
    issue_type: str            # See ISSUE_TYPES below
    severity: Severity
    description: str
    location: TextLocation
    evidence: Optional[str]    # Supporting quotes/data
    suggestion: Optional[str]  # How to fix (for Track B)
    guideline_violation: bool = False  # Flag for journal/reporting guideline issues

# Standard issue_type values (not exhaustive, agents can add more)
ISSUE_TYPES = {
    # Methods - Reporting Guidelines
    "missing_ethics_statement": "IRB/ethics approval not mentioned",
    "missing_conflict_of_interest": "COI declaration not found",
    "missing_data_availability": "Data availability statement missing",
    "missing_trial_registration": "Clinical trial registration not provided",
    "missing_consort_flow": "CONSORT flow diagram missing for RCT",
    "missing_prisma_checklist": "PRISMA checklist not referenced for systematic review",
    
    # Methods - Content
    "missing_sample_size": "Sample size (N) not explicitly stated",
    "missing_inclusion_criteria": "Inclusion/exclusion criteria not defined",
    "missing_statistical_methods": "Statistical methods not described",
    "tense_inconsistency": "Methods should use past tense",
    
    # Results
    "dangling_figure_ref": "Figure referenced but not defined",
    "orphaned_figure": "Figure defined but never referenced",
    "n_inconsistency": "Sample size differs between sections",
    "missing_effect_size": "Effect size not reported with p-value",
    
    # Citations
    "lazy_citation": "General claim supported by specific/primary source",
    "imprecise_citation": "Specific claim supported by review paper",
    "missing_citation": "Claim requires citation but none provided",
    "dangling_citation": "Citation has no matching bibliography entry",
    
    # Cross-Document
    "number_contradiction": "Same metric has different values in different sections",
    "terminology_inconsistency": "Term used inconsistently across paper",
    
    # Figures
    "caption_text_mismatch": "Caption doesn't match referencing text",
    "vague_caption": "Caption lacks specific information",
    "duplicate_figure_number": "Multiple figures share same number",
}

# Which issue_types are guideline violations (auto-flag)
GUIDELINE_ISSUE_TYPES = {
    "missing_ethics_statement",
    "missing_conflict_of_interest", 
    "missing_data_availability",
    "missing_trial_registration",
    "missing_consort_flow",
    "missing_prisma_checklist",
}
```

### Guideline Violations: Matching ReviewerZero's UX

To match/beat ReviewerZero's "Structured Review Report" with separate Guideline Violations section:

**Backend:** Issues with `guideline_violation=True` are surfaced separately.

```python
def flag_guideline_violations(issues: List[Issue]) -> List[Issue]:
    """Auto-flag known guideline issue types."""
    for issue in issues:
        if issue.issue_type in GUIDELINE_ISSUE_TYPES:
            issue.guideline_violation = True
    return issues
```

**Frontend Grouping:** One panel that groups issues into 4 buckets:

| Bucket | Condition | Color |
|--------|-----------|-------|
| **Major Issues** | `severity in {CRITICAL, MAJOR}` and not guideline | 🔴 Red |
| **Minor Issues** | `severity = MINOR` | 🟡 Yellow |
| **Additional Comments** | `severity = SUGGESTION` | 🔵 Blue |
| **Guideline Violations** | `guideline_violation = True` | 🟣 Purple (separate section) |

Note: Guideline violations can overlap with Major/Minor severity but get their own dedicated bucket in the UI.

```typescript
// Frontend grouping logic
function groupIssues(issues: Issue[]) {
  return {
    guidelineViolations: issues.filter(i => i.guideline_violation),
    majorIssues: issues.filter(i => 
      ['critical', 'major'].includes(i.severity) && !i.guideline_violation
    ),
    minorIssues: issues.filter(i => 
      i.severity === 'minor' && !i.guideline_violation
    ),
    additionalComments: issues.filter(i => 
      i.severity === 'suggestion' && !i.guideline_violation
    ),
  };
}
```

### Implementation Options for Guideline Checks

**Option A: Extend existing agents** (recommended for V0)
- MethodsReviewer checks for ethics, COI, data availability
- CrossDocAgent checks for trial registration in front-matter
- Tag specific checks with `guideline_violation=True`

**Option B: Dedicated GuidelinesAgent** (cleaner separation)
- Runs over: Methods + front-matter + tail sections (Acknowledgements, Declarations)
- Single-purpose agent, easier to maintain guideline-specific prompts

For V0, Option A is faster. Option B can be added later.

---

### Report Models (continued)

```python
class SectionReviewReport(BaseModel):
    """Output from a section reviewer (contains both tracks)."""
    section: str
    track_a_issues: List[Issue]
    track_b_suggestions: List[Issue]
    passed_checks: List[str]
    summary: Optional[str]

class CrossDocReport(BaseModel):
    """Output from CrossDocConsistency agent."""
    issues: List[Issue]
    consistency_score: float   # 0-1
    ns_found: Dict[str, List[int]]  # Section → N values found

class CitationPoliceReport(BaseModel):
    """Output from CitationPolice agent."""
    total_citations: int
    lazy_citations: List[Issue]
    imprecise_citations: List[Issue]
    appropriate_citations: int

class FigureReport(BaseModel):
    """Output from FigureAgent."""
    total_figures: int
    track_a_issues: List[Issue]
    track_b_suggestions: List[Issue]
    passed_checks: List[str]

class OverallStatus(str, Enum):
    PASS = "pass"
    MAJOR_ISSUES = "major_issues"
    CRITICAL_ISSUES = "critical_issues"

class GroupedIssues(BaseModel):
    """Issues grouped by severity/type for ReviewerZero-style UI."""
    major_issues: List[Issue]           # CRITICAL + MAJOR, not guideline
    minor_issues: List[Issue]           # MINOR, not guideline
    additional_comments: List[Issue]    # SUGGESTION, not guideline
    guideline_violations: List[Issue]   # Any issue with guideline_violation=True

class FullReviewOutput(BaseModel):
    """Final aggregated output sent to frontend."""
    document_id: str
    title: str
    
    # Detailed reports by source
    sections: List[SectionReviewReport]
    cross_doc: CrossDocReport
    citation_police: CitationPoliceReport
    figures: FigureReport
    
    # Grouped for ReviewerZero-style UI
    grouped_issues: GroupedIssues
    
    # Summary
    overall_status: OverallStatus
    summary: str
    processing_time_seconds: float

def build_grouped_issues(all_issues: List[Issue]) -> GroupedIssues:
    """Group all issues into 4 buckets for the UI."""
    return GroupedIssues(
        guideline_violations=[i for i in all_issues if i.guideline_violation],
        major_issues=[i for i in all_issues 
                      if i.severity in {Severity.CRITICAL, Severity.MAJOR} 
                      and not i.guideline_violation],
        minor_issues=[i for i in all_issues 
                      if i.severity == Severity.MINOR 
                      and not i.guideline_violation],
        additional_comments=[i for i in all_issues 
                             if i.severity == Severity.SUGGESTION 
                             and not i.guideline_violation],
    )
```

---

## Index Layer (The "Refine-Style Magic")

These are **pure Python helpers** that pre-compute lookups without calling any LLM. This is what makes cross-document consistency checks fast and accurate.

### CrossDocIndex

Extracts and indexes numbers, terms, and notation across sections.

```python
class CrossDocIndex(BaseModel):
    """Pre-computed cross-document lookups."""
    ns_by_section: Dict[str, List[int]]           # {"methods": [150, 75], "results": [150]}
    key_numbers: Dict[str, List[float]]           # {"p_values": [0.05, 0.01], "means": [3.5, 4.2]}
    term_to_sentence_ids: Dict[str, List[str]]    # {"ANOVA": ["methods-s5", "results-s12"]}
    notation_map: Dict[str, str]                  # {"α": "significance level", "N": "sample size"}

class CrossDocIndexer:
    """Builds CrossDocIndex from ParsedDocument."""
    
    N_PATTERNS = [
        r'[Nn]\s*=\s*(\d+)',
        r'(\d+)\s+participants',
        r'(\d+)\s+subjects',
        r'sample\s+(?:size|of)\s+(\d+)',
    ]
    
    def build(self, doc: ParsedDocument) -> CrossDocIndex:
        ns_by_section = {}
        for section_name, section in doc.sections.items():
            ns_by_section[section_name] = self._extract_ns(section.text)
        
        return CrossDocIndex(
            ns_by_section=ns_by_section,
            key_numbers=self._extract_key_numbers(doc),
            term_to_sentence_ids=self._build_term_index(doc),
            notation_map=self._extract_notation(doc),
        )
    
    def _extract_ns(self, text: str) -> List[int]:
        # Regex extraction of sample sizes
        ...
    
    def find_sentences_by_term(self, doc: ParsedDocument, term: str) -> List[Sentence]:
        """Helper for agents to find all mentions of a term."""
        ...
```

### CitationIndex

Maps citations to bibliography entries and tracks which claims cite which sources.

```python
class CitationIndex(BaseModel):
    """Pre-computed citation lookups."""
    citation_to_bib: Dict[str, BibliographyEntry]      # "[3]" → BibEntry
    bib_to_citations: Dict[str, List[CitationRef]]     # "smith2020" → [CitationRef, ...]
    unmatched_citations: List[str]                      # Citations with no bib entry
    unmatched_bib_entries: List[str]                    # Bib entries never cited

class CitationIndexer:
    """Builds CitationIndex from ParsedDocument."""
    
    def build(self, doc: ParsedDocument) -> CitationIndex:
        citation_to_bib = {}
        bib_to_citations = defaultdict(list)
        
        # Match citations to bibliography entries
        for citation in doc.citations:
            matching_bib = self._find_matching_bib(citation, doc.bibliography)
            if matching_bib:
                citation_to_bib[citation.id] = matching_bib
                bib_to_citations[matching_bib.id].append(citation)
        
        return CitationIndex(
            citation_to_bib=citation_to_bib,
            bib_to_citations=dict(bib_to_citations),
            unmatched_citations=self._find_unmatched_citations(doc),
            unmatched_bib_entries=self._find_unmatched_bib(doc),
        )
```

### FigureIndex

Maps figure labels to their blocks and all references.

```python
class FigureIndex(BaseModel):
    """Pre-computed figure lookups."""
    label_to_figure: Dict[str, FigureBlock]        # "Figure 1" → FigureBlock
    label_to_refs: Dict[str, List[FigureRef]]      # "Figure 1" → [ref1, ref2, ...]
    dangling_refs: List[FigureRef]                  # Refs to non-existent figures
    orphaned_figures: List[FigureBlock]             # Figures never referenced

class FigureIndexer:
    """Builds FigureIndex from ParsedDocument."""
    
    def build(self, doc: ParsedDocument) -> FigureIndex:
        label_to_figure = {self._normalize(f.label): f for f in doc.figures}
        label_to_refs = defaultdict(list)
        
        for ref in doc.figure_refs:
            label_to_refs[self._normalize(ref.label)].append(ref)
        
        # Find dangling refs (ref to figure that doesn't exist)
        dangling = [r for r in doc.figure_refs 
                    if self._normalize(r.label) not in label_to_figure]
        
        # Find orphaned figures (figure never referenced)
        orphaned = [f for f in doc.figures 
                    if self._normalize(f.label) not in label_to_refs]
        
        return FigureIndex(
            label_to_figure=label_to_figure,
            label_to_refs=dict(label_to_refs),
            dangling_refs=dangling,
            orphaned_figures=orphaned,
        )
    
    def _normalize(self, label: str) -> str:
        """Normalize 'Figure 1', 'Fig. 1', 'FIGURE 1' → 'figure_1'"""
        return re.sub(r'[^a-z0-9]', '_', label.lower()).strip('_')
```

### AgentContext

The standard input passed to all agents, containing the document and all indices.

```python
class AgentContext(BaseModel):
    """Everything an agent needs to do its job."""
    doc: ParsedDocument
    cross: CrossDocIndex
    citations: CitationIndex
    figures: FigureIndex
    
    class Config:
        arbitrary_types_allowed = True
```

---

## Ingestion & Parsing Layer

### DocumentBuilder

Single orchestrator that chains all parsers to produce a `ParsedDocument`.

```python
class DocumentBuilder:
    """Orchestrates PDF → ParsedDocument conversion."""
    
    def __init__(self):
        self.pdf_parser = PdfParser()
        self.section_splitter = SectionSplitter()
        self.sentence_indexer = SentenceIndexer()
        self.citation_extractor = CitationExtractor()
        self.bibliography_parser = BibliographyParser()
        self.figure_extractor = FigureExtractor()
    
    def build(self, pdf_bytes: bytes, filename: str) -> ParsedDocument:
        # Step 1: PDF → Markdown
        markdown = self.pdf_parser.parse(pdf_bytes)
        
        # Step 2: Split into sections
        sections = self.section_splitter.split(markdown)
        
        # Step 3: Index sentences within each section
        for section in sections.values():
            section.sentences = self.sentence_indexer.index(section)
        
        # Step 4: Extract citations and bibliography
        citations = self.citation_extractor.extract(sections)
        bibliography = self.bibliography_parser.parse(
            sections.get("references", ParsedSection(name="references", text="", sentences=[]))
        )
        
        # Step 5: Extract figures and references
        figures, figure_refs = self.figure_extractor.extract(markdown, sections)
        
        # Step 6: Compute document hash for DEMO_MODE
        doc_hash = hashlib.sha256(pdf_bytes).hexdigest()
        
        return ParsedDocument(
            doc_id=str(uuid.uuid4()),
            doc_hash=doc_hash,
            title=self._extract_title(markdown),
            sections=sections,
            figures=figures,
            figure_refs=figure_refs,
            citations=citations,
            bibliography=bibliography,
            raw_markdown=markdown,
        )
```

### Component Implementations

```python
class PdfParser:
    """Wraps pymupdf4llm for PDF → Markdown conversion."""
    
    def parse(self, pdf_bytes: bytes) -> str:
        import pymupdf4llm
        # Returns markdown with structure preserved
        return pymupdf4llm.to_markdown(pdf_bytes)

class SectionSplitter:
    """Splits markdown into named sections."""
    
    SECTION_PATTERNS = [
        (r'#+\s*abstract', 'abstract'),
        (r'#+\s*introduction', 'introduction'),
        (r'#+\s*methods?', 'methods'),
        (r'#+\s*results?', 'results'),
        (r'#+\s*discussion', 'discussion'),
        (r'#+\s*references?', 'references'),
    ]
    
    def split(self, markdown: str) -> Dict[str, ParsedSection]:
        sections = {}
        # Try regex-based splitting first
        sections = self._regex_split(markdown)
        
        # Fallback to LLM if regex fails
        if len(sections) < 3:
            sections = self._llm_fallback(markdown)
        
        return sections
    
    def _regex_split(self, markdown: str) -> Dict[str, ParsedSection]:
        # Find section boundaries using heading patterns
        ...
    
    def _llm_fallback(self, markdown: str) -> Dict[str, ParsedSection]:
        # Single LLM call to get section boundaries
        prompt = """Given this paper markdown, return JSON with section boundaries:
        {"abstract": {"start": 0, "end": 500}, "introduction": {"start": 501, "end": 2000}, ...}
        """
        ...

class SentenceIndexer:
    """Splits section text into indexed sentences."""
    
    def index(self, section: ParsedSection) -> List[Sentence]:
        import nltk
        sentences = []
        raw_sentences = nltk.sent_tokenize(section.text)
        
        char_pos = 0
        for i, sent_text in enumerate(raw_sentences):
            start = section.text.find(sent_text, char_pos)
            end = start + len(sent_text)
            
            sentences.append(Sentence(
                id=f"{section.name}-s{i}",
                section=section.name,
                text=sent_text,
                char_start=start,
                char_end=end,
                paragraph_index=self._get_paragraph_index(section.text, start),
            ))
            char_pos = end
        
        return sentences

class CitationExtractor:
    """Extracts in-text citations."""
    
    PATTERNS = [
        r'\[(\d+(?:,\s*\d+)*)\]',           # [1], [1, 2, 3]
        r'\(([A-Z][a-z]+(?:\s+et\s+al\.?)?,?\s*\d{4})\)',  # (Smith, 2020)
    ]
    
    def extract(self, sections: Dict[str, ParsedSection]) -> List[CitationRef]:
        citations = []
        for section_name, section in sections.items():
            if section_name == "references":
                continue
            for sentence in section.sentences:
                for pattern in self.PATTERNS:
                    for match in re.finditer(pattern, sentence.text):
                        citations.append(CitationRef(
                            id=match.group(1),
                            section=section_name,
                            sentence_id=sentence.id,
                            sentence_text=sentence.text,
                        ))
        return citations

class FigureExtractor:
    """Extracts figure blocks and in-text references."""
    
    FIGURE_BLOCK_PATTERN = r'(Figure\s+\d+)[.:]\s*(.+?)(?=\n\n|\Z)'
    FIGURE_REF_PATTERN = r'(Fig(?:ure)?\.?\s*\d+)'
    
    def extract(self, markdown: str, sections: Dict[str, ParsedSection]) -> Tuple[List[FigureBlock], List[FigureRef]]:
        figures = self._extract_figure_blocks(markdown)
        refs = self._extract_figure_refs(sections)
        return figures, refs
```

---

## Agent Layer

### Base Agent Architecture

```python
class BaseAgent:
    """Base class for all review agents."""
    
    name: str
    target_section: Optional[str] = None  # None for horizontal agents
    
    def __init__(self, llm_client):
        self.llm = llm_client
    
    async def run(self, ctx: AgentContext) -> Union[SectionReviewReport, CrossDocReport, CitationPoliceReport, FigureReport]:
        prompt = self.build_prompt(ctx)
        response = await self.llm.complete(prompt)
        return self.parse_response(response)
    
    def build_prompt(self, ctx: AgentContext) -> str:
        raise NotImplementedError
    
    def parse_response(self, response: str) -> BaseModel:
        raise NotImplementedError
    
    def get_section_text(self, ctx: AgentContext) -> str:
        """Helper: get this agent's target section text."""
        if self.target_section and self.target_section in ctx.doc.sections:
            return ctx.doc.sections[self.target_section].text
        return ""
    
    def get_cross_section_context(self, ctx: AgentContext, terms: List[str]) -> str:
        """Helper: find mentions of terms in other sections for context."""
        snippets = []
        for term in terms:
            sentences = ctx.cross.term_to_sentence_ids.get(term, [])
            for sent_id in sentences[:3]:  # Limit to 3 per term
                # Find the sentence and add it
                ...
        return "\n".join(snippets)
```

### Section Reviewers (Vertical Agents)

Each section reviewer returns **both Track A and Track B** in a single call.

```python
class MethodsReviewer(BaseAgent):
    """Reviews the Methods section."""
    
    name = "methods_reviewer"
    target_section = "methods"
    
    def build_prompt(self, ctx: AgentContext) -> str:
        methods_text = self.get_section_text(ctx)
        
        # Get N values found across document for consistency check
        ns_elsewhere = {k: v for k, v in ctx.cross.ns_by_section.items() 
                        if k != "methods"}
        
        return METHODS_PROMPT_TEMPLATE.format(
            methods_text=methods_text,
            ns_in_methods=ctx.cross.ns_by_section.get("methods", []),
            ns_elsewhere=ns_elsewhere,
        )
    
    def parse_response(self, response: str) -> SectionReviewReport:
        data = json.loads(response)
        return SectionReviewReport(
            section="methods",
            track_a_issues=[Issue(**i) for i in data.get("track_a_issues", [])],
            track_b_suggestions=[Issue(**i) for i in data.get("track_b_suggestions", [])],
            passed_checks=data.get("passed_checks", []),
            summary=data.get("summary"),
        )

# Similar implementations for:
# - AbstractReviewer
# - IntroductionReviewer  
# - ResultsReviewer
# - DiscussionReviewer
```

### Horizontal Agents (Ability Specialists)

```python
class CrossDocConsistencyAgent(BaseAgent):
    """Checks consistency across all sections."""
    
    name = "cross_doc_consistency"
    target_section = None
    
    def build_prompt(self, ctx: AgentContext) -> str:
        # Build compact summary of cross-doc data
        payload = {
            "ns_by_section": ctx.cross.ns_by_section,
            "key_numbers": ctx.cross.key_numbers,
            "unmatched_citations": ctx.citations.unmatched_citations,
            "unmatched_bib_entries": ctx.citations.unmatched_bib_entries,
        }
        return CROSS_DOC_PROMPT_TEMPLATE.format(payload=json.dumps(payload))

class CitationPoliceAgent(BaseAgent):
    """Detects lazy and imprecise citations."""
    
    name = "citation_police"
    target_section = None
    
    def build_prompt(self, ctx: AgentContext) -> str:
        # Build list of claim-citation pairs with metadata
        items = []
        for citation in ctx.doc.citations:
            bib_entry = ctx.citations.citation_to_bib.get(citation.id)
            items.append({
                "claim": citation.sentence_text,
                "citation_id": citation.id,
                "cited_paper": bib_entry.raw_text if bib_entry else "UNKNOWN",
                "is_review": bib_entry.is_review_paper if bib_entry else None,
                "section": citation.section,
            })
        return CITATION_POLICE_PROMPT_TEMPLATE.format(items=json.dumps(items))

class FigureAgent(BaseAgent):
    """Checks figure-caption-text consistency."""
    
    name = "figure_agent"
    target_section = None
    
    def build_prompt(self, ctx: AgentContext) -> str:
        # FigureIndex already computed dangling refs and orphaned figures!
        payload = {
            "figures": [f.model_dump() for f in ctx.doc.figures],
            "figure_refs": [r.model_dump() for r in ctx.doc.figure_refs],
            "dangling_refs": [r.model_dump() for r in ctx.figures.dangling_refs],
            "orphaned_figures": [f.model_dump() for f in ctx.figures.orphaned_figures],
        }
        return FIGURE_PROMPT_TEMPLATE.format(payload=json.dumps(payload))
```

---

## Orchestrator Layer

### ReviewOrchestrator

The main entry point that coordinates everything.

```python
class ReviewOrchestrator:
    """Orchestrates the full review pipeline."""
    
    def __init__(self, llm_client):
        self.document_builder = DocumentBuilder()
        self.agents = [
            # Section reviewers
            AbstractReviewer(llm_client),
            IntroductionReviewer(llm_client),
            MethodsReviewer(llm_client),
            ResultsReviewer(llm_client),
            DiscussionReviewer(llm_client),
            # Horizontal agents
            CrossDocConsistencyAgent(llm_client),
            CitationPoliceAgent(llm_client),
            FigureAgent(llm_client),
        ]
    
    async def review(self, pdf_bytes: bytes, filename: str) -> FullReviewOutput:
        start_time = time.time()
        
        # Step 1: Parse document
        doc = self.document_builder.build(pdf_bytes, filename)
        
        # Step 2: Build indices (pure Python, fast)
        cross_index = CrossDocIndexer().build(doc)
        citation_index = CitationIndexer().build(doc)
        figure_index = FigureIndexer().build(doc)
        
        # Step 3: Create agent context
        ctx = AgentContext(
            doc=doc,
            cross=cross_index,
            citations=citation_index,
            figures=figure_index,
        )
        
        # Step 4: Check for DEMO_MODE
        if DEMO_MODE and doc.doc_hash == DEMO_PAPER_HASH:
            return self._load_demo_results(doc.doc_id)
        
        # Step 5: Run all agents in parallel
        results = await asyncio.gather(*[
            agent.run(ctx) for agent in self.agents
        ])
        
        # Step 6: Aggregate results
        output = self._aggregate(doc, results, time.time() - start_time)
        
        return output
    
    def _aggregate(self, doc: ParsedDocument, results: List, processing_time: float) -> FullReviewOutput:
        section_reports = [r for r in results if isinstance(r, SectionReviewReport)]
        cross_doc = next(r for r in results if isinstance(r, CrossDocReport))
        citation_police = next(r for r in results if isinstance(r, CitationPoliceReport))
        figures = next(r for r in results if isinstance(r, FigureReport))
        
        # Determine overall status
        all_issues = []
        for report in section_reports:
            all_issues.extend(report.track_a_issues)
        all_issues.extend(cross_doc.issues)
        all_issues.extend(citation_police.lazy_citations)
        all_issues.extend(figures.track_a_issues)
        
        if any(i.severity == Severity.CRITICAL for i in all_issues):
            status = OverallStatus.CRITICAL_ISSUES
        elif any(i.severity == Severity.MAJOR for i in all_issues):
            status = OverallStatus.MAJOR_ISSUES
        else:
            status = OverallStatus.PASS
        
        return FullReviewOutput(
            document_id=doc.doc_id,
            title=doc.title,
            sections=section_reports,
            cross_doc=cross_doc,
            citation_police=citation_police,
            figures=figures,
            overall_status=status,
            summary=self._build_summary(status, all_issues),
            processing_time_seconds=processing_time,
        )
```

---

## Core Framework: Track A/B Split

**This is the key architectural insight.** Every agent returns BOTH tracks in a single response:

### Track A: Objective Audit (The "Desk Reject" Pass)
- **Binary checks:** Pass/Fail, no subjectivity
- **Verifiable:** Can be confirmed without domain expertise  
- **Severity:** Critical or Major only
- **Examples:** Missing IRB statement, undefined sample size, citation without bibliography entry

### Track B: Suggestive Critique (The "Peer Review" Pass)
- **Improvement suggestions:** Not errors, but opportunities
- **Subjective:** Reasonable people might disagree
- **Severity:** Minor or Suggestion only
- **Examples:** Passive voice, could add subheadings, sentence could be clearer

**Key Design Decision:** Single agent per section/ability returns both tracks (not separate Track A and Track B agents).

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SINGLE AGENT → BOTH TRACKS                               │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                      MethodsReviewer                                │   │
│   │                                                                     │   │
│   │   Input: AgentContext (doc + indices)                               │   │
│   │                          │                                          │   │
│   │                          ▼                                          │   │
│   │   ┌─────────────────────────────────────────────────────────────┐   │   │
│   │   │              Single LLM Call with Both Checklists           │   │   │
│   │   └─────────────────────────────────────────────────────────────┘   │   │
│   │                          │                                          │   │
│   │            ┌─────────────┴─────────────┐                            │   │
│   │            ▼                           ▼                            │   │
│   │   ┌───────────────────┐       ┌───────────────────┐                 │   │
│   │   │   track_a_issues  │       │ track_b_suggestions│                │   │
│   │   │   (Critical/Major)│       │   (Minor/Suggest)  │                │   │
│   │   └───────────────────┘       └───────────────────┘                 │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   Why single agent?                                                         │
│   • One LLM call instead of two (cost & latency)                            │
│   • Shared context (don't duplicate section text)                           │
│   • Coherent reasoning across both tracks                                   │
│   • Frontend can filter by track without backend changes                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Section-Specific Agent Specifications

### Methods Section Agent

**Track A Checks (Objective - V0):**
| Check | Condition | Severity |
|-------|-----------|----------|
| Study Type Classification | Detect: Human, Animal, Simulation, Review, Meta-analysis | Required |
| IRB/Ethics Statement | If Human/Animal study → must have ethics approval | Critical |
| Sample Size (N) | Must be explicitly stated | Major |
| Inclusion/Exclusion Criteria | Must be defined for empirical studies | Major |
| Statistical Methods | Must describe tests used | Major |
| Tense Consistency | Methods should be past tense (completed study) | Major |
| Internal Contradictions | Numbers here must match elsewhere | Critical |

**Track B Suggestions (Subjective - V1):**
| Category | Example |
|----------|---------|
| Structure | "Consider breaking into subheadings: Participants, Design, Analysis" |
| Detail | "Manufacturer locations missing for key reagents" |
| Conciseness | "This paragraph could be tightened by 30%" |
| Clarity | "The order of procedures is unclear" |

---

### Results Section Agent

**Track A Checks (Objective - V0):**
| Check | Condition | Severity |
|-------|-----------|----------|
| Figure/Table References | Every "Figure X" must correspond to actual figure | Critical |
| Statistical Reporting | P-values, confidence intervals present where claimed | Major |
| Sample Size Consistency | N in Results matches N in Methods | Critical |
| Data-Claim Alignment | Claims must be supported by presented data | Critical |
| Unit Consistency | Same units used throughout | Major |

**Track B Suggestions (Subjective - V1):**
| Category | Example |
|----------|---------|
| Presentation Order | "Consider presenting results in order of hypotheses" |
| Data Grouping | "These three paragraphs could be consolidated" |
| Visualization | "This data might be clearer as a figure" |

---

### Introduction Section Agent

**Track A Checks (Objective - V0):**
| Check | Condition | Severity |
|-------|-----------|----------|
| Citation Presence | Claims about prior work must have citations | Critical |
| Hypothesis/Aims Stated | Must clearly state research question | Major |
| Citation-Bibliography Match | All citations have bibliography entries | Critical |
| No Results Spoilers | Introduction shouldn't reveal specific findings | Major |

**Track B Suggestions (Subjective - V1):**
| Category | Example |
|----------|---------|
| Narrative Flow | "The transition from paragraph 2 to 3 is abrupt" |
| Scope | "Background section could be more focused" |
| Gap Statement | "The research gap could be stated more explicitly" |

---

### Discussion Section Agent

**Track A Checks (Objective - V0):**
| Check | Condition | Severity |
|-------|-----------|----------|
| Results Reference | Discussion must reference actual results | Critical |
| No New Data | Cannot introduce new results here | Critical |
| Limitation Acknowledgment | Must acknowledge study limitations | Major |
| Conclusion-Evidence Match | Conclusions must be supported by results | Critical |

**Track B Suggestions (Subjective - V1):**
| Category | Example |
|----------|---------|
| Alternative Explanations | "Consider addressing alternative interpretations" |
| Future Directions | "Future research section could be more specific" |
| Broader Impact | "Could better articulate significance" |

---

### Abstract Agent

**Track A Checks (Objective - V0):**
| Check | Condition | Severity |
|-------|-----------|----------|
| Structure Completeness | Must have: Background, Methods, Results, Conclusion | Major |
| Claim-Paper Consistency | Every claim must appear in main text | Critical |
| No Undefined Abbreviations | Cannot use abbreviations not defined in abstract | Major |

**Track B Suggestions (Subjective - V1):**
| Category | Example |
|----------|---------|
| Impact Statement | "Could strengthen the significance statement" |
| Quantitative Results | "Consider including key numerical findings" |

---

### Cross-Document Agent

**Track A Checks (Objective - V0):**
| Check | Condition | Severity |
|-------|-----------|----------|
| Notation Consistency | Same symbol = same meaning throughout | Critical |
| Number Consistency | Sample sizes, percentages match across sections | Critical |
| Citation Integrity | All in-text citations in bibliography (and vice versa) | Critical |
| Figure/Table Accounting | All figures/tables referenced; all references valid | Critical |
| Terminology Consistency | Same term used for same concept | Major |

**Track B Suggestions (Subjective - V1):**
| Category | Example |
|----------|---------|
| Narrative Arc | "The story from Intro to Discussion could be tighter" |
| Redundancy | "This point is made in both Methods and Results" |
| Balance | "Discussion is disproportionately long vs Results" |

---

### Citation Police Agent (Semantic Scholar) ⭐ KEY DIFFERENTIATOR

**This is an LLM agent** enhanced with Semantic Scholar API data.
It analyzes whether citations are used appropriately in context.

**The Core Problem:**
- Author makes general claim: "LLMs are transforming biology [1]"
- They cite YOUR specific tool paper instead of a survey
- This is lazy scholarship and dilutes your citation impact

**The Review Paper Exception:**
Not all "general claim + citation" pairs are lazy. If the cited paper IS a review/survey, 
that's actually correct scholarship. We must check paper type before flagging.

**Data Flow:**
```
Bibliography DOIs → Semantic Scholar API → Get publicationTypes → Pass to LLM Agent
                                                    ↓
                              is_review_paper: true/false for each citation
```

**Implementation: `backend/services/semantic_scholar_service.py`**

```python
import os
import httpx
from typing import Dict, List, Optional, Any

class PaperMetadata(BaseModel):
    doi: str
    title: str
    abstract: Optional[str]
    publication_types: List[str]  # e.g., ["Review", "JournalArticle"]
    is_review_paper: bool
    citation_count: Optional[int]

class SemanticScholarService:
    """
    Fetches paper metadata including publication type.
    Used to determine if a citation is a Review/Survey vs Primary Source.
    """
    
    def __init__(self):
        self.api_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY")  # Optional, increases rate limit
        self.base_url = "https://api.semanticscholar.org/graph/v1"
        self.headers = {"x-api-key": self.api_key} if self.api_key else {}
    
    async def get_paper_metadata(self, doi: str) -> Optional[PaperMetadata]:
        """Fetch paper details including publication type."""
        
        # Request fields we need
        fields = "title,abstract,publicationTypes,citationCount"
        url = f"{self.base_url}/paper/DOI:{doi}?fields={fields}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers, timeout=10.0)
                
                if response.status_code == 404:
                    return None  # Paper not found
                    
                if response.status_code != 200:
                    return None
                
                data = response.json()
                
                # Determine if this is a review paper
                pub_types = data.get("publicationTypes") or []
                title = data.get("title") or ""
                
                is_review = (
                    "Review" in pub_types or
                    "MetaAnalysis" in pub_types or
                    "survey" in title.lower() or
                    "review" in title.lower()
                )
                
                return PaperMetadata(
                    doi=doi,
                    title=title,
                    abstract=data.get("abstract"),
                    publication_types=pub_types,
                    is_review_paper=is_review,
                    citation_count=data.get("citationCount")
                )
                
            except httpx.TimeoutException:
                return None
    
    async def batch_get_metadata(self, dois: List[str]) -> Dict[str, PaperMetadata]:
        """Fetch metadata for multiple papers."""
        results = {}
        for doi in dois:
            metadata = await self.get_paper_metadata(doi)
            if metadata:
                results[doi] = metadata
        return results
```

**Citation Police Prompt: `prompts/citation_police_track_b.md`**

```markdown
You are the "Citation Police" - an expert at detecting lazy or inappropriate citations.

You will receive:
1. A sentence from the manuscript containing a citation
2. The cited paper's title and abstract
3. Whether the cited paper is a Review/Survey (is_review_paper: true/false)

Your job: Determine if the citation is APPROPRIATE for the claim being made.

---

### CLASSIFICATION RULES

**STEP 1: Classify the CLAIM type**
- GENERAL CLAIM: Background statement, widely accepted fact, field overview
  - Examples: "Machine learning is popular in biology", "Proteins fold in complex ways"
- SPECIFIC CLAIM: Particular result, method attribution, numerical finding
  - Examples: "Model X achieved 90% accuracy", "We used the method from [12]"

**STEP 2: Classify the CITATION type**
- REVIEW/SURVEY: is_review_paper = true
- PRIMARY SOURCE: is_review_paper = false (original research, tool paper, method paper)

**STEP 3: Apply the Logic Matrix**

| Claim Type | Citation Type | Verdict |
|------------|---------------|---------|
| GENERAL | REVIEW | ✅ PASS - Correct way to cite consensus |
| GENERAL | PRIMARY | ⚠️ FLAG - Lazy citation |
| SPECIFIC | REVIEW | ⚠️ FLAG - Imprecise, find primary source |
| SPECIFIC | PRIMARY | ✅ PASS - Appropriate (if content matches) |

---

### OUTPUT FORMAT

For each citation analyzed, return:
```json
{
  "citation_id": "string",
  "claim_text": "the sentence containing the citation",
  "claim_type": "general|specific",
  "cited_paper_type": "review|primary",
  "verdict": "pass|flag",
  "issue_type": null | "lazy_citation" | "imprecise_citation" | "content_mismatch",
  "explanation": "Why this was flagged (or null if pass)",
  "suggestion": "How to fix it (or null if pass)"
}
```

---

### EXAMPLES

**Example 1: PASS (General + Review)**
- Claim: "Large language models have shown remarkable capabilities across domains [1]"
- Cited Paper: "A Survey of Large Language Models" (is_review_paper: true)
- Verdict: ✅ PASS - Citing a survey for a general statement is correct.

**Example 2: FLAG (General + Primary)**  
- Claim: "Deep learning has revolutionized protein structure prediction [2]"
- Cited Paper: "AlphaFold2: Highly accurate protein structure prediction" (is_review_paper: false)
- Verdict: ⚠️ FLAG
- Issue: lazy_citation
- Explanation: "You cite AlphaFold2 (a specific tool) for a general claim about the field. AlphaFold2 is ONE example, not proof of a field-wide revolution."
- Suggestion: "Cite a review paper about ML in structural biology, OR rewrite to: 'Tools like AlphaFold2 [2] have advanced protein structure prediction.'"

**Example 3: FLAG (Specific + Review)**
- Claim: "The transformer architecture uses self-attention mechanisms [3]"
- Cited Paper: "A Survey of Transformers" (is_review_paper: true)
- Verdict: ⚠️ FLAG
- Issue: imprecise_citation
- Explanation: "You describe a specific architectural component but cite a survey. Find the original Transformer paper."
- Suggestion: "Cite Vaswani et al. 'Attention Is All You Need' for the original architecture."

**Example 4: PASS (Specific + Primary)**
- Claim: "We used the preprocessing pipeline from BioToolX [4]"
- Cited Paper: "BioToolX: A pipeline for biological data" (is_review_paper: false)
- Verdict: ✅ PASS - Citing the original tool for method attribution is correct.
```

**Track B Output Schema:**

```python
class CitationPoliceIssue(BaseModel):
    citation_id: str
    claim_text: str
    claim_type: Literal["general", "specific"]
    cited_paper_type: Literal["review", "primary"]
    verdict: Literal["pass", "flag"]
    issue_type: Optional[Literal["lazy_citation", "imprecise_citation", "content_mismatch"]]
    explanation: Optional[str]
    suggestion: Optional[str]

class CitationPoliceReport(BaseModel):
    total_citations_analyzed: int
    issues: List[CitationPoliceIssue]
    lazy_citation_count: int
    imprecise_citation_count: int
```

**Integration with Pipeline:**

```
Phase 1: DOI Extraction (from bibliography)
    ↓
Phase 2: Semantic Scholar API → Publication Types (is_review_paper)
    ↓
Phase 3: LLM Agent → Analyzes claim-citation pairs with is_review_paper context
    ↓
Output: CitationPoliceReport (lazy/imprecise citations flagged)
```

**DOI Extraction: `backend/services/parser/doi_extractor.py`**

```python
import re
from typing import List

class DOIExtractor:
    """Extract DOIs from bibliography text."""
    
    # Standard DOI regex pattern
    DOI_PATTERN = re.compile(
        r'\b(10\.\d{4,}/[^\s\]>"]+)',
        re.IGNORECASE
    )
    
    @classmethod
    def extract_from_text(cls, text: str) -> List[str]:
        """Extract all DOIs from text."""
        matches = cls.DOI_PATTERN.findall(text)
        # Clean up trailing punctuation
        cleaned = [re.sub(r'[.,;:\'")\]]+$', '', doi) for doi in matches]
        return list(set(cleaned))  # Deduplicate
    
    @classmethod
    def extract_from_bibliography(cls, bib_entries: List[str]) -> List[str]:
        """Extract DOIs from list of bibliography entries."""
        all_dois = []
        for entry in bib_entries:
            all_dois.extend(cls.extract_from_text(entry))
        return list(set(all_dois))
```

**Frontend Component: Citation Police Card**

```
┌─────────────────────────────────────────────────────┐
│  📚 CITATION QUALITY                                │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ✅ 38 Citations Analyzed                           │
│                                                     │
│  ⚠️  2 Lazy Citations Detected                      │
│     └─ Line 45: General claim cites specific tool   │
│     └─ Line 89: Background cites your method paper  │
│                                                     │
│  ⚠️  1 Imprecise Citation                           │
│     └─ Line 112: Specific claim cites a review      │
│                                                     │
│  ✅ 35 Appropriate Citations                        │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Frontend Component: Guideline Violations Card**

```
┌─────────────────────────────────────────────────────┐
│  📋 GUIDELINE VIOLATIONS                            │
├─────────────────────────────────────────────────────┤
│                                                     │
│  🟣 3 Reporting Guideline Issues                    │
│                                                     │
│  🔴 Missing Ethics Statement                        │
│     └─ Methods: No IRB/ethics approval mentioned    │
│     └─ Suggestion: Add ethics approval statement    │
│                                                     │
│  🔴 Missing Data Availability                       │
│     └─ No data availability statement found         │
│     └─ Suggestion: Add statement per journal policy │
│                                                     │
│  🟡 Missing Conflict of Interest                    │
│     └─ COI declaration not found in Declarations    │
│     └─ Suggestion: Add COI statement                │
│                                                     │
│  ✅ Trial Registration: N/A (not a clinical trial)  │
│  ✅ CONSORT/PRISMA: N/A (not RCT/systematic review) │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Frontend Component: Structured Review Summary (ReviewerZero-style)**

Groups all issues into 4 buckets for the main results view:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  📊 REVIEW SUMMARY                                          Overall: ⚠️     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  🔴 MAJOR ISSUES (3)                              [Click to expand]         │
│  ├─ Methods: Sample size not explicitly stated                              │
│  ├─ Results: Figure 3 referenced but not defined                            │
│  └─ Cross-Doc: N=150 in Methods, N=148 in Results                           │
│                                                                             │
│  🟡 MINOR ISSUES (5)                              [Click to expand]         │
│  ├─ Methods: Consider adding power analysis                                 │
│  ├─ Results: Effect sizes not reported with p-values                        │
│  └─ ... 3 more                                                              │
│                                                                             │
│  🔵 ADDITIONAL COMMENTS (4)                       [Click to expand]         │
│  ├─ Introduction: Could strengthen transition to hypothesis                 │
│  ├─ Discussion: Consider adding limitation about sample demographics        │
│  └─ ... 2 more                                                              │
│                                                                             │
│  🟣 GUIDELINE VIOLATIONS (2)                      [Click to expand]         │
│  ├─ Missing ethics statement (IRB approval)                                 │
│  └─ Missing data availability statement                                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### Figure Agent ⭐ ANOTHER KEY DIFFERENTIATOR

**Refine doesn't touch figures. Most tools don't.**
We explicitly reason about figures, captions, and their relationship to text.

**Goal:**
1. Ensure figure ↔ caption ↔ in-text references are structurally and logically consistent
2. (Optional) Use vision to check that caption actually matches what's drawn

**Data Model for Figures:**

```python
class FigureBlock(BaseModel):
    label: str              # "Figure 1", "Fig. 2", etc.
    caption: str
    image_bytes: Optional[bytes]  # For vision pass (V1)
    page_number: int
    bounding_box: Optional[Tuple[float, float, float, float]]

class ParsedDocument(BaseModel):
    # ... existing fields ...
    figures: List[FigureBlock]
    figure_refs: List[FigureReference]  # All "Figure X" mentions in text

class FigureReference(BaseModel):
    label: str              # "Figure 1"
    section: str            # Where it's mentioned
    paragraph_index: int
    sentence: str           # The sentence containing the reference
```

---

#### Figure Agent Track A (Objective - V0)

**F1: Label-Caption Integrity**
| Check | Condition | Severity |
|-------|-----------|----------|
| Sequential Numbering | Figures numbered 1, 2, 3... without gaps | Critical |
| No Duplicates | No two figures share the same number | Critical |
| Captions Non-Empty | Every figure has a caption | Major |

**F2: In-Text Reference Integrity**
| Check | Condition | Severity |
|-------|-----------|----------|
| Dangling References | Every "Figure X" in text has a matching captioned figure | Critical |
| Orphaned Figures | Every captioned figure is referenced at least once in text | Major |

**F3: Placement Sanity**
| Check | Condition | Severity |
|-------|-----------|----------|
| Section Appropriateness | Result figures should be referenced in Results, not just Methods | Major |
| Forward References | Figures should be introduced before detailed discussion | Minor |

**F4: Caption-Text Consistency (Textual)**
| Check | Condition | Severity |
|-------|-----------|----------|
| Topic Alignment | Caption topic matches the claim in referencing sentence | Critical |
| Direction Alignment | If text says "X increases", caption shouldn't imply "X decreases" | Critical |

**Track A Output Example:**

```json
{
  "section": "figures",
  "issues": [
    {
      "issue_type": "missing_figure",
      "severity": "critical",
      "description": "Text references 'Figure 3', but there is no Figure 3 caption.",
      "location": {
        "section": "Results",
        "paragraph_index": 4,
        "quote": "As shown in Figure 3, treatment efficacy increased..."
      },
      "evidence": "Existing figures: Figure 1, Figure 2, Figure 4."
    },
    {
      "issue_type": "orphaned_figure",
      "severity": "major",
      "description": "Figure 5 has a caption but is never referenced in the text.",
      "location": {
        "section": "figures",
        "paragraph_index": null,
        "quote": "Figure 5: Supplementary analysis of control group."
      }
    }
  ],
  "passed_checks": ["sequential_numbering", "all_captions_nonempty", "no_duplicates"]
}
```

---

#### Figure Agent Track B (Suggestive - V1)

**S1: Caption Quality**
| Category | Example |
|----------|---------|
| Too Vague | "Caption 'Results of experiment 1' is uninformative. Consider including variables, direction of effect, and sample size." |
| Missing Units | "Caption doesn't specify units for the Y-axis." |

**S2: Redundancy**
| Category | Example |
|----------|---------|
| Caption-Text Duplication | "Caption duplicates sentence in paragraph 3 verbatim. Consider making caption more informative." |

**S3: Visual Storytelling**
| Category | Example |
|----------|---------|
| Late Introduction | "Figure 4 isn't referenced until the final paragraph. Consider introducing earlier." |
| Consolidation | "Figures 2 and 3 show similar relationships. Consider merging into a multi-panel figure." |

---

#### Vision Pass (Optional - V1+)

If GPT-4o or Claude vision is available, add a second step:

**For each FigureBlock (cap at 3-5 for demo):**
1. Send: `image + caption + referencing sentences`
2. Prompt: "Does the caption accurately describe the patterns visible? Does the referencing text align?"

**Vision Output:**

```json
{
  "figure_label": "Figure 2",
  "caption_matches_figure": true,
  "text_matches_figure": false,
  "issues": [
    {
      "issue_type": "text_misinterpretation",
      "severity": "critical",
      "description": "Text claims treatment B outperforms A, but figure clearly shows higher values for A.",
      "location": {...}
    }
  ]
}
```

**Integration with Track A:**
- `caption_matches_figure = false` → Critical: "Caption does not correctly describe the plotted data."
- `text_matches_figure = false` → Critical: "Text misstates the direction/magnitude shown in figure."

**Architecture for Vision (plug-in ready):**

```python
class FigureAnalyzer:
    def __init__(self, use_vision: bool = False):
        self.use_vision = use_vision
    
    async def analyze(self, figure: FigureBlock, references: List[FigureReference]) -> FigureAnalysis:
        # Always run text-based checks
        text_issues = await self._check_text_consistency(figure, references)
        
        # Optionally run vision checks
        vision_issues = []
        if self.use_vision and figure.image_bytes:
            vision_issues = await self._check_with_vision(figure, references)
        
        return FigureAnalysis(
            figure_label=figure.label,
            text_issues=text_issues,
            vision_issues=vision_issues
        )
    
    async def _check_with_vision(self, figure: FigureBlock, references: List[FigureReference]):
        # Swap this implementation later without touching rest of agent
        pass
```

---

**Frontend Component: Figure Card**

```
┌─────────────────────────────────────────────────────┐
│  📊 FIGURES & CAPTIONS                              │
├─────────────────────────────────────────────────────┤
│                                                     │
│  🔴 1 Critical Issue                                │
│     └─ Figure 3 referenced but not defined          │
│                                                     │
│  ⚠️  2 Major Issues                                 │
│     └─ Figure 5 never referenced in text            │
│     └─ Caption for Fig 2 too vague                  │
│                                                     │
│  ✅ 4 Figures consistent and well-placed            │
│                                                     │
│  👁️ Vision Check: Not enabled (upgrade to V1)       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

**Figure Agent Prompt: `prompts/figure_track_a.md`**

```markdown
You are the "Figure Specialist" for a high-impact scientific journal.

You will receive:
1. A list of all figures with their labels and captions
2. A list of all in-text figure references with their surrounding sentences
3. Section context for each reference

### TRACK A: OBJECTIVE CHECKS

**F1: Label-Caption Integrity**
☐ Are figures numbered sequentially (1, 2, 3...) without gaps?
  - Severity: CRITICAL if gap (e.g., 1, 2, 4 but no 3)
☐ Are there duplicate figure numbers?
  - Severity: CRITICAL if duplicates
☐ Does every figure have a non-empty caption?
  - Severity: MAJOR if caption is missing or just the label

**F2: Reference Integrity**
☐ Does every "Figure X" / "Fig. X" in text have a matching captioned figure?
  - Severity: CRITICAL if reference to non-existent figure (dangling reference)
☐ Is every captioned figure referenced at least once in the text?
  - Severity: MAJOR if figure exists but is never mentioned (orphaned figure)

**F3: Placement Sanity**
☐ Are result figures referenced in Results section (not just Methods)?
  - Severity: MAJOR if outcome figure only mentioned in Methods
☐ Are figures introduced before detailed discussion of their content?
  - Severity: MINOR if figure discussed in detail before first mention

**F4: Caption-Text Consistency**
For each figure reference, compare the caption to the referencing sentence:
☐ Do they describe the same variables/concepts?
  - Severity: CRITICAL if clearly different topics
☐ If directionality is claimed (X increases, Y decreases), does caption support it?
  - Severity: CRITICAL if text claims opposite of what caption describes

### OUTPUT FORMAT
Return JSON with:
- issues: array of issues found
- passed_checks: array of check names that passed

Each issue must include:
- issue_type: "missing_figure" | "orphaned_figure" | "duplicate_label" | "gap_in_numbering" | "caption_text_mismatch" | "wrong_section"
- severity: "critical" | "major" | "minor"
- description: Clear explanation
- location: Where the issue was found
- evidence: Supporting quotes from both caption and text if applicable
```

```python
from typing import List, Optional, Literal
from pydantic import BaseModel, Field

# --- Shared Components ---
class TextLocation(BaseModel):
    section: str  # "Methods", "Results", etc.
    paragraph_index: int
    char_start: Optional[int]
    char_end: Optional[int]
    quote: str  # The specific text triggering the comment

# --- TRACK A: OBJECTIVE AUDIT ---
class CriticalIssue(BaseModel):
    issue_type: str  # e.g., "missing_irb", "citation_missing", "inconsistent_n"
    severity: Literal["critical", "major"]
    description: str
    location: Optional[TextLocation]
    evidence: Optional[str]  # Supporting quote if contradiction

class TrackAReport(BaseModel):
    section: str
    study_type_detected: Optional[Literal["human", "animal", "simulation", "review", "meta-analysis"]]
    issues: List[CriticalIssue]
    passed_checks: List[str]  # e.g., ["IRB Present", "Sample Size Defined"]

# --- TRACK B: SUGGESTIVE CRITIQUE ---
class ImprovementSuggestion(BaseModel):
    category: Literal["structure", "clarity", "conciseness", "tone", "flow"]
    current_text: Optional[str]
    suggested_revision: Optional[str]
    rationale: str
    location: TextLocation

class TrackBReport(BaseModel):
    section: str
    suggestions: List[ImprovementSuggestion]
    readability_score: Optional[float]  # 0.0 to 10.0

# --- FULL REVIEW OUTPUT ---
class FullReviewOutput(BaseModel):
    document_id: str
    track_a_reports: List[TrackAReport]  # One per section + cross-document
    track_b_reports: Optional[List[TrackBReport]]  # None if Track A has critical failures
    overall_status: Literal["pass", "major_issues", "critical_issues"]
    summary: str
```

---

#### Phase 3 Tasks (Week 2, Days 8-10): Complete Agents + Track B
- [ ] **P3.1** Complete remaining Track A agents:
  - Introduction Agent
  - Discussion Agent
  - Abstract Agent
- [ ] **P3.2** Add Track B to Methods Agent (structure, detail suggestions)
- [ ] **P3.3** Add Track B to Results Agent (presentation order, visualization)
- [ ] **P3.4** Add Citation Truth Track B (controversy warnings from Scite tallies) ⭐
- [ ] **P3.5** Build result aggregation (combine all Track A/B reports)
- [ ] **P3.6** Create progress tracking UI (show which agents are running)
- [ ] **P3.7** Implement export functionality (Markdown, JSON)
- [ ] **P3.8** Add filtering (Track A only, Track A+B, by section, by severity)

#### Deliverable
Upload a paper → Full Track A + Track B review → categorized, filterable report with export

---

### Phase 4: Frontend Polish (Days 11-12)
**Goal:** Professional, usable interface

#### Tasks
- [ ] **P4.1** Design and build landing page
  - Clear value proposition
  - Example output preview
  - Upload CTA
- [ ] **P4.2** Build upload flow
  - Drag-and-drop
  - Format detection
  - Progress indicator
- [ ] **P4.3** Build results viewer
  - Left panel: document with highlights
  - Right panel: comment list
  - Click comment → jump to location
- [ ] **P4.4** Implement filtering (by category, severity)
- [ ] **P4.5** Add export options (Markdown, PDF report, JSON)
- [ ] **P4.6** Mobile responsiveness
- [ ] **P4.7** Loading states and error handling
- [ ] **P4.8** Add sample documents for demo

#### Deliverable
Polished, demo-ready interface

---

### Phase 5: Deployment & Demo (Days 13-14)
**Goal:** Live, working demo

#### Tasks
- [ ] **P5.1** Set up production infrastructure
  - Frontend: Vercel
  - Backend: Railway or Fly.io
  - Database: Supabase or Railway Postgres
  - Storage: Cloudflare R2 or S3
  - Queue: Upstash Redis
- [ ] **P5.2** Environment configuration
- [ ] **P5.3** Domain setup
- [ ] **P5.4** Rate limiting (prevent abuse)
- [ ] **P5.5** Basic analytics (PostHog or similar)
- [ ] **P5.6** Error monitoring (Sentry)
- [ ] **P5.7** Write README with:
  - Setup instructions
  - Architecture explanation
  - API documentation
- [ ] **P5.8** Create demo video/GIF
- [ ] **P5.9** Load testing
- [ ] **P5.10** Final bug fixes

#### Deliverable
Live URL + polished GitHub repo

---

## Tech Stack Summary

### Frontend
| Component | Technology | Rationale |
|-----------|------------|-----------|
| Framework | Next.js 14 (App Router) | SSR, API routes, good DX |
| Styling | Tailwind CSS | Rapid development |
| Components | shadcn/ui | Professional look, accessible |
| State | Zustand or React Query | Simple, effective |
| PDF Viewer | react-pdf | Display uploaded docs |

### Backend
| Component | Technology | Rationale |
|-----------|------------|-----------|
| Framework | FastAPI | Async, typed, fast |
| Task Queue | Celery + Redis | Reliable async processing |
| Database | PostgreSQL | Robust, good with JSON |
| Storage | S3-compatible (Minio/R2) | Standard, cheap |
| LLM | Claude API | Best for nuanced analysis |

### Document Processing
| Component | Technology | Rationale |
|-----------|------------|-----------|
| PDF Parsing | PyMuPDF (fitz) | Fast, reliable |
| DOCX Parsing | python-docx | Standard |
| LaTeX Parsing | TexSoup + regex | Good enough for structure |
| Text Chunking | Custom + tiktoken | Control over boundaries |

### DevOps
| Component | Technology | Rationale |
|-----------|------------|-----------|
| Hosting (FE) | Vercel | Easy, free tier |
| Hosting (BE) | Railway | Simple Python hosting |
| CI/CD | GitHub Actions | Standard |
| Monitoring | Sentry | Error tracking |

---

## Data Models

### Database Schema (PostgreSQL)

```sql
-- Users (simple for V0)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Documents
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    storage_path VARCHAR(500) NOT NULL,
    parsed_content JSONB,  -- structured document representation
    created_at TIMESTAMP DEFAULT NOW()
);

-- Review Jobs
CREATE TABLE review_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id),
    status VARCHAR(50) DEFAULT 'pending',  -- pending, processing, completed, failed
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT,
    agent_progress JSONB,  -- {"agent1": "complete", "agent2": "running", ...}
    created_at TIMESTAMP DEFAULT NOW()
);

-- Review Comments
CREATE TABLE review_comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID REFERENCES review_jobs(id),
    severity VARCHAR(20) NOT NULL,
    category VARCHAR(50) NOT NULL,
    excerpt TEXT NOT NULL,
    location JSONB NOT NULL,  -- {"section": "Methods", "paragraph": 3, "char_start": 150, "char_end": 200}
    explanation TEXT NOT NULL,
    suggestion TEXT,
    agent_source VARCHAR(50),  -- which agent generated this
    confidence FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_documents_user ON documents(user_id);
CREATE INDEX idx_jobs_document ON review_jobs(document_id);
CREATE INDEX idx_jobs_status ON review_jobs(status);
CREATE INDEX idx_comments_job ON review_comments(job_id);
```

### API Endpoints

```
POST   /api/upload              Upload document, returns document_id
GET    /api/documents/{id}      Get document metadata + parsed content
POST   /api/review              Start review job, returns job_id
GET    /api/jobs/{id}           Get job status + progress
GET    /api/jobs/{id}/comments  Get review comments
GET    /api/jobs/{id}/export    Export results (format=md|json|pdf)
```

---

## Agent Prompt Architecture (Track A/B)

### Base System Prompt Template

```
You are the "{SECTION_NAME} Section Specialist" for a high-impact scientific journal.
Your job is to perform a TRACK A OBJECTIVE AUDIT on the {SECTION_NAME} section.

### TRACK A: OBJECTIVE AUDIT (Zero Tolerance)
You are checking for BINARY pass/fail criteria. These are not style suggestions.
An issue is only flagged if it is objectively verifiable as an error or omission.

{SECTION_SPECIFIC_CHECKS}

### INPUT DATA
Study Title: {{title}}
{SECTION_NAME} Section Text: {{text}}
{ADDITIONAL_CONTEXT}

### OUTPUT FORMAT
Return ONLY valid JSON adhering to this schema:
{
  "section": "{SECTION_NAME}",
  "study_type_detected": "human|animal|simulation|review|meta-analysis|null",
  "issues": [
    {
      "issue_type": "string (from defined types)",
      "severity": "critical|major",
      "description": "Clear explanation of the problem",
      "location": {
        "paragraph_index": int,
        "quote": "exact text from paper"
      },
      "evidence": "supporting quote if contradiction (optional)"
    }
  ],
  "passed_checks": ["list", "of", "checks", "that", "passed"]
}

If no issues found, return empty issues array with all checks in passed_checks.
```

---

### Methods Agent (Track A) Prompt

```
You are the "Methods Section Specialist" for a high-impact scientific journal.

### TRACK A: OBJECTIVE AUDIT

**Step 1: Classify the Study Type**
First, determine: Human, Animal, In Vitro/Cell, Simulation, Review, or Meta-analysis.
This classification determines which checks apply.

**Step 2: Apply Checks Based on Study Type**

FOR HUMAN/ANIMAL STUDIES:
☐ IRB/Ethics Statement: Is there EXPLICIT mention of ethics approval, IRB, or ethics committee? 
  - Severity: CRITICAL if missing
  - Look for: "IRB", "ethics committee", "institutional review", "approved by", "consent obtained"
  
☐ Sample Size (N): Is the number of participants/subjects explicitly stated?
  - Severity: MAJOR if missing
  - Must be a specific number, not "several" or "multiple"

☐ Inclusion/Exclusion Criteria: Are selection criteria defined?
  - Severity: MAJOR if missing for clinical studies

FOR ALL EMPIRICAL STUDIES (Human, Animal, Simulation):
☐ Statistical Methods: Is there description of statistical tests used?
  - Severity: MAJOR if missing
  - Look for: t-test, ANOVA, regression, chi-square, confidence intervals, p-values

☐ Tense Consistency: Is the section in past tense (completed study)?
  - Severity: MAJOR if future tense ("will be recruited" suggests proposal, not completed study)

FOR ALL STUDIES:
☐ Reproducibility: Could another researcher replicate this?
  - Key equipment, software versions, protocols should be named
  - Severity: MAJOR for critical missing details

**Do NOT Flag (Track B issues, not Track A):**
- Passive voice (acceptable in scientific writing)
- Missing manufacturer locations (suggestion, not error)
- Suboptimal organization (suggestion, not error)

### OUTPUT
Return JSON with issues array. Each issue must cite the specific text or note "not found" for missing elements.
```

---

### Results Agent (Track A) Prompt

```
You are the "Results Section Specialist" for a high-impact scientific journal.

### TRACK A: OBJECTIVE AUDIT

**Checks:**

☐ Figure/Table References Exist:
  - Every "Figure X", "Fig. X", "Table Y" mentioned must correspond to an actual figure/table
  - Severity: CRITICAL if reference to non-existent figure/table
  - Note: You may not see the actual figures, but flag if numbering is inconsistent (e.g., Figure 3 referenced but only Figures 1, 2, 4 exist)

☐ Statistical Reporting Completeness:
  - If a claim uses words like "significant", "p < X", there must be actual statistical values
  - Severity: MAJOR if claiming significance without numbers
  - Look for: p-values, confidence intervals, effect sizes, test statistics

☐ Sample Size Consistency:
  - N reported in Results must match N stated in Methods
  - Severity: CRITICAL if numbers contradict
  - Quote both values when flagging

☐ Data-Claim Alignment:
  - Claims must be supported by data presented in the same section
  - Severity: CRITICAL if claim has no supporting data
  - Example: "Treatment was effective" with no efficacy data shown

☐ Unit Consistency:
  - Same measurements should use same units throughout
  - Severity: MAJOR if units change without explanation (e.g., kg then lbs)

**Do NOT Flag (Track B):**
- Order of presentation
- Whether data would be better as figure vs table
- Interpretation of results (belongs in Discussion)

### ADDITIONAL CONTEXT PROVIDED
- Methods section summary (for N verification)
- List of figure/table captions detected

### OUTPUT
Return JSON. For contradictions, include "evidence" field with both conflicting quotes.
```

---

### Introduction Agent (Track A) Prompt

```
You are the "Introduction Section Specialist" for a high-impact scientific journal.

### TRACK A: OBJECTIVE AUDIT

**Checks:**

☐ Citations for Prior Work Claims:
  - Any claim about previous research, known facts, or "studies have shown" MUST have citation
  - Severity: CRITICAL if factual claim about literature has no citation
  - Exception: Universally accepted facts (e.g., "DNA is a double helix")

☐ Research Question/Hypothesis Present:
  - Must explicitly state what this study aims to investigate
  - Severity: MAJOR if no clear research question by end of Introduction
  - Look for: "we hypothesized", "we aimed to", "this study investigates", "our objective"

☐ Citation-Bibliography Match:
  - Every (Author, Year) or [number] citation must exist in References/Bibliography
  - Severity: CRITICAL if citation has no corresponding reference
  - Note: You'll receive bibliography extract for cross-checking

☐ No Results Preview:
  - Introduction should not reveal specific findings
  - Severity: MAJOR if specific results numbers appear
  - Acceptable: "We found evidence for..." (vague)
  - Not acceptable: "We found a 45% reduction..." (specific)

**Do NOT Flag (Track B):**
- Flow and narrative structure
- Length of background section
- Depth of literature review

### ADDITIONAL CONTEXT PROVIDED
- List of bibliography entries

### OUTPUT
Return JSON. For missing citations, quote the unsupported claim.
```

---

### Discussion Agent (Track A) Prompt

```
You are the "Discussion Section Specialist" for a high-impact scientific journal.

### TRACK A: OBJECTIVE AUDIT

**Checks:**

☐ References Own Results:
  - Discussion must reference findings from this paper's Results section
  - Severity: CRITICAL if Discussion doesn't mention any specific results
  - Look for: references to figures, specific numbers from Results, "our findings"

☐ No New Data:
  - Discussion cannot introduce new results not presented in Results section
  - Severity: CRITICAL if new data/numbers appear
  - New statistical tests, new N values, new measurements = violation

☐ Limitations Acknowledged:
  - Must acknowledge at least one study limitation
  - Severity: MAJOR if no limitations section or acknowledgment
  - Look for: "limitation", "weakness", "future studies should", "caveat"

☐ Conclusions Supported:
  - Conclusions cannot exceed what the data shows
  - Severity: CRITICAL for causal claims without experimental support
  - Flag: "X causes Y" if study was correlational
  - Flag: Generalization beyond study population without caveat

**Do NOT Flag (Track B):**
- Speculation clearly marked as such
- Length of discussion
- Alternative interpretations not mentioned

### ADDITIONAL CONTEXT PROVIDED
- Results section summary
- Study design type from Methods

### OUTPUT
Return JSON. For unsupported conclusions, quote both the claim and the limited evidence.
```

---

### Abstract Agent (Track A) Prompt

```
You are the "Abstract Specialist" for a high-impact scientific journal.

### TRACK A: OBJECTIVE AUDIT

**Checks:**

☐ Structural Completeness:
  - Abstract must contain: Background/Purpose, Methods, Results, Conclusion
  - Severity: MAJOR if any component entirely missing
  - Note: Don't require explicit headers, but content must be present

☐ Claims Match Paper:
  - Every specific claim in abstract must appear in main text
  - Severity: CRITICAL if abstract claims something not in paper
  - Especially watch for: numbers, effect sizes, conclusions

☐ No Undefined Abbreviations:
  - First use of any abbreviation must be spelled out in abstract
  - Severity: MAJOR if abbreviation used without definition
  - Exception: Universally known (DNA, RNA, HIV)

☐ Consistency with Sections:
  - Methods described match Methods section
  - Results numbers match Results section
  - Conclusions match Discussion conclusions
  - Severity: CRITICAL for contradictions

**Do NOT Flag (Track B):**
- Writing quality
- Impact statement strength
- Word count (unless grossly over limit)

### ADDITIONAL CONTEXT PROVIDED
- Key facts extracted from each main section

### OUTPUT
Return JSON. For mismatches, quote both abstract text and paper text.
```

---

### Cross-Document Agent (Track A) Prompt

```
You are the "Consistency Specialist" for a high-impact scientific journal.
You review the ENTIRE manuscript for cross-section consistency.

### TRACK A: OBJECTIVE AUDIT

**Checks:**

☐ Notation Consistency:
  - Same mathematical symbol must mean same thing throughout
  - Severity: CRITICAL if symbol redefined or used inconsistently
  - Track: Greek letters, subscripts, variable names

☐ Number Consistency:
  - Sample sizes (N) must match across Abstract, Methods, Results
  - Percentages, means, p-values must be consistent if repeated
  - Severity: CRITICAL for any numerical contradiction

☐ Citation Integrity:
  - Every in-text citation has bibliography entry
  - Every bibliography entry is cited at least once (warning only)
  - Severity: CRITICAL for citations without entries

☐ Figure/Table Accounting:
  - All figures/tables are referenced in text
  - All references point to existing figures/tables
  - Numbering is sequential without gaps
  - Severity: CRITICAL for orphan figures or dangling references

☐ Terminology Consistency:
  - Same concept = same term throughout
  - Severity: MAJOR if terminology shifts without explanation
  - Example: "participants" in Methods, "subjects" in Results, "patients" in Discussion

**Do NOT Flag (Track B):**
- Narrative flow between sections
- Redundancy (saying same thing twice)
- Section length balance

### INPUT
You receive:
- Document section summaries
- All extracted citations
- All bibliography entries  
- All figure/table references
- Key numerical values by section

### OUTPUT
Return JSON. Always quote conflicting text from BOTH locations.
```

---

## Processing Strategy

### Section-Based Processing (Primary Approach)
With the Track A/B architecture, we process by **section** not by arbitrary chunks:

```
Document → Section Splitter → Parallel Section Agents
                                    │
                                    ├── Abstract Agent
                                    ├── Introduction Agent  
                                    ├── Methods Agent
                                    ├── Results Agent
                                    ├── Discussion Agent
                                    └── Cross-Document Agent (receives summaries from all)
```

**Why section-based is better:**
1. Each section has different rules (Methods needs IRB, Discussion needs limitations)
2. Natural semantic boundaries
3. Most sections fit in context window
4. Easier to attribute issues to document location

### Handling Large Sections
If a section exceeds 6000 tokens:
- **Methods/Results:** Split by subsections (if present) or by paragraph groups
- **Introduction/Discussion:** Split by paragraph with 1-paragraph overlap
- Run same agent on each chunk, aggregate results

### Cross-Document Agent Flow
```
Step 1: Extract from each section
  - Methods: N values, study type, key procedures
  - Results: N values, statistics, figure/table refs
  - Abstract: All claims
  - Bibliography: All entries
  
Step 2: Build consistency index
  - numbers_by_section: {"Methods": {"N": 45}, "Results": {"N": 45}}
  - citations_mentioned: ["Smith 2020", "Jones 2019"]
  - bibliography_entries: ["Smith 2020", "Jones 2019", "Brown 2018"]
  
Step 3: Run Cross-Document Agent with index
  - Detects: N mismatch, unreferenced citations, inconsistent terminology
```

### Token Budget per Section (Typical Paper)
| Section | Typical Tokens | Fits Single Call? |
|---------|---------------|-------------------|
| Abstract | 200-400 | ✓ Always |
| Introduction | 1500-3000 | ✓ Usually |
| Methods | 2000-5000 | ✓ Usually |
| Results | 2000-6000 | Sometimes needs split |
| Discussion | 2000-5000 | ✓ Usually |
| References | 1000-3000 | ✓ (extracted, not reviewed) |

---

## Deduplication Logic

With section-specialized agents, deduplication is simpler (each section has one agent).
Cross-Document Agent may catch issues also caught by section agents:

1. **Same Issue, Same Location:** Keep the more specific one (section agent)
2. **Same Issue, Cross-Section:** Keep Cross-Document version (it has both quotes)
3. **Unique Issues:** Keep all

**Deduplication Algorithm:**
```python
def deduplicate(issues: List[Issue]) -> List[Issue]:
    # Group by location (section + paragraph)
    by_location = group_by(issues, key=lambda i: (i.section, i.paragraph_index))
    
    result = []
    for location, group in by_location.items():
        if len(group) == 1:
            result.append(group[0])
        else:
            # Multiple issues at same location
            # Keep highest severity, prefer section agent over cross-doc
            best = max(group, key=lambda i: (
                severity_rank(i.severity),
                i.agent_source != "cross_document"
            ))
            result.append(best)
    
    return sorted(result, key=lambda i: severity_rank(i.severity), reverse=True)
```

---

## Cost Estimation (Revised for Section-Based)

### Per-Paper Breakdown (Typical 20-page paper)

| Agent | Input Tokens | Output Tokens | Cost (Sonnet) |
|-------|-------------|---------------|---------------|
| Abstract Agent | 500 + 2K context | 500 | $0.01 |
| Introduction Agent | 2500 + 1K context | 800 | $0.02 |
| Methods Agent | 4000 + 1K context | 1000 | $0.03 |
| Results Agent | 5000 + 2K context | 1200 | $0.04 |
| Discussion Agent | 4000 + 2K context | 1000 | $0.03 |
| Cross-Document Agent | 3K summary + 2K index | 1500 | $0.03 |
| **Total Track A** | | | **~$0.16** |

**Track B (V1):** ~$0.12 additional (simpler checks, shorter responses)

**Full Review (Track A + B):** ~$0.28 per paper

This is significantly cheaper than my original estimate because:
1. Section-specific prompts are more focused
2. Less redundant context passed to multiple agents
3. No overlap/deduplication overhead

Acceptable. Can optimize with:
- Haiku for grammar/surface checks
- Caching common patterns
- Batch processing

---

## Risk Mitigation

### Technical Risks
| Risk | Mitigation |
|------|------------|
| PDF parsing fails | Fallback to OCR (Tesseract), flag low confidence |
| Context window exceeded | Robust chunking, summarization layer |
| Agent produces invalid JSON | Retry with repair prompt, validate schema |
| Rate limits | Queue with backoff, parallel user isolation |
| Long processing times | Progress streaming, timeout handling |

### Quality Risks
| Risk | Mitigation |
|------|------------|
| False positives (flagging correct text) | Confidence scores, "dismiss" button |
| Missed issues | Clear scope communication, encourage human review |
| Domain-specific errors | Allow field specification, adjust prompts |
| Hallucinated citations | Always verify against extracted bibliography |

---

## Success Metrics

### V0 Scope: Track A Only (End of Week 1)
**The "Desk Reject Detector"** - catches fatal flaws before submission

**Functional Requirements:**
- [ ] Upload PDF → see parsed structure with sections identified
- [ ] Track A agents run on all 5 sections + cross-document
- [ ] **Figure Agent Track A: numbering, refs, caption-text consistency** ⭐
- [ ] Returns JSON with issues categorized as Critical/Major
- [ ] Frontend displays results with:
  - Pass/Fail status per section
  - Issue list with excerpts
  - **Figure Card** (dangling refs, orphaned figures)
  - Clickable navigation to issue location

**Track A Checks Implemented:**
- [ ] Methods: IRB, sample size, stats methods, tense
- [ ] Results: Figure refs, N consistency, stat reporting
- [ ] Introduction: Citations present, hypothesis stated
- [ ] Discussion: References results, no new data, limitations
- [ ] Abstract: Structure complete, claims match paper
- [ ] Cross-Document: Number consistency, citation integrity
- [ ] **Figure Agent: Sequential numbering, dangling refs, orphaned figures, caption-text match** ⭐

**Quality Targets (V0):**
- Precision: >90% (Critical issues flagged are real problems)
- False positive rate: <10% (don't cry wolf)
- Processing time: <90 seconds for typical paper

---

### V1 Scope: Track A + Track B (End of Week 2)
**The "Full Review Assistant"** - adds polish suggestions

**Additional Functional Requirements:**
- [ ] Track B agents provide improvement suggestions
- [ ] **Citation Police Agent: Lazy citation detection** ⭐⭐ KEY DIFFERENTIATOR
- [ ] **Figure Agent Track B: Caption quality, placement suggestions** ⭐
- [ ] **Figure Vision Pass (optional): Image-caption-text verification** ⭐⭐
- [ ] Filtering by Track (A only, A+B)
- [ ] Export: Markdown report, JSON, annotated PDF
- [ ] Polish: loading states, error recovery, mobile responsive
- [ ] Live deployment with rate limiting
- [ ] Sample papers for demo

**Track B Checks Implemented:**
- [ ] Structure suggestions (subheadings, organization)
- [ ] Clarity improvements (passive voice, complex sentences)
- [ ] Conciseness flags (verbose paragraphs)
- [ ] Flow suggestions (transitions, narrative arc)
- [ ] **Citation Police: Lazy citations (general claim + primary source)** ⭐⭐
- [ ] **Citation Police: Imprecise citations (specific claim + review)** ⭐⭐
- [ ] **Figure Agent: Caption quality, redundancy, visual storytelling** ⭐

**Quality Targets (V1):**
- Track A precision maintained: >90%
- Track B usefulness: >60% of suggestions deemed helpful by users
- Citation Police: Correctly identifies lazy vs appropriate citations
- Figure Agent: Catches all dangling references with 100% accuracy
- Full review time: <3 minutes
- Export formats all work correctly

---

### Demo Success Criteria
The demo is successful if:
1. **First impression:** Reviewer says "this is useful" within 30 seconds of seeing output
2. **Trust:** No obviously wrong Critical issues in sample paper review
3. **Completeness:** Catches at least one issue reviewer hadn't noticed
4. **Professional:** UI looks like a real product, not a hackathon project
5. **Differentiator:** Shows Citation Police OR Figure Agent catching something impressive

---

## Directory Structure

```
manuscript-review/
├── frontend/
│   ├── app/
│   │   ├── page.tsx                 # Landing page
│   │   ├── upload/page.tsx          # Upload flow
│   │   ├── review/[id]/page.tsx     # Results viewer
│   │   └── layout.tsx
│   ├── components/
│   │   ├── ui/                      # shadcn components
│   │   ├── DocumentViewer.tsx       # Shows paper with highlights
│   │   ├── IssuePanel.tsx           # List of issues with filters
│   │   ├── SectionStatus.tsx        # Pass/Fail indicators per section
│   │   ├── UploadDropzone.tsx       # Drag-and-drop upload
│   │   └── ProgressTracker.tsx      # Shows which agents are running
│   ├── lib/
│   │   ├── api.ts                   # API client
│   │   └── types.ts                 # TypeScript types from schemas
│   └── package.json
│
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI app
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── upload.py        # POST /upload
│   │   │   │   ├── review.py        # POST /review, GET /jobs/{id}
│   │   │   │   └── export.py        # GET /export/{id}
│   │   │   └── deps.py              # Dependencies (DB, auth)
│   │   │
│   │   ├── core/
│   │   │   ├── config.py            # Settings, env vars
│   │   │   └── database.py          # DB connection
│   │   │
│   │   ├── models/                  # SQLAlchemy models
│   │   │   ├── document.py
│   │   │   ├── job.py
│   │   │   └── issue.py
│   │   │
│   │   ├── schemas/                 # Pydantic schemas
│   │   │   ├── document.py
│   │   │   ├── review.py            # TrackAReport, TrackBReport, Issue
│   │   │   └── common.py            # TextLocation, etc.
│   │   │
│   │   ├── services/
│   │   │   ├── parser/                  # Ingestion & Parsing Layer
│   │   │   │   ├── __init__.py
│   │   │   │   ├── document_builder.py  # Orchestrates PDF → ParsedDocument
│   │   │   │   ├── pdf_parser.py        # pymupdf4llm wrapper
│   │   │   │   ├── section_splitter.py  # Regex + LLM fallback
│   │   │   │   ├── sentence_indexer.py  # Splits into indexed sentences
│   │   │   │   ├── citation_extractor.py
│   │   │   │   ├── bibliography_parser.py
│   │   │   │   └── figure_extractor.py
│   │   │   │
│   │   │   ├── indexers/                # Index Layer (pure Python, no LLM)
│   │   │   │   ├── __init__.py
│   │   │   │   ├── cross_doc_indexer.py # Ns, key numbers, term map
│   │   │   │   ├── citation_indexer.py  # Citation ↔ bib mapping
│   │   │   │   └── figure_indexer.py    # Label ↔ figure ↔ refs
│   │   │   │
│   │   │   ├── agents/                  # Agent Layer
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py              # BaseAgent + AgentContext
│   │   │   │   ├── abstract_reviewer.py
│   │   │   │   ├── introduction_reviewer.py
│   │   │   │   ├── methods_reviewer.py
│   │   │   │   ├── results_reviewer.py
│   │   │   │   ├── discussion_reviewer.py
│   │   │   │   ├── cross_doc_agent.py
│   │   │   │   ├── citation_police_agent.py
│   │   │   │   └── figure_agent.py
│   │   │   │
│   │   │   ├── external/                # External API integrations
│   │   │   │   ├── __init__.py
│   │   │   │   ├── semantic_scholar.py  # Paper metadata lookup
│   │   │   │   └── mock_semantic_scholar.py  # DEMO_MODE fallback
│   │   │   │
│   │   │   ├── orchestrator.py          # ReviewOrchestrator
│   │   │   └── aggregator.py            # Result merging & status
│   │   │
│   │   └── fixtures/                    # DEMO_MODE pre-baked results
│   │       ├── demo_paper.pdf
│   │       ├── demo_paper_hash.txt
│   │       ├── demo_citation_police.json
│   │       └── demo_full_review.json
│   │
│   ├── prompts/                         # Prompt templates (version controlled)
│   │   ├── system_base.md
│   │   ├── abstract_reviewer.md         # Track A + B combined
│   │   ├── introduction_reviewer.md
│   │   ├── methods_reviewer.md
│   │   ├── results_reviewer.md
│   │   ├── discussion_reviewer.md
│   │   ├── cross_doc_agent.md
│   │   ├── citation_police.md
│   │   └── figure_agent.md
│   │
│   ├── tests/
│   │   ├── test_parser/
│   │   │   ├── test_document_builder.py
│   │   │   ├── test_section_splitter.py
│   │   │   └── test_sentence_indexer.py
│   │   ├── test_indexers/
│   │   │   ├── test_cross_doc_indexer.py
│   │   │   ├── test_citation_indexer.py
│   │   │   └── test_figure_indexer.py
│   │   ├── test_agents/
│   │   │   ├── test_methods_reviewer.py
│   │   │   ├── test_citation_police.py
│   │   │   └── test_figure_agent.py
│   │   └── fixtures/
│   │       ├── good_paper.pdf
│   │       ├── missing_irb.pdf
│   │       ├── inconsistent_n.pdf
│   │       ├── lazy_citations.pdf
│   │       └── bad_figures.pdf
│   │
│   ├── requirements.txt
│   └── Dockerfile
│
├── docs/
│   ├── API.md
│   ├── ARCHITECTURE.md
│   └── PROMPTS.md

├── scripts/
│   ├── setup.sh
│   ├── seed_demo.py                     # Creates DEMO_MODE fixtures
│   └── evaluate_accuracy.py

├── sample_papers/
│   └── example_review.json

├── docker-compose.yml
├── README.md
└── .github/
    └── workflows/
        ├── ci.yml
        └── deploy.yml
```

---

## Next Steps

1. **Immediate:** Review this architecture, identify gaps
2. **Day 1 Morning:** Initialize repo, set up frontend/backend skeletons
3. **Day 1 Afternoon:** Get PDF upload + parsing working end-to-end
4. **Day 2:** Document intelligence layer (sections, citations)
5. **Days 3-4:** Single comprehensive agent with prompt iteration
6. **Days 5-7:** Parallel agents + orchestration
7. **Days 8-10:** Frontend polish + results viewer
8. **Days 11-12:** Deployment + documentation
9. **Days 13-14:** Testing, bug fixes, demo prep

---

## Open Questions for Discussion

1. **Authentication Scope:** Full auth system vs. anonymous uploads with rate limiting?
2. **Figure Analysis:** Worth adding vision capabilities in V1?
3. **Citation Verification:** Should we actually fetch cited papers to verify claims? (expensive but powerful)
4. **LaTeX Priority:** How important is native .tex support vs. just accepting compiled PDFs?
5. **Collaboration:** Any multi-user features needed, or single-user sufficient?
6. **Customization:** Should users be able to select which agents run, or fixed pipeline?

---

*Document Version: 1.0*  
*Last Updated: [Current Date]*  
*Status: Ready for Review*