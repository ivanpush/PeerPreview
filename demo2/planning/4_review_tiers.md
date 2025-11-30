# 04: Review Tiers

## Overview

Three tiers control **depth of analysis**, not number of issues. A strong document should return few issues at any tier.

| Tier | Primary Models | Cost | Latency | Mental Model |
|------|----------------|------|---------|--------------|
| **Quick** | Opus (Extractor) + Haiku | $0.50–1.50 | ~30s | "Fast polish before sharing a draft" |
| **Standard** | Opus (Extractor) + Sonnet | $1.00–3.00 | ~60s | "Thorough prep for peer review" |
| **Deep** | Opus (Extractor, Adversary) + Sonnet | $2.00–5.00 | ~120s | "Stress-test before high-stakes submission" |

**Note:** Extractor always runs Opus — it builds the ArgumentMap everything else depends on. See Model Selection table for full breakdown.

**Add-on:**
- **Consensus** (+$3–8) — 3 frontier models (Claude, GPT, Gemini), disagreement flagging, confidence scoring. Deep tier only.

---

## Tier Comparison Matrix

| Capability | Quick | Standard | Deep |
|------------|-------|----------|------|
| **Extractor** | Lite (claims only) | Full (claims + evidence + structure) | Maximal (+ red flags) |
| **Clarity** | Major issues only | Full (2-pass: sentence + block) | Full (2-pass) |
| **Rigor** | Major issues, no tools | Full | Expert |
| **Domain** | Skip | 1-3 Perplexity queries | 3-5 Pro queries + Go Deeper available |
| **Adversary** | Skip | Light (top 3-5 attacks) | Full + bias profile |
| **Consensus** | No | No | Optional toggle |
| **Go Deeper** | No | No | Available per-issue |

---

## Quick Tier

**Core identity:** Fast, cheap — prose polish + major logic flags.

**Who runs:**
| Agent | Behavior |
|-------|----------|
| Extractor | Lite map (claims only, no evidence linking) |
| Clarity | Full (this is main value) |
| Rigor | Major contradictions only, no tool calls |
| Domain | Skip |
| Adversary | Skip |

**Token budget:** 1-3k per agent call
**Model:** Haiku
**Cost:** $0.25–1.00

**Output:** Quick scan + rewrites + 2-5 major logic flags

---

## Standard Tier

**Core identity:** Comprehensive section-level review.

**Who runs:**
| Agent | Behavior |
|-------|----------|
| Extractor | Full map (claims + evidence + methods + definitions) |
| Clarity | Full 2-pass (sentence-level + block-level) |
| Rigor | Full internal consistency pass |
| Domain | 1-3 Perplexity queries, positioning analysis |
| Adversary | Light pass (top 3-5 attack vectors) |

**Token budget:** 10-20k per agent call
**Model:** Sonnet
**Cost:** $0.50–2.50

**Output:** Editorial + methodological + structural + light adversarial

---

## Deep Tier

**Core identity:** Everything + hostile adversarial reasoning.

**Who runs:**
| Agent | Behavior |
|-------|----------|
| Extractor | Maximal map (+ effect sizes, red flags) |
| Clarity | Full 2-pass |
| Rigor | Expert-level (V1: + stats tools) |
| Domain | 3-5 Perplexity Pro queries, full positioning |
| Adversary | Full hostile review + bias profile |

**Token budget:** 20-40k per agent call
**Model:** Opus (Extractor, Adversary), Sonnet (others)
**Cost:** $2.00–5.00

**Output:** Full expert review + adversarial stress-test

**Exclusive features:**
- Consensus mode (optional)
- Go Deeper (per-issue deep research)

---

## Consensus Mode (Deep + Toggle)

**What it is:** Run Rigor + Adversary across 3 frontier models, aggregate results.

**What runs once (shared):**
- Extractor (Opus)
- Domain (Perplexity)
- Clarity (optional — style-based, low value from consensus)

**What runs 3× (per model: Claude, GPT, Gemini):**
- Rigor
- Adversary

**Aggregation:**
| Agreement | Confidence | Display |
|-----------|------------|---------|
| 3/3 agree | High | Single merged card |
| 2/3 agree | Medium | Merged card + dissent note |
| 0/3 agree | Low | Show all 3 perspectives |

**Auto-resolution:** On disagreement, issue-level Perplexity search attempts to resolve.

**Cost:** +$2–6 over Deep base

---

## Go Deeper (Deep Tier Only)

Per-issue deep dive when user requests more investigation.

**Eligible issues:**
- Domain/positioning (novelty, related work)
- Rigor issues involving external claims
- Adversary issues referencing field norms

**Not eligible:**
- Clarity issues (prose quality)
- Internal consistency issues (no external lookup helps)

**Flow:**
1. User clicks "Go Deeper" on card
2. Domain Agent runs Perplexity Deep Research for that issue
3. Heavy model receives issue + map nodes + research bundle
4. Returns expanded analysis + sources + confidence

**Cost:** Billed per call. Hard cap per document (e.g., 5 calls).

---

## RAG Behavior by Tier

| Tier | Document-Level RAG | Citation Verification | Issue-Level RAG |
|------|-------------------|----------------------|-----------------|
| Quick | None | None (V0) | None |
| Standard | 1-3 queries (field context) | None (V0) | None |
| Deep | 3-5 Pro queries | None (V0) | Go Deeper (on request) |
| Consensus | Shared (run once) | None (V0) | Auto on disagreement |

**V1:** Citation verification will be added to Standard (flagged) and Deep (all).

---

## Model Selection

| Agent | Quick | Standard | Deep |
|-------|-------|----------|------|
| Extractor | Opus | Opus | Opus |
| Clarity | Haiku | Sonnet | Sonnet |
| Rigor | Haiku | Sonnet | Sonnet |
| Domain | — | Sonnet | Sonnet |
| Adversary | — | Sonnet | Opus |
| Assembler | — | — | — |

**Notes:**
- **Extractor** is always Opus — it builds the ArgumentMap that everything else depends on
- **Adversary** upgrades to Opus at Deep tier for more sophisticated attacks
- **Domain** always uses Sonnet for reasoning/writeup; "Pro queries" refers to Perplexity Pro tier, not the LLM
- **Tool access** (Perplexity, code exec) is tier-gated, not model-gated
- **Assembler** performs deterministic merging/deduplication (no model call). Only uses LLM adjudicator inside Consensus Mode via `assembler_consensus.md` prompt.

---

## Pricing Breakdown

*Estimates based on ~10-15 page document. Actual cost varies by length.*

### Quick (~$0.50–1.50)
- Extractor (Opus): ~$0.40
- Clarity (Haiku): ~$0.10
- Rigor (Haiku): ~$0.05

### Standard (~$1.00–3.00)
- Extractor (Opus): ~$0.50
- Clarity (Sonnet): ~$0.30
- Rigor (Sonnet): ~$0.30
- Domain (Sonnet + Perplexity): ~$0.40
- Adversary (Sonnet): ~$0.25

### Deep (~$2.00–5.00)
- Extractor (Opus): ~$0.70
- Clarity (Sonnet): ~$0.40
- Rigor (Sonnet): ~$0.50
- Domain (Sonnet + Pro Perplexity): ~$0.80
- Adversary (Opus): ~$0.80

### Consensus (+$3–8)
- 3× Rigor: ~$1.50
- 3× Adversary: ~$2.40
- Consensus clustering: ~$0.20
- LLM adjudicator (Consensus only): ~$0.30
- Issue-level RAG (V1): ~$0.50

*Note: Assembler is deterministic and incurs no model cost outside of Consensus Mode adjudication.*

---

## User-Facing Copy

### Quick
> **Quick Scan** — Fast polish for prose, grammar, and clarity. Catches issues you'd miss after staring at the same draft too long. Best for early drafts.

### Standard
> **Full Review** — Comprehensive analysis of logic, structure, and positioning. The review you'd want before sending to collaborators or reviewers.

### Deep
> **Deep Analysis** — Expert-level stress test with adversarial critique and field context. Best for high-stakes submissions (Nature, grants, legal filings).

### Consensus
> **Multi-Model Consensus** — Three frontier models review independently, highlighting agreements and flagging disputes. Maximum confidence for critical documents.