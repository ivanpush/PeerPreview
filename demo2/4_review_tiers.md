# PeerPreview: Review Tiers

## Overview

Four review tiers with increasing depth, model capability, and cost. Even the lowest tier focuses on substantive logic and reasoning — this is a thinking tool, not a grammar checker.

---

## Quick Scan
**$0.25–1.00**

> Fast logic check on your core argument.
> 
> Scans your key sections for reasoning gaps, unsupported claims, internal contradictions, and mislabeled evidence. Not a grammar pass — a sanity check on whether your argument holds together.

**What you get:**
- Priority sections analyzed
- Claim-evidence alignment check
- Internal consistency scan
- Logical gaps flagged
- Rewrites for major issues

---

## Full Review
**$0.50–2.50**

> Thorough analysis of your entire argument.
> 
> Every section examined for logical soundness, evidentiary support, and structural coherence. The review you'd get from a rigorous colleague who traced every claim back to its support.

**What you get:**
- All sections analyzed
- Full rigor + clarity pass
- Cross-section consistency check
- Domain positioning (where relevant)
- Rewrites for major + moderate issues

---

## Deep Analysis
**$1.00–4.00**

> What your toughest critic will say.
> 
> Adversarial analysis that finds every weakness before your reviewers do. Overclaiming, hidden assumptions, missing limitations, alternative explanations you didn't address.

**What you get:**
- Everything in Full Review
- Adversarial reviewer pass
- Domain expert analysis  
- Rewrites for all issues

---

## Master Review
**$3.00–10.00+**

> Multi-model verification for high-stakes work.
> 
> Three frontier models analyze independently. Agreement means high confidence. Disagreement means you need to look closely. Maximum rigor for documents where the outcome matters.

**What you get:**
- Everything in Deep Analysis
- 3 frontier models (Claude, Gemini, GPT)
- Disagreement flagging
- Confidence scoring per issue
- Consensus rewrites

---

## Lever Summary

| Lever | Quick Scan | Full Review | Deep Analysis | Master Review |
|-------|------------|-------------|---------------|---------------|
| **Model** | Haiku | Sonnet | Sonnet | Frontier × 3 |
| **Reasoning depth** | Core logic | Full analysis | Adversarial | Adversarial × 3 |
| **Section coverage** | Priority (top 3) | All | All | All |
| **Domain Expert** | — | If scope needs | ✓ | ✓ |
| **Cross-model** | — | — | — | ✓ |
| **Rewrites on** | Major | Major + Moderate | All | All + consensus |
| **Cost** | $0.25–1.00 | $0.50–2.50 | $1.00–4.00 | $3.00–10.00+ |

---

## What Each Tier Checks

| Check | Quick | Full | Deep | Master |
|-------|:-----:|:----:|:----:|:------:|
| Claim-evidence alignment | ✓ | ✓ | ✓ | ✓ |
| Internal contradictions | ✓ | ✓ | ✓ | ✓ |
| Logical gaps / non-sequiturs | ✓ | ✓ | ✓ | ✓ |
| Mislabeled reasoning | ✓ | ✓ | ✓ | ✓ |
| Cross-section consistency | — | ✓ | ✓ | ✓ |
| Domain positioning | — | If needed | ✓ | ✓ |
| Overclaiming detection | — | — | ✓ | ✓ |
| Hidden assumptions | — | — | ✓ | ✓ |
| Missing limitations | — | — | ✓ | ✓ |
| Alternative explanations | — | — | ✓ | ✓ |
| Model disagreement flags | — | — | — | ✓ |

---

## Internal Tier Mapping

Maps user-facing tiers to internal depth system:

| User Tier | Internal Depth | Persona Schema Behavior |
|-----------|----------------|-------------------------|
| Quick Scan | `light` | Supportive tone, brief rationales |
| Full Review | `standard` | Balanced tone, detailed rationales |
| Deep Analysis | `heavy` | Adversarial tone, exhaustive rationales |
| Master Review | `master` | Adversarial × 3, reconciled rationales |