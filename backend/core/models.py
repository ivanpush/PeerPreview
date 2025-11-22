"""Core data models for manuscript review system."""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal
from enum import Enum
from datetime import datetime
import hashlib


# ============== Enums ==============

class Severity(str, Enum):
    """Issue severity levels."""
    CRITICAL = "critical"      # Would cause desk rejection
    MAJOR = "major"            # Significant problem
    MINOR = "minor"            # Should fix but not fatal
    SUGGESTION = "suggestion"  # Optional improvement


class OverallStatus(str, Enum):
    """Overall manuscript review status."""
    PASS = "pass"
    MAJOR_ISSUES = "major_issues"
    CRITICAL_ISSUES = "critical_issues"


# ============== Document Structure Models ==============

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
    image_path: Optional[str] = None  # For future vision pass
    image_bytes: Optional[bytes] = None


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
    doi: Optional[str] = None
    is_review_paper: Optional[bool] = None  # From Semantic Scholar or mock


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


# ============== Issue & Report Models ==============

class TextLocation(BaseModel):
    """Where an issue was found - NO LINE NUMBERS (avoids hallucinations)."""
    section: str
    sentence_id: Optional[str] = None
    paragraph_index: Optional[int] = None
    quote: str                 # Exact excerpt for fuzzy matching


class Issue(BaseModel):
    """A single issue found by an agent."""
    issue_type: str            # See ISSUE_TYPES mapping
    severity: Severity
    description: str
    location: TextLocation
    evidence: Optional[str] = None    # Supporting quotes/data
    suggestion: Optional[str] = None  # How to fix (for Track B)
    guideline_violation: bool = False  # Flag for journal/reporting guideline issues


class SectionReviewReport(BaseModel):
    """Output from a section reviewer (contains both tracks)."""
    section: str
    track_a_issues: List[Issue]
    track_b_suggestions: List[Issue]
    passed_checks: List[str]
    summary: Optional[str] = None


class CrossDocReport(BaseModel):
    """Output from CrossDocConsistency agent."""
    issues: List[Issue]
    consistency_score: float   # 0-1
    ns_found: Dict[str, List[int]]  # Section → N values found


class CitationPoliceIssue(BaseModel):
    """Individual citation analysis result."""
    citation_id: str
    claim_text: str
    claim_type: Literal["general", "specific"]
    cited_paper_type: Literal["review", "primary"]
    verdict: Literal["pass", "flag"]
    issue_type: Optional[Literal["lazy_citation", "imprecise_citation", "content_mismatch"]] = None
    explanation: Optional[str] = None
    suggestion: Optional[str] = None


class CitationPoliceReport(BaseModel):
    """Output from CitationPolice agent."""
    total_citations: int
    lazy_citations: List[Issue]
    imprecise_citations: List[Issue]
    appropriate_citations: int
    detailed_analysis: Optional[List[CitationPoliceIssue]] = None


class FigureReport(BaseModel):
    """Output from FigureAgent."""
    total_figures: int
    track_a_issues: List[Issue]
    track_b_suggestions: List[Issue]
    passed_checks: List[str]


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

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    model_versions: Dict[str, str] = {}  # Track which LLM was used for each agent


# ============== Index Models ==============

class CrossDocIndex(BaseModel):
    """Pre-computed cross-document lookups."""
    ns_by_section: Dict[str, List[int]]           # {"methods": [150, 75], "results": [150]}
    key_numbers: Dict[str, List[float]]           # {"p_values": [0.05, 0.01], "means": [3.5, 4.2]}
    term_to_sentence_ids: Dict[str, List[str]]    # {"ANOVA": ["methods-s5", "results-s12"]}
    notation_map: Dict[str, str]                  # {"α": "significance level", "N": "sample size"}


class CitationIndex(BaseModel):
    """Pre-computed citation lookups."""
    citation_to_bib: Dict[str, BibliographyEntry]      # "[3]" → BibEntry
    bib_to_citations: Dict[str, List[CitationRef]]     # "smith2020" → [CitationRef, ...]
    unmatched_citations: List[str]                      # Citations with no bib entry
    unmatched_bib_entries: List[str]                    # Bib entries never cited


class FigureIndex(BaseModel):
    """Pre-computed figure lookups."""
    label_to_figure: Dict[str, FigureBlock]        # "Figure 1" → FigureBlock
    label_to_refs: Dict[str, List[FigureRef]]      # "Figure 1" → [ref1, ref2, ...]
    dangling_refs: List[FigureRef]                  # Refs to non-existent figures
    orphaned_figures: List[FigureBlock]             # Figures never referenced


class AgentContext(BaseModel):
    """Everything an agent needs to do its job."""
    doc: ParsedDocument
    cross: CrossDocIndex
    citations: CitationIndex
    figures: FigureIndex

    class Config:
        arbitrary_types_allowed = True


# ============== Semantic Scholar Models ==============

class PaperMetadata(BaseModel):
    """Paper metadata from Semantic Scholar or mock."""
    doi: str
    title: str
    abstract: Optional[str] = None
    publication_types: List[str] = []  # e.g., ["Review", "JournalArticle"]
    is_review_paper: bool = False
    citation_count: Optional[int] = None


# ============== Standard Issue Types ==============

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


# ============== Helper Functions ==============

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


def flag_guideline_violations(issues: List[Issue]) -> List[Issue]:
    """Auto-flag known guideline issue types."""
    for issue in issues:
        if issue.issue_type in GUIDELINE_ISSUE_TYPES:
            issue.guideline_violation = True
    return issues