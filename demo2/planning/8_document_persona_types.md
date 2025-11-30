# 08: Document Type Personas

> **Version Note:** In V0, Domain contributes only to the FIELD tab. Citation-verification and routing to RIGOR will be introduced in V1. Personas in this document describe final behavior; V0 implementation uses FIELD-only routing.

## Design Principle

**Tabs are immutable. Archetypes are content, not chrome.**

The UI displays the same three tabs regardless of document type. This builds muscle memory and eliminates per-session learning curves. The document-specific "persona" emerges through the *voice* of the feedback text, not through badges, labels, or variable UI elements.

---

## The Universal Trinity (3 Fixed Tabs)

These tabs never change, no matter what document is uploaded:

| Tab | What It Catches | Mental Model |
|-----|-----------------|--------------|
| **CLARITY** | Readability, flow, grammar, formatting, structure | "Fix the English." |
| **RIGOR** | Accuracy, citations, data integrity, logic consistency | "Fix the Errors." |
| **FIELD** | Persuasion, novelty, defenses, counter-arguments | "Fix the Argument." |

---

## Agent → Tab Mapping

The `assembler_agent` routes the backend agents into the 3 immutable tabs:

### CLARITY (The Polish)
Low-stakes, easy-to-fix issues.

| Agent | Contribution |
|-------|--------------|
| `clarity_agent` (sentence pass) | Sentence-level readability |
| `clarity_agent` (block pass) | Multi-paragraph flow |

> **Note:** Clarity is implemented as a single agent with two passes (sentence-level then block-level). These personas reflect cognitive modes, not separate agents.

**Vibe:** Helpful, neutral, corrective.

### RIGOR (The Proof)
Objective issues — right or wrong.

| Agent | Contribution |
|-------|--------------|
| `rigor_agent` | Math, methods, stats, logic |
| `domain_agent` | Citations, precedent, factual accuracy (V1 only) |

**Vibe:** Strict, factual, binary.

### FIELD (The Win)
Subjective, adversarial — where the value lives.

| Agent | Contribution |
|-------|--------------|
| `adversary_agent` | Adversarial synthesis, weakness exploitation |
| `domain_agent` | Novelty claims, market/field positioning |

> **Note:** Extractor (map builder) is upstream only — produces ArgumentMap but no issue cards.

**Vibe:** Critical, insightful, challenging.

---

## Archetypes as Voice, Not Labels

**Don't use badges. Don't use tags. Use voice.**

The archetype is the prompt personality used to *write* the card text. Users recognize the persona through tone, not UI chrome.

### Example: Scientific Manuscript → FIELD Tab

```
Card Title: Unsupported Conclusion

"This is a stretch. You claim X in the abstract, but your data in 
Figure 3 only supports Y. A critical reviewer will reject this immediately."
```
*(User recognizes "Reviewer 2" through the text itself)*

### Example: Legal Brief → FIELD Tab

```
Card Title: Distinguishable Precedent

"Opposing counsel will argue that Smith v. Jones doesn't apply here 
because the jurisdiction is different. You need to address this 
distinction explicitly."
```
*(User recognizes "Opposing Counsel" through the context)*

### Example: Grant Proposal → RIGOR Tab

```
Card Title: Timeline Mismatch

"Aim 2 depends on completion of Aim 1, but you've allocated them 
to the same year. A study section panelist will flag this as 
infeasible."
```
*(User recognizes "Study Section Panelist" through domain framing)*

---

## Document-Type Archetype Reference

The `assembler_agent` uses these personas when rewriting output for each document type:

### Scientific Manuscript
| Tab | Voice |
|-----|-------|
| Clarity | Copy editor |
| Rigor | Grad student methodologist |
| Strategy | Hostile expert / "Reviewer 2" |

### Grant Proposal
| Tab | Voice |
|-----|-------|
| Clarity | Grants administrator |
| Rigor | Study section methodologist |
| Strategy | Skeptical program officer |

### Policy Brief
| Tab | Voice |
|-----|-------|
| Clarity | Communications specialist |
| Rigor | Research analyst |
| Strategy | Political opposition / Agency bureaucrat |

### Legal Brief
| Tab | Voice |
|-----|-------|
| Clarity | Court clerk |
| Rigor | Skeptical judge |
| Strategy | Opposing counsel |

### Generic Document
| Tab | Voice |
|-----|-------|
| Clarity | Editor |
| Rigor | Careful reader |
| Strategy | Skeptic |

---

## User Controls

| Control | Function |
|---------|----------|
| **Depth selector** | Controls exhaustiveness/harshness (token budget, issue threshold, number of flags) |
| **User input field** | Free text for concerns, focus areas, context ("Nature submission", "focus on stats", "worried about policy recs") |

---

## Implementation Notes

- UI is "boring" (stable, predictable) — content is exciting (voice-driven, domain-specific)
- Depth affects how much the archetype "leans in" — low depth = constructive, high depth = adversarial
- User input gets injected into agent context to weight attention toward specified areas
- The assembler rewrites technical output into persona voice; it doesn't label the persona