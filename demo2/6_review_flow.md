# PeerPreview: Review Flow

## Tier Key

```
*      First Pass    (Opus + Haiku,    $0.25–1.00)
**     Full Review   (Opus + Sonnet,   $0.50–2.50)
***    Deep Analysis (Opus,            $1.00–4.00)
***+   + Consensus   (3× Frontier,     +$2–6)
```

Planning Agent uses Opus at all tiers — it's one call, it's the steering wheel, don't cheap out.

---

## RAG Integration

### When RAG Runs

| Tier | Document-Level RAG | Issue-Level RAG |
|------|-------------------|-----------------|
| * First Pass | — | — |
| ** Full Review | — | — |
| *** Deep Analysis | ✅ After Global Map | — |
| ***+ Consensus | ✅ After Global Map | ✅ Auto on disagreement |

### Document-Level RAG Flow (*** and ***+)

```
Global Map complete
      │
      ▼
Extract keywords:
  - field/domain
  - key claims
  - methods mentioned
  - novelty signals
      │
      ▼
Perplexity Search (Pro mode)
      │
      ▼
Research bundle (top 5-10 results)
      │
      ▼
Attached to Domain Positioning prompt
      │
      ▼
Available to downstream agents
```

### Issue-Level RAG Flow (***+ only)

```
Consensus Reducer detects disagreement
      │
      ▼
Extract issue keywords
      │
      ▼
Perplexity Search (targeted)
      │
      ▼
Single model (Opus) re-evaluates
      │
      ├── Resolved → "Resolved with research" tag
      │
      └── Still disputed → Flag to user
```

---

## Flow Diagram

```
START
│
├── Input:
│     DocumentObject
│     UserIntent
│     Depth (* / ** / *** / ***+)
│
└──► PLANNING AGENT  (* ** *** ***+)
        Inputs:
            - DocumentObject
            - UserIntent
            - depth tier
        Outputs:
            - ReviewPlan {
                 scopes_to_run,
                 tracks_to_run,
                 run_global_hostile,
                 section_priorities,
                 persona_schema,
                 token_budgets,
                 consensus_flag
              }
│
│
├──► PHASE 1: GLOBAL UNDERSTANDING
│
│     GLOBAL MAP AGENT  (* ** *** ***+)
│         Inputs:
│             - DocumentObject
│             - ReviewPlan
│         Outputs:
│             - global_map {
│                  section_roles,
│                  claims,
│                  evidence_links,
│                  argument_flow,
│                  key_terms,
│                  undefined_terms,
│                  potential_weaknesses,
│                  cross_section_tensions
│               }
│
│     DOCUMENT-LEVEL RAG  (*** ***+ only)
│         *      NOT RUN
│         **     NOT RUN
│         ***    RUN
│         ***+   RUN
│         Inputs:
│             - global_map.key_terms
│             - global_map.claims (keywords)
│             - field signals
│         Process:
│             - Perplexity Pro Search
│         Outputs:
│             - research_bundle {
│                  sources[],
│                  synthesized_context
│               }
│
│     DOMAIN POSITIONING AGENT  (** *** ***+)
│         *      NOT RUN
│         **     RUN
│         ***    RUN (with research_bundle)
│         ***+   RUN per-model (with research_bundle)
│         Inputs:
│             - DocumentObject
│             - global_map
│             - research_bundle (*** ***+ only)
│             - ReviewPlan
│         Outputs:
│             - domain_positioning {
│                  field,
│                  novelty_assessment,
│                  related_work_gaps,
│                  stakeholder_concerns,
│                  significance_assessment
│               }
│
│
├──► PHASE 2: LOCAL TRACK AGENTS (async parallel)
│
│     RIGOR AGENT  (* ** *** ***+)
│         Inputs:
│             - DocumentObject
│             - global_map
│             - ReviewPlan
│         Outputs:
│             - issues_rigor[]
│
│
│     CLARITY PARAGRAPHS (B1)  (* ** *** ***+)
│         Inputs:
│             - DocumentObject
│             - ReviewPlan
│         Outputs:
│             - clarity_paragraph_issues[]
│
│
│     CLARITY BLOCKS (B2)  (** *** ***+)
│         *      NOT RUN
│         **     RUN
│         ***    RUN
│         ***+   RUN per-model
│         Inputs:
│             - DocumentObject
│             - ReviewPlan
│         Outputs:
│             - clarity_block_issues[]
│
│
├──► PHASE 3: GLOBAL HOSTILE AGENT  (*** ***+)
│         *      NOT RUN
│         **     NOT RUN
│         ***    RUN
│         ***+   RUN per-model
│         Inputs:
│             - DocumentObject
│             - global_map
│             - domain_positioning
│             - local_track_issues
│             - ReviewPlan
│         Outputs:
│             - hostile_issues[]
│
│
├──► PHASE 4: ASSEMBLER AGENT  (* ** *** ***+)
│         Inputs:
│             - ReviewPlan
│             - global_map
│             - raw_issues (rigor + clarity + hostile)
│         Tasks:
│             - merge duplicates
│             - assign scopes
│             - assign persona labels
│             - build persona summaries
│             - detect conflicts
│         Outputs:
│             - final_issues[]
│             - persona_summaries{}
│             - global_map
│
│
├──► PHASE 5: CONSENSUS REDUCER  (***+ only)
│         *      NOT RUN
│         **     NOT RUN
│         ***    NOT RUN
│         ***+   RUN
│         Inputs:
│             - model_A_result
│             - model_B_result
│             - model_C_result
│         Tasks:
│             - detect disagreements
│             - score confidence
│             - consolidate per-issue
│             - produce consensus rewrites
│         Outputs:
│             - consensus_final_issues[]
│             - disagreement_flags
│             - confidence_per_issue
│
│
├──► PHASE 5b: ISSUE-LEVEL RAG RESOLUTION  (***+ only, if disagreements)
│         Trigger: disagreement_flags not empty
│         Per flagged issue:
│             │
│             ▼
│         Extract issue keywords
│             │
│             ▼
│         Perplexity Search (targeted)
│             │
│             ▼
│         Opus re-evaluates with research
│             │
│             ├── Resolved → update issue, add "Resolved with research" tag
│             │
│             └── Still disputed → keep flag, show all model stances
│
│
└──► RETURN TO UI  (* ** *** ***+)
        - DocumentObject
        - final_issues[] or consensus_final_issues[]
        - persona_summaries
        - global_map
```

---

## Agent Summary by Tier

| Agent | * | ** | *** | ***+ |
|-------|---|----|----|------|
| Planning | ✓ | ✓ | ✓ | ✓ |
| Global Map | ✓ | ✓ | ✓ | ✓ per-model |
| Domain Positioning | — | ✓ | ✓ | ✓ per-model |
| Rigor | ✓ | ✓ | ✓ | ✓ per-model |
| Clarity B1 | ✓ | ✓ | ✓ | ✓ per-model |
| Clarity B2 | — | ✓ | ✓ | ✓ per-model |
| Global Hostile | — | — | ✓ | ✓ per-model |
| Assembler | ✓ | ✓ | ✓ | ✓ |
| Consensus Reducer | — | — | — | ✓ |

---

## Model Selection by Agent

| Agent | * | ** | *** | ***+ |
|-------|---|----|----|------|
| Planning | Opus | Opus | Opus | Opus |
| Global Map | Haiku | Sonnet | Opus | per-model |
| Domain Positioning | — | Sonnet | Opus | per-model |
| Rigor | Haiku | Sonnet | Opus | per-model |
| Clarity B1 | Haiku | Sonnet | Sonnet | per-model |
| Clarity B2 | — | Sonnet | Opus | per-model |
| Global Hostile | — | — | Opus | per-model |
| Assembler | Haiku | Sonnet | Sonnet | Sonnet |
| Consensus Reducer | — | — | — | Opus |

**per-model** = each frontier model (Opus, GPT-5.1, Gemini 2) runs independently

---

## Go Deeper (Post-Review)

Available on Deep Analysis (***) and Consensus (***+) tiers.

### Flow

```
Review complete → UI displays issues
      │
      ▼
User views issues
  - Each eligible issue has checkbox
  - Clarity track issues: no checkbox (not applicable)
  - Already-deepened issues: disabled checkbox + "Deep Research ✓" tag
      │
      ▼
User batch-selects issues
      │
      ▼
[ Run Deep Research ($X.XX) ]  ← price updates with selection count
      │
      ▼
Per selected issue:
      │
      ├── Perplexity Deep Research mode
      │     - Multi-step, iterative search
      │     - 10-15 results synthesized
      │     - ~15-30 seconds
      │
      ▼
      ├── Extended Opus analysis (2-3× tokens)
      │     - Full reasoning trace
      │     - Source integration
      │     - Confidence scoring
      │
      ▼
Issue updated:
  - Status: completed
  - Tag: "Deep Research ✓"
  - Checkbox: disabled
  - Expandable panel with:
      - Original stance(s)
      - Sources found
      - Reasoning trace
      - Final verdict
      - Confidence %
      │
      ▼
User can select OTHER issues for another batch
```

### Eligible Tracks

| Track | Go Deeper? | Reason |
|-------|-----------|--------|
| `domain_positioning` | ✅ | Literature helps |
| `rigor` | ✅ | Field standards |
| `global_hostile` | ✅ | If field-related |
| `clarity` | ❌ | Just rewrite it |
| `global_map` | ❌ | Internal logic |

### Issue State Machine

```
                    ┌─────────────────┐
                    │   available     │ ← default for eligible tracks
                    └────────┬────────┘
                             │
                      user selects
                             │
                             ▼
                    ┌─────────────────┐
                    │     queued      │
                    └────────┬────────┘
                             │
                      batch runs
                             │
                             ▼
                    ┌─────────────────┐
                    │   completed     │ ← "Deep Research ✓" tag
                    └─────────────────┘
                    
                    ┌─────────────────┐
                    │ not_applicable  │ ← clarity track (no checkbox)
                    └─────────────────┘
```

### UX Hints

- **Disputed issue (Consensus)**: Nudge → "Models disagreed. Deep Research can help."
- **Non-disputed issue**: Soft friction → "This will cost $X. Continue?"

### Cost

- ~$0.30–0.50 per issue
- Perplexity Deep Research: ~$0.05–0.10
- Extended Opus: ~$0.20–0.40