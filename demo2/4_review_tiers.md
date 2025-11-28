# PeerPreview: Review Tiers (Canonical)

## Core Principle

**Depth scales behavior.** Some agents only run at higher tiers. Global Hostile only at Deep.

---

## 🟢 First Pass

**Core identity**: Fast, cheap, mostly clarity + obvious logic flaws.

**Cost**: $0.25–1.00  
**Model**: Opus (Planning) + Haiku (other agents)  
**Token limits**: 1–3k per call

### User-Facing Copy

> Core logic, structure, major issues.

### Agent Behavior

| Agent | Behavior |
|-------|----------|
| Global Map | Claims only (no evidence linking), tiny hostile sketch |
| Domain Positioning | **Off** |
| Rigor | Major contradictions / unsupported primary claims only |
| Clarity B1 | Full rewrite coverage (main value of this tier) |
| Clarity B2 | Off |
| Global Hostile | Off |

**Mental model**: Quick scan + rewrites + 2–5 major logic flags.

---

## 🔵 Full Review

**Core identity**: Comprehensive section-level review.

**Cost**: $0.50–2.50  
**Model**: Opus (Planning) + Sonnet (other agents)  
**Token limits**: 10–20k per call

### User-Facing Copy

> Full-section critique with balanced depth.

### Agent Behavior

| Agent | Behavior |
|-------|----------|
| Global Map | Full claims + evidence map |
| Domain Positioning | Full (field detect + novelty claims + light retrieval if available) |
| Rigor | Full section-level: methods, consistency, assumptions |
| Clarity B1 | Full |
| Clarity B2 | Full |
| Global Hostile | Disabled |

**Mental model**: Editorial + methodological + structural correctness.

---

## 🟣 Deep Analysis

**Core identity**: Everything + hostile adversarial reasoning.

**Cost**: $1.00–4.00  
**Models**: Opus (Planning, Global Map, Domain Pos, Hostile, Rigor), Sonnet (Clarity, Assembler)  
**Token limits**: 20–40k per call

### User-Facing Copy

> Adversarial expert review of claims, methods, and reasoning.

### RAG Behavior

- **Document-level keyword RAG**: After Global Map, Perplexity search on document keywords (field, claims, methods)
- Research bundle attached to Domain Positioning + downstream agents
- No automatic issue-level RAG (single model, no disagreements)

### Agent Behavior

| Agent | Behavior |
|-------|----------|
| Global Map | Full + expanded argument chain + contradiction graph |
| Domain Positioning | Full + retrieval-backed + precedent/related work |
| Rigor | Full expert-level |
| Clarity B1 | Full |
| Clarity B2 | Full |
| Global Hostile | **ENABLED** |

**Mental model**: Hostile review + expert critique + novelty/precedent checking.

---

## 🔥 Consensus Mode (Deep only)

**Core identity**: Triangulated frontier-model adjudication.

**Cost**: +$2.00–6.00 (on top of Deep Analysis)  
**Models**: 3× frontier (e.g., Claude Opus, GPT-5.1, Gemini Ultra)

### User-Facing Copy

> Three top models cross-check and reconcile disagreements.

### RAG Behavior

- **Document-level keyword RAG**: Same as Deep Analysis (upfront)
- **Issue-level RAG (auto)**: On disagreement or vague responses
  - Targeted Perplexity search on issue keywords
  - Single model (Opus) re-evaluates with research
  - If still unresolved → flag to user as "Disputed"

### Behavior

- 3 independent Deep Analysis runs
- Consensus Reducer detects contradictions
- On disagreement: auto issue-level RAG → Opus re-evaluates
- If resolved → merged issue with "Resolved with research" tag
- If unresolved → flagged as "Disputed" with all model stances shown
- Confidence score per issue

**Mental model**: Three Reviewer #2s argue; you get the reconciliation.

---

## 🔬 Go Deeper (Post-Review Add-on)

**Available on**: Deep Analysis, Consensus  
**Cost**: ~$0.30–0.50 per issue  
**Trigger**: User batch-selects issues, clicks "Run Deep Research"

### What It Does

- Runs Perplexity **Deep Research** mode (exhaustive, multi-step search)
- Extended Opus analysis (2-3× token budget)
- Returns research brief with sources, reasoning trace, verdict, confidence

### User-Facing Copy

> Get exhaustive research and expert analysis on selected issues.

### Availability by Track

| Track | Go Deeper Available? | Why |
|-------|---------------------|-----|
| `domain_positioning` | ✅ | External literature helps |
| `rigor` | ✅ | Field standards, norms |
| `global_hostile` | ✅ | If field-related |
| `clarity` | ❌ | Just rewrite it |
| `global_map` | ❌ | Internal document issue |

### Issue States

| State | UI | Can Select? |
|-------|-----|-------------|
| `available` | Checkbox enabled | ✅ |
| `not_applicable` | No checkbox (clarity track) | — |
| `completed` | "Deep Research ✓" tag, disabled | ❌ |

### Flow

```
User selects issues (batch)
      │
      ▼
[ Run Deep Research ($X.XX) ]  ← price updates with count
      │
      ▼
Per issue:
  - Perplexity Deep Research (15-30s)
  - Extended Opus analysis
      │
      ▼
Issues updated with:
  - "Deep Research" tag
  - Expandable analysis panel
  - Sources, reasoning, verdict, confidence
      │
      ▼
User can select OTHER issues for another batch
```

### UX Hints

- If issue is disputed (Consensus): Nudge toward Go Deeper
- If issue is not disputed: Soft friction (confirm cost)

---

## Final Levers Matrix

| Lever | First Pass | Full Review | Deep Analysis | + Consensus |
|-------|------------|-------------|---------------|-------------|
| **Backend agents** | Core only | All | All (max) | 3× All (max) |
| **Model** | Opus + Haiku | Opus + Sonnet | Opus | 3× Frontier |
| **Token limit** | 1–3k | 10–20k | 20–40k | 20–40k × 3 |
| **Global Map depth** | Shallow | Full | Maximal | Maximal³ |
| **Doc-level RAG** | Off | Off | ✅ Perplexity | ✅ Perplexity |
| **Issue-level RAG** | Off | Off | Off | ✅ Auto on disagreement |
| **Domain Positioning** | Off | Full | Full + RAG | Full + RAG³ |
| **Rigor** | Major issues only | Full | Expert-level | Expert-level³ |
| **Clarity B1** | Full | Full | Full | Full³ |
| **Clarity B2** | Off | Full | Full | Full³ |
| **Global Hostile** | Off | Off | **ON** | ON³ |
| **Rewrites on** | Major | Major + Moderate | All | All + reconciled |
| **Go Deeper** | Off | Off | ✅ Available | ✅ Available |
| **Cost** | $0.25–1.00 | $0.50–2.50 | $1.00–4.00 | +$2.00–6.00 |

**Note**: Planning always uses Opus. Other agents use Haiku/Sonnet/Opus based on tier.

---

## What Each Tier Checks

| Check | First | Full | Deep |
|-------|:-----:|:----:|:----:|
| Claim-evidence alignment | Major only | ✓ | ✓ |
| Internal contradictions | Major only | ✓ | ✓ |
| Logical gaps / non-sequiturs | Major only | ✓ | ✓ |
| Mislabeled reasoning | Major only | ✓ | ✓ |
| Cross-section consistency | — | ✓ | ✓ |
| Domain positioning | — | ✓ | ✓ + retrieval |
| Overclaiming detection | — | — | ✓ |
| Hidden assumptions | — | — | ✓ |
| Missing limitations | — | — | ✓ |
| Alternative explanations | — | — | ✓ |
| Adversarial synthesis | — | — | ✓ |

---

## Internal Mapping

| User-Facing | Internal Alias | Depth Value |
|-------------|----------------|-------------|
| First Pass | `light` | `first_pass` |
| Full Review | `standard` | `full_review` |
| Deep Analysis | `heavy` | `deep_analysis` |
| + Consensus | — | `consensus: true` |

---

## Model Selection by Agent

Planning uses Opus at all tiers — it's one call, it's the steering wheel, don't cheap out.

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

**Notes:**
- "per-model" at ***+ means each frontier model (Opus, GPT-5.1, Gemini 2) runs that agent independently
- Assembler doesn't need per-model since it runs after Consensus Reducer consolidates
- Planning at Opus even for First Pass ensures user intent is captured correctly