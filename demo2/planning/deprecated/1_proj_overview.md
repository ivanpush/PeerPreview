# PeerPreview: Project Overview

## What We're Building

A generalized document-review AI system for serious knowledge work: academic manuscripts, grants, memos, legal briefs, and policy documents.

**Target user**: Researchers, policy analysts, lawyers, executives who need rigorous feedback on important documents before submission.

**Core value proposition**: Structured, non-hallucinated critique using rubric-based evaluation — not free-form AI rambling.

---

## V0 Scope

**Strategy: Skip parsing, prove the architecture.**

We bypass PDF/DOCX/LaTeX parsing by using 4 hand-curated JSON fixtures. This lets us prove the full pipeline works without getting stuck on parsing edge cases. Parsing is V1.

---

## Core Architecture

**Single source of truth**: Every document becomes a canonical `ManuscriptObject`. The system never rewrites or mutates the user's original file directly — all operations derive from this intermediate representation.

```
User selects document  →  POST /api/intake
                          (returns metadata + detected type)
User clicks Start      →  POST /api/run-review
                          (returns ManuscriptObject + Issues)
User accepts/dismisses →  POST /api/decisions
User exports           →  POST /api/export
                          (returns same-format file with revisions)
```

**Why ManuscriptObject matters:**
1. HTML viewer is NOT the truth — just an interaction layer
2. Agents need stable structure (sections → paragraphs → sentences)
3. Issues anchor to nodeIds for mapping back to source files
4. Protects user files from corruption (no direct PDF/DOCX manipulation)
5. Enables cross-section reasoning (global agents)

---

## Architecture: Backend Agents + Scopes + Personas

**Key insight**: Personas are output frames, not processing units.

The backend runs 5 core agents that produce raw analysis. An **Assembler** then reframes that into document-type-specific **scopes** and **personas** at render time.

### Backend Agents

| Agent | Purpose |
|-------|---------|
| `global_map` | Structure, claims, evidence links, argument map |
| `domain_positioning` | Field detection, related work, novelty signals |
| `rigor` | Logic, stats, methods, feasibility |
| `clarity` | Paragraph + block level readability |
| `global_hostile` | Adversarial synthesis (Heavy only) |
| `assembler` | Maps backend → scopes → personas |

### Scopes (UI-facing, vary by document type)

| Document Type | UI Scopes |
|---------------|-----------|
| Scientific Manuscript | Rigor, Clarity, Counterpoint |
| Grant Application | Significance, Innovation, Approach, Feasibility |
| Policy Brief | Evidence, Stakeholder Objections, Implementation, Clarity |
| Legal Brief | Precedent, Factual Support, Procedural, Persuasive Force |
| Generic | Consistency, Clarity, Claim Strength |

### How It Fits Together

1. Planning Agent chooses which **scopes** to run based on document type + user intent
2. Scopes map to **backend agents** via `persona_map.json`
3. Backend agents produce raw issues
4. **Assembler** maps issues to scopes, applies persona voice, merges duplicates
5. UI displays issues grouped by scope with persona labels

---

## Groundedness Rules (Anti-Hallucination)

All agents MUST follow these rules:

1. **Return zero issues if document is sound** — no manufactured criticism
2. **Acknowledge strengths** — every section assessment includes what works
3. **Never invent missing content** — only flag what's actually there
4. **Never nitpick style preferences** — only flag if it blocks comprehension
5. **Never escalate severity without evidence** — cite specific text
6. **Borderline = not a violation** — when in doubt, don't flag
7. **Heavy depth can return zero issues** — strong docs exist

---

## Issue Codes

Each backend agent produces issues with agent-specific codes:

| Agent | Code Prefix | Examples |
|-------|-------------|----------|
| global_map | `MAP_` | `MAP_CLAIM_UNSUPPORTED`, `MAP_CROSS_SECTION_CONFLICT` |
| rigor | `RIGOR_` | `RIGOR_LOGIC_GAP`, `RIGOR_STATS_MISUSE`, `RIGOR_METHOD_MISSING` |
| clarity | `CLARITY_` | `CLARITY_AMBIGUOUS`, `CLARITY_UNDEFINED_TERM`, `CLARITY_FLOW_BROKEN` |
| domain_positioning | `DOMAIN_` | `DOMAIN_NOVELTY_OVERCLAIM`, `DOMAIN_RELATED_WORK_GAP` |
| global_hostile | `HOSTILE_` | `HOSTILE_FATAL_FLAW`, `HOSTILE_ALTERNATIVE_EXPLANATION` |

The Assembler maps these to UI scopes and applies persona voice.

---

## Depth System

Depth = reasoning thoroughness, NOT number of issues.

| Aspect | Light | Standard | Heavy |
|--------|-------|----------|-------|
| **Global Map** | Basic | Full | Deep analysis |
| **Domain Positioning** | — | If scope needs | Always |
| **Rigor Agent** | Light pass | Full pass | Deep pass |
| **Clarity Agent** | ✓ | ✓ | ✓ |
| **Global Hostile** | — | — | ✓ |
| **Assembler Tone** | Supportive | Balanced | Adversarial |
| **Rewrites** | None | Paragraph-level | Multi-paragraph |
| **Cost** | ~$0.30-0.50 | ~$0.80-1.50 | ~$2.00-4.00 |

---

## Document Types Supported

| Type | Key Signals | Section Mapping |
|------|-------------|-----------------|
| `academic_manuscript` | Abstract, Introduction, Methods, Results, Discussion, References | IMRAD roles |
| `grant_proposal` | Specific Aims, Significance, Innovation, Approach | Aims/Significance/Approach |
| `legal_brief` | Statement of Facts, Issues Presented, Argument, Conclusion | Facts/Issue/Argument/Conclusion |
| `policy_brief` | Executive Summary, Background, Policy Options, Recommendations | Summary/Background/Options/Recommendations |
| `memo` | To/From/Date/Re headers; Background, Analysis, Recommendation | Header/Body/Recommendation |
| `technical_report` | Background, Problem, Proposal, Roadmap | Heading hierarchy |
| `generic_knowledge_doc` | Catchall | Heading hierarchy only |

---

## Page Limits

| Document Length | Behavior |
|-----------------|----------|
| ≤15 pages | Full review at any depth |
| 16-40 pages | Full review; cost warning for Heavy |
| 41-60 pages | Light/Medium only; Heavy requires section selection |
| >60 pages | **Blocked** — must truncate or select sections |

---

## User Intent Dominance

User prompt guides the majority of reviewer effort, but dynamically reweights if:
- User has little to say → default to standard review
- Document is exceptionally strong → acknowledge and reduce issue count
- User focus areas are irrelevant to a track → track uses rubric defaults

Planning Agent extracts: focus sections, tone, emphasis, priorities, constraints.

---

## Export Strategy: Same Format Out

We ALWAYS return the same format the user uploaded, with revisions in the native format.

| Input | Output | How Revisions Appear |
|-------|--------|----------------------|
| PDF | PDF | Sticky note annotations |
| DOCX | DOCX | Track changes OR revised doc + change log |
| LaTeX | .tex | `% REVIEW:` comments + rewritten sections |

---

## V0 Fixtures

4 hand-curated JSON files: academic manuscript (PDF), grant (DOCX), policy memo (PDF), arXiv paper (LaTeX).

---

## System Rules (Non-Negotiable)

1. **ManuscriptObject is the single source of truth** — HTML is interaction view only
2. **Export always matches original format** — PDF→PDF, DOCX→DOCX, LaTeX→LaTeX
3. **Backend agents produce raw issues, Assembler maps to scopes/personas**
4. **Agents must acknowledge strengths** — and can return zero issues
5. **Depth controls reasoning intensity, not issue quantity**
6. **Accepting a rewrite auto-conflicts overlapping issues** — mutual exclusion
7. **Backend agents are reusable** — scopes vary by document type
8. **Persona voice is applied by Assembler** — not baked into agents
9. **Docs >60 pages must be blocked or reduced**
10. **Demo dropdown is temporary** — real upload replaces it in V1

---

## Page Structure

Only 2 pages + 1 modal:

| Route | Component | Purpose |
|-------|-----------|---------|
| `/` | UploadPage | Doc selector, depth, prompt chips, Start Review |
| `/review/:sessionId` | ReviewScreen | 3-pane viewer with issues, Accept/Dismiss |
| (modal) | ExportModal | Format summary, Generate & Download |

No separate progress page — ReviewScreen shows spinner until data loads.

---

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/intake` | Returns metadata + detected type |
| POST | `/api/run-review` | Returns ManuscriptObject + Issues[] |
| POST | `/api/decisions` | Save Accept/Dismiss decisions |
| POST | `/api/export` | Returns same-format file with revisions |

---

## Tech Stack

| Task | Tool |
|------|------|
| Backend | Python (FastAPI) |
| Frontend | React + TypeScript |
| LLM | Claude API (Sonnet for agents, Haiku for classification) |
| PDF annotation | PyMuPDF |
| DOCX generation | python-docx |
| Sentence segmentation | pysbd |
| Diff visualization | diff-match-patch |

---

## Success Criteria

- [ ] Load fixtures via demo dropdown
- [ ] Type detection with override → persona_schema selection
- [ ] Scope selection UI (document-type-specific)
- [ ] Depth slider with cost estimate
- [ ] Planning Agent → ReviewPlan with scopes_to_run + tracks_to_run
- [ ] Global Map Agent → GlobalMap (claims, evidence, structure)
- [ ] Rigor + Clarity agents → raw issues
- [ ] Global Hostile Agent (Heavy only)
- [ ] Assembler → final issues with scope + persona_label + persona_summaries
- [ ] ReviewScreen with issues grouped by scope
- [ ] Accept/Dismiss with conflict handling
- [ ] Export stubs (PDF annotations, DOCX change log, LaTeX comments)