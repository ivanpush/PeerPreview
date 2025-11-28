# PeerPreview: Review Tiers

## Overview

Three review tiers with increasing depth and domain specificity. Optional consensus mode for high-stakes work.

---

## First Pass
**$0.25–1.00**

> Core logic, structure, major issues.

**What you get:**
- Priority sections analyzed
- Claim-evidence alignment check
- Internal consistency scan
- Logical gaps flagged
- Rewrites for major issues

---

## Full Review
**$0.50–2.50**

> Full-section critique with balanced depth.

**What you get:**
- All sections analyzed
- Full rigor + clarity pass
- Cross-section consistency check
- Domain positioning (where relevant)
- Rewrites for major + moderate issues

---

## Deep Analysis
**$1.00–4.00**

> Adversarial expert review of claims, methods, and reasoning.

**What you get:**
- Everything in Full Review
- Domain expert analysis
- Overclaiming detection
- Hidden assumptions surfaced
- Missing limitations flagged
- Alternative explanations considered
- Rewrites for all issues

---

## Consensus Mode (Deep only)
**+$2.00–6.00**

> Three top models cross-check and reconcile disagreements.

Available as add-on to Deep Analysis only.

**What you get:**
- 3 frontier models (Claude, Gemini, GPT)
- Independent analysis from each
- Disagreement flagging
- Confidence scoring per issue
- Consensus rewrites

---

## Lever Summary

| Lever | First Pass | Full Review | Deep Analysis | + Consensus |
|-------|------------|-------------|---------------|-------------|
| **Model** | Haiku | Sonnet | Sonnet | Frontier × 3 |
| **Section coverage** | Priority | All | All | All |
| **Domain Expert** | — | If relevant | ✓ | ✓ |
| **Cross-model** | — | — | — | ✓ |
| **Rewrites on** | Major | Major + Moderate | All | All + reconciled |
| **Cost** | $0.25–1.00 | $0.50–2.50 | $1.00–4.00 | +$2.00–6.00 |

---

## What Each Tier Checks

| Check | First | Full | Deep |
|-------|:-----:|:----:|:----:|
| Claim-evidence alignment | ✓ | ✓ | ✓ |
| Internal contradictions | ✓ | ✓ | ✓ |
| Logical gaps / non-sequiturs | ✓ | ✓ | ✓ |
| Mislabeled reasoning | ✓ | ✓ | ✓ |
| Cross-section consistency | — | ✓ | ✓ |
| Domain positioning | — | If relevant | ✓ |
| Overclaiming detection | — | — | ✓ |
| Hidden assumptions | — | — | ✓ |
| Missing limitations | — | — | ✓ |
| Alternative explanations | — | — | ✓ |

Consensus mode adds: model disagreement flags, confidence scoring, reconciled rewrites.

---

## Internal Mapping

| User-Facing | Internal Alias | Depth Value |
|-------------|----------------|-------------|
| First Pass | `light` | `first_pass` |
| Full Review | `standard` | `full_review` |
| Deep Analysis | `heavy` | `deep_analysis` |
| + Consensus | — | `consensus: true` |