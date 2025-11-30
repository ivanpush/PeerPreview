# PeerPreview: Tier Value Comparison

## TL;DR

| Tier | Model | RAG | Special |
|------|-------|-----|---------|
| **First Pass** | Haiku | — | Fast, cheap, major issues only |
| **Full Review** | Sonnet | Basic (1 query) | Field-aware, thorough |
| **Deep Analysis** | Opus | Pro (3-5 queries) | Adversarial + Go Deeper |
| **Consensus** | 3× Frontier | Pro + issue-level | 3 experts, dispute handling |

---

## The Upgrade Story

```
First Pass     →  "Is my argument broken?"
Full Review    →  "Is my argument solid?"
Deep Analysis  →  "What would sink my argument?"
Consensus      →  "What do 3 experts think?"
```

---

## Model Progression

| Tier | Model | Why |
|------|-------|-----|
| First Pass | Haiku | Fast, cheap, catches obvious |
| Full Review | Sonnet | Catches subtle reasoning gaps |
| Deep Analysis | Opus | Expert-level, adversarial thinking |
| Consensus | Opus + GPT-5.1 + Gemini | Coverage, calibration, confidence |

---

## RAG Progression

| Aspect | First Pass | Full Review | Deep Analysis | Consensus |
|--------|------------|-------------|---------------|-----------|
| **Perplexity mode** | — | Regular | Pro | Pro |
| **Queries** | — | 1 broad | 3-5 targeted | 3-5 (shared) |
| **What you get** | — | 1 synthesis + citations | 3-5 syntheses + richer citations | Same as Deep |
| **Issue-level RAG** | — | — | — | Auto on disagreement |
| **Go Deeper** | — | — | ✅ (Deep Research mode) | ✅ (Deep Research mode) |
| **Cost** | — | ~$0.005 | ~$0.02-0.03 | ~$0.03-0.10 |
| **Latency** | — | ~2s | ~5-8s | ~5-8s |

**Note**: Consensus runs doc-level RAG **once**, shared across all 3 models. Not 3× cost.

### Query Strategy by Tier

**Full Review** (1 broad query):
```
"{document field} {main claims} recent research"
```

**Deep Analysis** (3-5 targeted queries):
```
1. "{field} state of the art"
2. "{main novelty claim} prior work"
3. "{methodology} best practices standards"
4. "{key result} alternative explanations"  
5. "{limitations} common criticisms"
```

**Go Deeper** (per-issue, Deep Research mode):
```
Perplexity Deep Research on specific issue keywords
→ Multi-step, exhaustive, internally iterative
```

---

## Agent Progression

| Agent | First Pass | Full Review | Deep Analysis | Consensus |
|-------|------------|-------------|---------------|-----------|
| Planning | Opus | Opus | Opus | Opus |
| Global Map | Shallow | Full | Maximal | Maximal × 3 |
| Domain Positioning | — | ✅ | ✅ + deep RAG | ✅ × 3 |
| Rigor | Major only | Full | Expert-level | Expert × 3 |
| Clarity B1 | Full | Full | Full | Full × 3 |
| Clarity B2 | — | ✅ | ✅ | ✅ × 3 |
| Global Hostile | — | — | ✅ | ✅ × 3 |

---

## What Each Tier Adds

### First Pass → Full Review

| New | Value |
|-----|-------|
| Sonnet (vs Haiku) | Catches subtle reasoning gaps |
| Domain Positioning | Field awareness, novelty assessment |
| Evidence linking | Maps claim → evidence dependencies |
| Clarity B2 | Block flow, transitions, structure |
| Basic RAG | "Your claim overlaps with Chen 2024" |
| More rewrites | Major + Moderate issues |

### Full Review → Deep Analysis

| New | Value |
|-----|-------|
| Opus (vs Sonnet) | Expert-level reasoning |
| Deep RAG | Multi-query, synthesized research |
| Global Hostile | "What would sink this?" adversarial pass |
| Expert rigor | Stats, methods, feasibility scrutiny |
| Go Deeper | Post-review deep research option |
| All rewrites | Even minor issues get suggestions |

### Deep Analysis → Consensus

| New | Value |
|-----|-------|
| 3 models | Different perspectives, better coverage |
| Confidence scoring | Know when something is solid vs uncertain |
| Dispute flagging | "This is a judgment call" signals |
| Auto issue RAG | Attempts to resolve disagreements |
| Model stances | See what each expert thinks |

---

## Cost Breakdown

| Tier | Model Cost | RAG Cost | Total |
|------|------------|----------|-------|
| First Pass | $0.20-0.80 | — | **$0.25-1.00** |
| Full Review | $0.40-2.00 | ~$0.01 | **$0.50-2.50** |
| Deep Analysis | $0.90-3.50 | ~$0.03 | **$1.00-4.00** |
| + Consensus | $2.70-10.50 | ~$0.05 | **+$2.00-6.00** |

RAG cost is noise. Model tier is the driver.

---

## Go Deeper (Add-on)

Available at Deep Analysis and Consensus.

| Aspect | Value |
|--------|-------|
| Cost | ~$0.30-0.50 per issue |
| Search | Perplexity Deep Research (exhaustive) |
| Analysis | Extended Opus (2-3× tokens) |
| Output | Sources, reasoning trace, verdict, confidence |
| Eligible tracks | Domain Positioning, Rigor, Global Hostile |
| Not eligible | Clarity (just rewrite it) |

---

## User Decision Guide

| If you need... | Choose |
|----------------|--------|
| Quick sanity check on a draft | First Pass |
| Thorough review for submission | Full Review |
| Maximum rigor, find what I missed | Deep Analysis |
| High-stakes, need confidence | Consensus |

---

## One-Liners

| Tier | Pitch |
|------|-------|
| **First Pass** | Fast logic check. Catches major issues. Good for drafts. |
| **Full Review** | Thorough analysis. Field-aware. Catches what you missed. |
| **Deep Analysis** | Adversarial expert review. Finds what would sink you. |
| **Consensus** | Three experts. See where they agree and where they don't. |