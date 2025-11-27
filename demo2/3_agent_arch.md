PeerPreview: Agent Architecture & Pipeline (Final Version)
Overview

PeerPreview performs deep, structured analysis of long-form knowledge-work documents (manuscripts, policy briefs, grants, memos, up to ~30 pages).

The pipeline has three phases:

Phase 1 — Global Understanding

Planning Agent

Global Map Agent (claims, terminology, section map, early hostile sketch)

Phase 2 — Local Reviews (parallel)

Rigor Agent (Track A) — section-level

Clarity Agents (Track B)
• B1 = per paragraph
• B2 = multi-paragraph flow

(Track C does NOT run here!)

Phase 3 — Global Reasoning (Heavy only)

Global Consistency & Hostile Synthesis Agent (Track C final)

Flow Diagram
documentObject + UserIntent
            │
            ▼
      Planning Agent
            │
            ▼
   Phase 1: Global Map Agent
   (Claim Map, Term Map, Section Map,
    Early Hostile Sketch)
            │
            ▼
   Phase 2: Local Track Agents (parallel)
   ├── Track A (Rigor, per-section)
   ├── Track B1 (Clarity, per-paragraph)
   └── Track B2 (Clarity, multi-paragraph blocks)
            │
            ▼
        Aggregator
            │
            ▼
   Phase 3: (Heavy only)
   Global Consistency + Final Hostile Review
            │
            ▼
        Final Issue[]

Data Models (Finalized)
documentObject
@dataclass
class documentObject:
    document_type: DocumentType          # 'manuscript', 'grant', 'policy_brief', etc.
    source_format: Literal['pdf', 'docx', 'latex']
    title: str
    sections: list['Section']
    meta: 'DocumentMetadata'

@dataclass
class Section:
    id: str
    heading: str
    role: SectionRole                    # e.g. 'intro', 'methods', 'discussion'
    paragraphs: list['Paragraph']

@dataclass
class Paragraph:
    id: str
    sentences: list['Sentence']
    page: int | None
    bbox: tuple | None

@dataclass
class Sentence:
    id: str
    text: str

@dataclass
class DocumentMetadata:
    filename: str
    page_count: int
    word_count: int
    section_names: list[str]

UserIntent
@dataclass
class UserIntent:
    depth: Literal['light', 'standard', 'heavy']
    prompt: str
    chips_selected: list[str]

ReviewPlan
@dataclass
class ReviewPlan:
    document_type: DocumentType
    depth: Literal['light', 'standard', 'heavy']

    # Which tracks run under user intent + depth
    tracks_to_run: list[Literal['rigor', 'clarity']]

    # C-track is global-only and depth controlled
    run_global_hostile: bool

    # Section prioritization
    section_priorities: list[str]
    sections_to_skip: list[str]

    # User intent
    user_focus_summary: str
    user_constraints: list[str]

    # Tone for critic or supportive reviews
    tone: Literal['supportive', 'balanced', 'adversarial']

    # Cost and token governance
    max_tokens_per_call: int
    total_budget_tokens: int
    concurrency_limit: int

Issue Model
@dataclass
class Issue:
    id: str
    track: Literal['rigor', 'clarity', 'skeptic']
    code: str
    severity: Literal['major', 'moderate', 'minor']
    location: 'IssueLocation'
    rationale: str
    suggestion: str | None
    proposed_rewrite: str | None
    conflicting_issue_ids: list[str]

@dataclass
class IssueLocation:
    section_id: str
    paragraph_id: str
    sentence_ids: list[str] | None
    char_range: tuple[int, int] | None

Phase 1 — Global Understanding
1. Planning Agent

Takes documentObject + UserIntent and produces a ReviewPlan:

which tracks run

the tone

cost cap

concurrency limits

which sections get priority

which are skipped

user constraints

This is a light LLM + logic step.

2. Global Map Agent (Mandatory)

This agent ingests the entire document and outputs:

Claim Map (what claims are made, where)

Terminology Map (acronyms, definitions)

Section Map (high-level summary of each section)

Argument Structure / Narrative Map

Early Hostile Sketch (Track C v0, used later in synthesis)

Output
{
  "claims": [...],
  "acronyms": {...},
  "section_summaries": {...},
  "argument_map": {...},
  "hostile_sketch": {...}
}


This grounding is essential for high-accuracy section-level reviews.

Phase 2 — Local Reviews (Parallel Track Agents)
All Phase 2 agents run in parallel under concurrency caps, e.g.:

5 parallel jobs on Light

10 on Standard

15 on Heavy

Track A — Rigor (Section-Level)

Reviews each section:

claim–evidence mismatch

contradictions

statistical issues

missing methodological detail

internal logic flaws

Uses global maps from Phase 1.

Track B1 — Clarity (Paragraph-Level)

For each paragraph:

ambiguity

cohesion

undefined terms

tone issues

rewrites suitable for diff

This produces most of the user-facing rewrites.

Track B2 — Multi-Paragraph Clarity (Flow-Level)

For selected 2–6 paragraph blocks per section:

transitions

redundancy

narrative flow

merge/split suggestions

optional rewritten block

This captures coherence that single paragraphs can’t.

❗ Track C does not run in Phase 2

Track C = global reasoning only
Not section-level.

Phase 3 — Global Consistency & Hostile Synthesis (Heavy Only)

Uses:

The full document

Global maps

All issues found in Phase 2

The early hostile sketch

Produces:

Final Hostile Review (Track C)

Cross-section consistency checks

Prioritized flaw list

Meta-analysis (“what really matters”)

This is the “Reviewer #2” output.

Aggregator

After Phase 2:

Combine issues

Deduplicate

Detect rewrite conflicts

Sort by severity + location

Final issues passed to Phase 3.

Execution Flow (Final Code Structure)
async def run_review(manuscript, user_intent):
    
    # Phase 1: Planning + Global Map
    doc_summary = await summarize_document(manuscript)
    plan = await plan_review(manuscript, user_intent, doc_summary)
    global_map = await global_map_agent(manuscript, plan)

    # Phase 2: Local Tracks (parallel)
    track_a_task = run_rigor(manuscript, plan, global_map)
    track_b1_task = run_clarity_paragraphs(manuscript, plan)
    track_b2_task = run_clarity_blocks(manuscript, plan)

    a_issues, b1_issues, b2_issues = await asyncio.gather(
        track_a_task, track_b1_task, track_b2_task
    )

    all_issues = aggregate(a_issues + b1_issues + b2_issues)

    # Phase 3: Global Reasoning (Heavy only)
    if plan.run_global_hostile:
        hostile_issues = await global_hostile_agent(
            manuscript, plan, global_map, all_issues
        )
        all_issues.extend(hostile_issues)

    return ReviewResult(
        plan=plan,
        issues=all_issues,
        global_map=global_map,
        doc_summary=doc_summary
    )

LLM Model Selection by Depth
Depth	Models	Tracks
Light	Haiku	B1 only
Standard	Sonnet	A + B1 + B2 + global map
Heavy	Sonnet (locals) + Opus (global)	A + B1 + B2 + full C
Cost & Concurrency Governance
Slider determines:

which tracks run

which model tier

how many blocks to include in B2

concurrency limits

token caps

Examples:

Light:

~3k–6k total tokens

clarity only

minimal flow checks

Haiku for everything

Standard:

~15k–30k tokens

A + B1 + B2 (auto selection)

Sonnet everywhere

Heavy:

~40k–80k tokens

All tracks

B2 aggressively

Opus for global passes

All governed by:

if estimated_cost > plan.total_budget_tokens:
    prune_B2_blocks()
    downgrade_models()
    reduce_tracks()

Final File Structure
/backend/
├── agents/
│   ├── planning_agent.py
│   ├── global_map_agent.py
│   ├── rigor_agent.py
│   ├── clarity_agent.py
│   │   ├── clarity_paragraphs.py
│   │   └── clarity_blocks.py
│   ├── global_hostile_agent.py
│   └── aggregator.py
├── core/
│   ├── models.py
│   ├── llm_client.py
│   └── config.py
├── pipeline/
│   └── orchestrator.py
└── examples/