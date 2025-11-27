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

## Three Review Axes (Tracks)

Every review runs up to three independent tracks. They have **strict separation** — no overlap in responsibilities.

| Track | Name | What It Checks |
|-------|------|----------------|
| A | **Rigor** | Correctness, logic, evidence, methodology, cross-section alignment |
| B | **Clarity** | Writing structure, readability, terminology, flow |
| C | **Skeptic** | Overclaiming, hidden assumptions, missing limitations, unbalanced framing |

---

## The Rubric System (Critical)

To prevent hallucinations and over-criticism, all reviewers use a **hard, deterministic rubric**. Agents can ONLY flag violations from this list.

### Track A — Rigor Violations
| Code | Violation | Description |
|------|-----------|-------------|
| A1 | Claim-evidence mismatch | Conclusion not supported by presented evidence |
| A2 | Internal contradiction | Statements conflict with each other |
| A3 | Non-sequitur | Conclusion does not follow from premises |
| A4 | Missing methodological detail | Essential info omitted |
| A5 | Statistical misinterpretation | Incorrect use/interpretation of stats |
| A6 | Cross-section disagreement | Abstract/results/discussion inconsistent |

### Track B — Clarity Violations
| Code | Violation | Description |
|------|-----------|-------------|
| B1 | Ambiguity blocking meaning | Reader cannot determine intent |
| B2 | Cohesion broken | Logical flow disrupted between sentences/paragraphs |
| B3 | Undefined critical term | Jargon or term used without definition |
| B4 | Style undermining professionalism | Tone/register inappropriate for audience |

### Track C — Skeptic Violations
| Code | Violation | Description |
|------|-----------|-------------|
| C1 | Overclaiming | Conclusions exceed what evidence supports |
| C2 | Hidden assumption | Premise taken as given without justification |
| C3 | Missing limitation | Obvious weakness not acknowledged |
| C4 | Unbalanced framing | Alternative explanations ignored |

**Rules:**
- Only violations may be flagged
- Borderline cases = NOT violations
- Agents are allowed (and required) to say a section is "good"
- No code = not a valid issue

---

## Groundedness Rules (Anti-Hallucination)

All agents MUST follow these rules:

1. Return zero issues if nothing violates rubric
2. Acknowledge strengths when present
3. Never invent missing content
4. Never nitpick style preferences (only flag B4 if unprofessional/unclear)
5. Never escalate severity without evidence
6. Justify each critique with exact sentence references
7. Use "suggestion" for mild improvements only
8. Heavy depth can still return "no issues" if document is strong

---

## Depth System

Depth = reasoning thoroughness, NOT number of issues.

| Aspect | Light | Medium | Heavy |
|--------|-------|--------|-------|
| **Tracks** | Clarity only + minimal Rigor | All three tracks | All three tracks |
| **Track C tone** | Skipped (or C1 only) | Fair/balanced ("careful reader") | Adversarial ("hostile Reviewer 2") |
| **Scope** | Per-sentence/paragraph | Paragraph + limited section | Line-level + section-level |
| **Rewrites** | None | Paragraph-level | Multi-paragraph, section-level |
| **Global agents** | None | Limited cross-doc check | Full consistency + overclaiming |
| **Model** | Small/fast | Mid-size | Largest |
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
3. **Issues must use rubric codes** — only A1-A6, B1-B4, C1-C4 are valid
4. **Reviewers must acknowledge strengths** — and can return zero issues
5. **Depth controls reasoning intensity, not issue quantity**
6. **Accepting a rewrite auto-conflicts overlapping issues** — mutual exclusion
7. **Track A ≠ Track C** — correctness ≠ skepticism, no overlap
8. **Track B never touches logic or tone** — only clarity/structure
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
- [ ] Type detection with override
- [ ] Depth slider with cost estimate
- [ ] Planning Agent → ReviewPlan
- [ ] All 3 track agents → Issues with rubric codes
- [ ] ReviewScreen with highlights + Accept/Dismiss
- [ ] Conflict handling (mutual exclusion)
- [ ] Export stubs (PDF annotations, DOCX change log, LaTeX comments)