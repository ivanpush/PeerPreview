# 01: Project Overview

## What We're Building

**PeerPreview** — AI-powered document review that surfaces issues and suggests fixes before human reviewers see your work.

**Not an editor.** We return issue cards with suggested rewrites. Users apply changes in their own tools.

**Not a chatbot.** Deterministic pipeline that produces structured output. No conversation, no hedging.

---

## Core Architecture

```
                         [User Uploads Document]
                                  │
                                  ▼
                    ┌─────────────────────────────┐
                    │  Doc Type Detection         │
                    │  (auto-detect or override)  │
                    └─────────────────────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────────┐
                    │  User Input                 │
                    │  • Tier (Quick/Std/Deep)    │
                    │  • Chips (focus areas)      │
                    │  • Free text concerns       │
                    └─────────────────────────────┘
                                  │
                                  ▼
                              [Parser]
                                  │
                                  ▼
                            Indexed JSON
                                  │
                  ┌───────────────┴───────────────┐
                  │                               │
                  ▼                               ▼
            [Extractor]                      [Clarity]
                  │                           (streams)
                  ▼                               │
    ArgumentMap + ReviewPlan                      │
                  │                               │
         [Prompt Selector]                        │
                  │                               │
          ┌───────┴───────┐                       │
          ▼               ▼                       │
      [Domain]        [Rigor]                     │
     (external)      (internal)                   │
          │               │                       │
          ▼               ▼                       │
    DomainReport    Rigor Issues                  │
          │               │                       │
          └───────┬───────┘                       │
                  ▼                               │
            [Adversary]                           │
         (receives both)                          │
                  │                               │
                  └───────────┬───────────────────┘
                              ▼
                         [Assembler]
                              │
                              ▼
               Issue Cards + Rubric
                              │
                              ▼
                       ┌──────────────┐
                       │      UI      │
                       │   (Review)   │
                       └──────────────┘
                              │
            User actions: accept/dismiss/edit
                              │
                              ▼
                         [ChangeLog]
                              │
                              ▼
                       ┌──────────────┐
                       │   [Export]   │
                       │              │
                       │ Original doc │
                       │ + ChangeLog  │
                       │      ↓       │
                       │ Format-aware │
                       │   rebuild    │
                       └──────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
      DOCX w/            PDF w/           LaTeX w/
    Track Changes      Annotations      Comment Blocks
```

**Input handling:**
- Doc type auto-detected, user can override
- User selects tier, chips, free text concerns
- All fed to Parser and downstream agents

**Pipeline flow (V0):**
- **Extractor** reads full doc → produces ArgumentMap + ReviewPlan
- **Clarity** begins streaming immediately using base prompt. Incorporates ArgumentMap slices once Extractor completes.
- **Prompt Selector** receives `doc_type`, `tier`, `chips`, `map_characteristics`, and `track_emphasis`. Picks prompt variants deterministically. At Quick tier, Adversary is skipped and Prompt Selector returns `None` for adversary_prompt.
- **Domain** ‖ **Rigor** run in parallel:
  - Domain: RAG queries → DomainReport (external context, positioning)
  - Rigor: ArgumentMap + text lookups → Rigor Issues (internal consistency)
- **Adversary** waits for both → receives ArgumentMap + DomainReport + Rigor issues as signals only (not for rewrite generation)
- **Assembler** merges all cards → applies voice, dedupes, scores. Assembler logic is deterministic; `assembler_consensus.md` is used only for the inner consensus-resolution step, not general assembly.

**V1 change:** When citation verification added, Rigor will receive DomainReport.

**Output handling:**
- UI captures user decisions in ChangeLog
- Export rebuilds original format with changes + annotations

### Consensus Mode (Deep + Toggle)

```
                    ┌─────────────────────────────┐
                    │  User Input                 │
                    │  • Tier: Deep               │
                    │  • Consensus: ✓ enabled     │
                    │  • Chips, free text         │
                    └─────────────────────────────┘
                                  │
                                  ▼
                            Indexed JSON
                                  │
          ┌───────────────────────┴───────────────────────┐
          │                                               │
          ▼                                               ▼
    [Extractor]                                      [Clarity]
    (run once)                                       (run once)
          │                                               │
          ▼                                               │
ArgumentMap + ReviewPlan                                  │
          │                                               │
 [Prompt Selector]                                        │
          │                                               │
          ▼                                               │
     [Domain]                                             │
    (run once)                                            │
          │                                               │
          ▼                                               │
    DomainReport                                          │
          │                                               │
          ├─────────────────┬─────────────────┐           │
          ▼                 ▼                 ▼           │
      [Claude]           [GPT]           [Gemini]         │
          │                 │                 │           │
          ▼                 ▼                 ▼           │
       Rigor             Rigor             Rigor          │
          │                 │                 │           │
          ▼                 ▼                 ▼           │
      Adversary         Adversary         Adversary       │
          │                 │                 │           │
          └────────┬────────┴────────┬────────┘           │
                   ▼                 ▼                    │
          [Consensus Clustering]                          │
                   │                                      │
                   └──────────────────┬───────────────────┘
                                      ▼
                                 [Assembler]
                                      │
                                      ▼
                     Issue Cards + Confidence + Dispute Markers
                                      │
                                      ▼
                                 [Export]
```

**Shared (run once):** Extractor, Prompt Selector, Domain, Clarity
**Per-model (3×):** Rigor + Adversary only — different reasoning, same evidence base
**Aggregation:** Consensus runs ONLY on Rigor + Adversary outputs. Detects agreement/disagreement on interpretation, not facts.

---

## Document Types

| Type | Example | Persona Flavor |
|------|---------|----------------|
| Scientific Manuscript | Journal paper | Reviewer 2 |
| Grant Proposal | NIH R01, NSF | Study section panelist |
| Policy Brief | Government memo | Political opposition |
| Legal Brief | Court filing | Opposing counsel |
| Generic | Any document | Skeptical reader |

---

## Three Tiers

| Tier | Cost | What Runs | Use Case |
|------|------|-----------|----------|
| **Quick** | $0.25–1 | Clarity + light Rigor | Drafts, informal sharing |
| **Standard** | $0.50–2.50 | Full pipeline | Pre-submission review |
| **Deep** | $1–4 | Full + Adversary + tools | High-stakes submissions |

**Add-on:** Consensus (+$2–6) — 3 models, disagreement flagging. Deep tier only.

---

## Three UI Tabs

| Tab | What It Shows | Agents |
|-----|---------------|--------|
| **CLARITY** | Readability, grammar, flow | Clarity |
| **RIGOR** | Errors, inconsistencies, logic gaps | Rigor |
| **FIELD** | Expert critiques, positioning, attack vectors | Domain, Adversary |

**Domain routing:**
- V0: All Domain cards → FIELD (positioning, novelty, field context)
- V1: Domain splits — citation issues → RIGOR, positioning → FIELD

Tabs are fixed. Personas vary by document type (voice, not UI chrome).

---

## Agent Roster

| Agent | Role | Reads |
|-------|------|-------|
| **Extractor** | Build ArgumentMap + ReviewPlan | Full doc (once) |
| **Clarity** | Prose quality (sentence + block) | Full doc |
| **Rigor** | Internal consistency | Map + lookups |
| **Domain** | External positioning, citations | Map + RAG |
| **Adversary** | Hostile review, attack vectors | Map + Rigor + Domain |
| **Assembler** | Merge, dedupe, voice, render | All cards |

Plus: **Prompt Selector** (deterministic, not LLM)

---

## Issue Card Structure

```json
{
  "id": "R-7",
  "tab": "RIGOR",
  "title": "Overstated effect size",
  "message": "Claim says 20% but data shows 15%",
  "severity": "major",
  "locations": [{"section_id": "...", "sentence_ids": [...]}],
  "original_text": "We found a 20% improvement...",
  "suggested_rewrite": "We found a 15% improvement...",
  "rationale": "Table 1 shows 15% average"
}
```

---

## V0 Scope

**Strategy:** Skip parsing, prove the architecture.

- Use hand-curated JSON fixtures (4 documents)
- Build full pipeline: Extractor → Agents → Assembler → UI
- Prove the architecture works before tackling parsing edge cases

**Parsing is V1.**

---

## Tech Stack

- **Backend:** Python, FastAPI
- **LLM:** Claude family (Haiku/Sonnet/Opus varies by agent and tier)
- **Consensus:** Claude + GPT + Gemini (Deep tier add-on)
- **RAG:** Perplexity API
- **Frontend:** React, Tailwind
- **Storage:** Indexed JSON (sentence-level IDs)

---

## Export Strategy

### Ground Truth

**ManuscriptObject (Indexed JSON) is the single source of truth.**

The HTML view is for interaction only. All user actions (accept rewrite, edit text, dismiss issue, add comment) are logged to a ChangeLog. Export rebuilds the document from ManuscriptObject + ChangeLog.

### ChangeLog Structure

```json
{
  "changes": [
    {
      "id": "ch-001",
      "type": "rewrite_accepted",
      "issue_id": "R-7",
      "sentence_ids": ["s_res_3_2"],
      "original_text": "We found a 20% improvement...",
      "new_text": "We found a 15% improvement...",
      "timestamp": "2025-01-15T10:30:00Z"
    },
    {
      "id": "ch-002",
      "type": "manual_edit",
      "sentence_ids": ["s_met_2_1"],
      "original_text": "...",
      "new_text": "...",
      "timestamp": "..."
    },
    {
      "id": "ch-003",
      "type": "issue_dismissed",
      "issue_id": "C-3",
      "reason": "user_dismissed",
      "timestamp": "..."
    }
  ]
}
```

### Export Modes

**Option A: Rebuild from Ground Truth**
- Apply ChangeLog to ManuscriptObject
- Regenerate document in original format
- Clean output, no revision history visible

**Option B: Annotated Original (Preferred)**
- Modify the *original uploaded file*
- Preserve formatting, styles, references
- Add visible change tracking

### Format-Specific Export

| Format | Export Strategy |
|--------|-----------------|
| **DOCX** | Track Changes mode — insertions/deletions visible, linked comments for issues |
| **PDF** | Sticky note annotations linked to issue cards, highlighted regions |
| **LaTeX** | `\added{}` / `\deleted{}` macros + `% PEERPREVIEW:` comment blocks |
| **Markdown** | Inline HTML comments or diff-style markers |

### DOCX Export Detail

```
Original: "We found a 20% improvement in all conditions."
                    ↓
Export:   "We found a [15%]{tracked insertion} [20%]{tracked deletion} improvement in [most]{insertion} [all]{deletion} conditions."

+ Linked comment: "[R-7] Overstated effect size. Table 1 shows 15%. Rewrite accepted."
```

### PDF Export Detail

```
┌─────────────────────────────────────────────────────────────┐
│ We found a 15% improvement in most conditions tested.       │
│                    ▲                                        │
│                    │                                        │
│         [Highlighted region]                                │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ 📌 R-7: Overstated effect size                          │ │
│ │ Original: "20% improvement in all conditions"           │ │
│ │ Status: Rewrite accepted                                │ │
│ │ Tab: RIGOR | Severity: Major                            │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Comment/Annotation Content

Each exported annotation includes:
- Issue ID and title
- Tab (CLARITY / RIGOR / FIELD)
- Severity
- Original text (if changed)
- Status: `Accepted` | `Dismissed` | `Manual edit` | `Unresolved`
- User notes (if any)

### Export Flow

```
User clicks "Export"
        │
        ▼
┌───────────────────────────────────────────────────────────┐
│ Export Modal                                              │
│                                                           │
│ Format: [Original (DOCX) ▼]                               │
│                                                           │
│ Include:                                                  │
│ ☑ Track changes for accepted rewrites                     │
│ ☑ Comments for unresolved issues                          │
│ ☐ Comments for dismissed issues                           │
│ ☑ Highlight edited regions                                │
│                                                           │
│ [Export Clean Copy]  [Export with Annotations]            │
└───────────────────────────────────────────────────────────┘
        │
        ▼
Load original file + ManuscriptObject + ChangeLog
        │
        ▼
Apply changes to original (preserve formatting)
        │
        ▼
Add annotations/comments/track-changes
        │
        ▼
Output file in original format
```

---

## Success Criteria

1. **Accuracy** — Issues are real, not hallucinated
2. **Actionable** — Suggested rewrites are usable
3. **Proportional** — Strong docs get few issues
4. **Fast** — Quick tier < 30s, Standard < 60s
5. **Grounded** — Every issue cites specific text

---

## Non-Negotiables

1. **Never invent content** — All issues grounded in document text
2. **Never silently rewrite** — All changes surfaced as tracked changes or annotations
3. **Acknowledge strengths** — Agents can return "no issues"
4. **Borderline = not a violation** — When uncertain, don't flag
5. **Export matches input format** — PDF→PDF, DOCX→DOCX

---

## Architecture Ground Truth

- Only **Extractor** and **Clarity** see full text.
- All other agents operate on the map + targeted lookups.
- **Assembler** is deterministic (LLM only inside Consensus Mode adjudication).
- V0 Domain routes to **FIELD only**; citation verification is V1.
- **Clarity** is one agent with two passes (sentence-level, then block-level).