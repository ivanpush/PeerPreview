# 05: Prompt Selector & Prompt Library

## Overview

The Prompt Selector is a **deterministic function** (not an LLM) that chooses prompt variants for each agent based on structured inputs. This replaces the need for an LLM-based "Planner" or "Router" agent.

**Why deterministic?**

| Approach | Latency | Debuggability | Failure Modes |
|----------|---------|---------------|---------------|
| LLM Planner | +2-5s | Hard (why did it route?) | Misrouting cascades |
| Deterministic Selector | ~0ms | Easy (inspect logic) | Predictable, testable |

LLM routers are warranted when agent sets are large/heterogeneous or user queries are unstructured. Neither applies here — topology is fixed, doc types are known, and Extractor provides structured signals.

---

## Inputs

The Prompt Selector receives:

| Input | Source | Type |
|-------|--------|------|
| `doc_type` | User selected or auto-detected | enum |
| `tier` | User selected | `quick` \| `standard` \| `deep` |
| `chips` | User selected | `string[]` |
| `review_plan.track_emphasis` | Extractor output | `{agent: "high"\|"medium"\|"low"}` |
| `review_plan.map_characteristics` | Extractor output | `{flag: boolean}` |

---

## Outputs

```python
@dataclass
class PromptSelection:
    clarity_prompt: str      # path to prompt file
    rigor_prompt: str
    domain_prompt: str
    adversary_prompt: str    # None if tier=quick
    assembler_mode: Literal["base", "consensus"]  # Assembler is rule-based, not LLM-prompted
```

---

## Prompt Library Structure

```
prompts/
├── shared/
│   └── header.md                 # Shared rules for all agents
│
├── clarity/
│   ├── clarity_base.md           # Default clarity prompt
│   ├── clarity_technical.md      # Heavy jargon tolerance
│   ├── clarity_legal.md          # Preserve legal precision
│   └── clarity_accessible.md     # Plain language focus
│
├── rigor/
│   ├── rigor_base.md             # Default rigor checks
│   ├── rigor_methods_heavy.md    # Methodology-focused
│   ├── rigor_theoretical.md      # Logic/proof-focused
│   ├── rigor_clinical.md         # Clinical trial standards
│   ├── rigor_grant.md            # Feasibility/budget focus
│   └── rigor_legal.md            # Precedent/procedure focus
│
├── domain/
│   ├── domain_base.md            # Default positioning
│   ├── domain_nature_tier.md     # High-impact journal standards
│   ├── domain_field_journal.md   # Domain-appropriate rigor
│   └── domain_legal.md           # Jurisdiction/precedent focus
│
├── adversary/
│   ├── adversary_base.md         # Generic Reviewer 2
│   ├── adversary_reviewer2.md    # Academic hostile reviewer
│   ├── adversary_grant_panel.md  # Study section panelist
│   ├── adversary_opposing_counsel.md  # Legal adversary
│   └── adversary_policy_opposition.md # Political opposition
│
└── assembler/
    ├── assembler_base.md         # Default assembly
    └── assembler_consensus.md    # Multi-model aggregation
```

---

## Selection Logic

```python
def select_prompts(
    doc_type: str,
    tier: str,
    chips: list[str],
    review_plan: ReviewPlan
) -> PromptSelection:
    """
    Deterministic prompt selection based on structured inputs.
    No LLM calls. Pure logic.
    """
    
    prompts = PromptSelection()
    map_chars = review_plan.map_characteristics
    track_emphasis = review_plan.track_emphasis
    
    # ─────────────────────────────────────────────────────────
    # CLARITY SELECTION
    # ─────────────────────────────────────────────────────────
    if doc_type == "legal_brief":
        prompts.clarity = "clarity_legal.md"
    elif doc_type == "policy_brief":
        prompts.clarity = "clarity_accessible.md"
    elif map_chars.get("jargon_heavy") and track_emphasis.get("clarity") == "high":
        prompts.clarity = "clarity_technical.md"
    else:
        prompts.clarity = "clarity_base.md"
    
    # ─────────────────────────────────────────────────────────
    # RIGOR SELECTION
    # ─────────────────────────────────────────────────────────
    if doc_type == "grant":
        prompts.rigor = "rigor_grant.md"
    elif doc_type == "legal_brief":
        prompts.rigor = "rigor_legal.md"
    elif "methodology" in chips:
        prompts.rigor = "rigor_methods_heavy.md"
    elif map_chars.get("clinical"):
        prompts.rigor = "rigor_clinical.md"
    elif map_chars.get("theoretical"):
        prompts.rigor = "rigor_theoretical.md"
    elif map_chars.get("methods_heavy"):
        prompts.rigor = "rigor_methods_heavy.md"
    else:
        prompts.rigor = "rigor_base.md"
    
    # ─────────────────────────────────────────────────────────
    # DOMAIN SELECTION
    # ─────────────────────────────────────────────────────────
    if "nature-tier" in chips:
        prompts.domain = "domain_nature_tier.md"
    elif doc_type == "legal_brief":
        prompts.domain = "domain_legal.md"
    elif doc_type in ["grant", "policy_brief"]:
        prompts.domain = "domain_field_journal.md"
    else:
        prompts.domain = "domain_base.md"
    
    # ─────────────────────────────────────────────────────────
    # ADVERSARY SELECTION
    # ─────────────────────────────────────────────────────────
    if tier == "quick":
        prompts.adversary = None  # Adversary skipped at Quick tier
    elif doc_type == "grant":
        prompts.adversary = "adversary_grant_panel.md"
    elif doc_type == "legal_brief":
        prompts.adversary = "adversary_opposing_counsel.md"
    elif doc_type == "policy_brief":
        prompts.adversary = "adversary_policy_opposition.md"
    else:
        prompts.adversary = "adversary_reviewer2.md"
    
    # Note: Adversary prompt is selected here but execution is tier-controlled.
    # Quick tier skips Adversary entirely regardless of prompt selection.
    
    # ─────────────────────────────────────────────────────────
    # ASSEMBLER MODE (rule-based, not LLM-prompted)
    # ─────────────────────────────────────────────────────────
    # Consensus requires BOTH deep tier AND user toggle
    if tier == "deep" and review_plan.consensus_enabled:
        prompts.assembler_mode = "consensus"
    else:
        prompts.assembler_mode = "base"
    
    return prompts
```

---

## Map Characteristics

The Extractor outputs structural flags that inform prompt selection:

```python
@dataclass
class MapCharacteristics:
    methods_heavy: bool = False      # >30% of claims are methodology
    data_heavy: bool = False         # Lots of tables/figures/stats
    theoretical: bool = False        # Proofs, derivations, no experiments
    clinical: bool = False           # Human subjects, trials, IRB
    multi_study: bool = False        # Meta-analysis or multi-experiment
    jargon_heavy: bool = False       # High domain-specific terminology
    has_code: bool = False           # Software/algorithm descriptions
    citation_density: str = "normal" # low | normal | high
```

These are boolean/categorical flags derived from the ArgumentMap during extraction. They enable prompt specialization without requiring an LLM router.

---

## Chip Taxonomy

Chips are user-selected focus areas that modify prompt selection and Assembler filtering.

### Focus Area Chips

| Chip | Effect |
|------|--------|
| `methodology` | Select `rigor_methods_heavy.md`, boost methods issues |
| `novelty` | Boost domain positioning issues |
| `statistics` | Enable stats verification in Rigor |
| `clarity` | Boost clarity issues, lower severity threshold |
| `citations` | Enable citation verification in Domain |

### Submission Context Chips

| Chip | Effect |
|------|--------|
| `nature-tier` | Select `domain_nature_tier.md`, strictest standards |
| `field-journal` | Domain-appropriate rigor |
| `preprint` | Lighter touch, focus on major issues |
| `internal-draft` | Very light, clarity-focused |

### Review Mode Chips

| Chip | Effect |
|------|--------|
| `consensus` | Enable multi-model consensus (Deep tier) |
| `go-deeper-all` | Pre-authorize Go Deeper on all eligible issues |

---

## User Free Text Handling

Free text is not used for prompt selection. Instead, it's:

1. **Parsed by Extractor** into `review_plan.user_focus_parsed`
2. **Injected into agent prompts** as attention-weighting context

Example injection:

```
USER FOCUS: The author is particularly concerned about statistical methodology
and whether Reviewer 2 will attack the novelty claims.

Prioritize:
- Issues related to stats, p-values, sample sizes, analytical rigor
- Weaknesses in novelty framing and positioning
```

This is appended to the selected prompt, not used to select the prompt.

---

## Tier Interaction

Prompt selection is mostly tier-agnostic. Tiers control:

| What Tier Controls | Mechanism |
|--------------------|-----------|
| Which agents run | Orchestrator logic (Adversary skipped at Quick) |
| Agent thoroughness | Token budget, issue threshold |
| Tool access | Perplexity queries, code execution |
| Consensus | Only available at Deep |

Prompt selection is the same across tiers except:
- `adversary_prompt = None` at Quick tier
- `assembler_consensus.md` selected when consensus enabled

---

## Execution Flow

```
User Inputs (doc_type, tier, chips, free_text)
         │
         ▼
    ┌──────────┐
    │ Extractor │──→ ArgumentMap + ReviewPlan (includes map_characteristics)
    └──────────┘
         │
         ▼
    ┌─────────────────┐
    │ Prompt Selector │ (deterministic, ~0ms)
    │                 │
    │ Inputs:         │
    │ - doc_type      │
    │ - tier          │
    │ - chips         │
    │ - map_chars     │
    │ - track_emphasis│
    │                 │
    │ Outputs:        │
    │ - clarity_prompt    = "clarity_legal.md"
    │ - rigor_prompt      = "rigor_methods_heavy.md"
    │ - domain_prompt     = "domain_base.md"
    │ - adversary_prompt  = "adversary_reviewer2.md"
    │ - assembler_mode    = "base"
    └─────────────────┘
         │
         ▼
    Agents execute with selected prompts
    (Assembler is rule-based, uses mode not prompt)
```

---

## Prompt Template Structure

Each prompt file follows this structure:

```markdown
# {Agent Name} Prompt

## Role
{One-line role description}

## Inputs
{What this agent receives}

## Task
{What this agent does}

## Output Schema
{JSON schema for output}

## Constraints
{Hard rules}

## Tier Behavior
{How behavior changes by tier — token budget, thoroughness}

## Examples
{Few-shot examples if helpful}
```

---

## Example Prompts

### rigor_base.md

```markdown
# Rigor Agent — Base

## Role
Check internal correctness, consistency, and logical coherence.

## Inputs
- ArgumentMap (claims, evidence, methods, definitions)
- Sentence lookup access
- ReviewPlan (priority sections, hotspots, user focus)
- Confidence mask (if consensus mode)

## Task
For each claim in the ArgumentMap:
1. Check if linked evidence actually supports the claim
2. Check if methods described could produce the claimed results
3. Check if definitions are used consistently
4. Check if statistics are plausible (not verification — pattern matching)

For cross-section consistency:
1. Check if Methods describes what Results reports
2. Check if Abstract matches Conclusions
3. Check if Figures match text descriptions

## Text Window Policy
- Default: ±1 sentence context
- Methods: ±2-3 sentences
- Results: Full paragraph
- Statistics: Include linked table text
- Cross-section: All linked nodes + ±1 each

## Output Schema
{
  "issues": [
    {
      "id": "R-{n}",
      "issue_type": "single_sentence | cross_section | structural",
      "title": "string",
      "message": "string",
      "severity": "major | moderate | minor",
      "locations": [...],
      "original_texts": {...},
      "suggested_rewrite": "string" | null,
      "suggested_rewrites": [...] | null,
      "rationale": "string",
      "confidence": 0.0-1.0
    }
  ]
}

## Constraints
- Only flag issues you can ground in specific text
- When uncertain, assign lower confidence, don't skip
- Cross-section issues require fetching all involved sentences

## Tier Behavior
- Quick: Major issues only, no tool calls, low token budget
- Standard: Full pass
- Deep: Expert-level, stats validation
```

### adversary_reviewer2.md

```markdown
# Adversary Agent — Hostile Reviewer 2

## Role
Attack the paper's argument, positioning, and strategy like a skeptical expert reviewer.

## Inputs
- ArgumentMap
- Rigor issues (from Rigor Agent)
- DomainReport (from Domain Agent)
- Abstract + Introduction text

## Task
Find the weakest points a hostile reviewer would exploit:

1. **Overclaiming**: Where do conclusions exceed what evidence supports?
2. **Missing controls**: What experiments/analyses are absent?
3. **Novelty gaps**: What prior work undermines the novelty claim?
4. **Methodology weaknesses**: What would a methods expert attack?
5. **Statistical concerns**: What would a statistician question?
6. **Framing problems**: How could the narrative be challenged?

For each attack:
- Identify the vulnerable claim/section
- Articulate the attack as a reviewer would phrase it
- Suggest a preemptive defense or revision

## Output Schema
{
  "attacks": [
    {
      "id": "A-{n}",
      "title": "string",
      "attack": "string (as reviewer would phrase it)",
      "target_nodes": ["C1", "M2"],
      "severity": "fatal | major | moderate",
      "suggested_defense": "string",
      "locations": [...]
    }
  ],
  "strategic_recommendations": [
    {
      "recommendation": "string",
      "rationale": "string"
    }
  ],
  "bias_profile": {  // Deep tier only
    "reviewer_archetype": "string",
    "likely_objections": ["string"],
    "overall_vulnerability": "high | medium | low"
  }
}

## Constraints
- Attack the argument, not the author
- Every attack must be grounded in specific text or Rigor/Domain findings
- "Fatal" severity only for issues that would likely cause rejection
- Suggested defenses should be actionable

## Tier Behavior
- Quick: Skip entirely
- Standard: Light pass, top 3-5 attacks only
- Deep: Full hostile review, bias profile, all attack vectors
```

---

## Adding New Prompt Variants

To add a new prompt variant:

1. Create the prompt file in the appropriate directory
2. Add selection logic to `select_prompts()`
3. Document the trigger conditions

Example: Adding `rigor_computational.md` for CS papers

```python
# In select_prompts():
elif map_chars.get("has_code") and doc_type == "scientific_manuscript":
    prompts.rigor = "rigor_computational.md"
```

---

## Testing Prompt Selection

```python
def test_prompt_selection():
    # Test 1: Grant with methodology focus
    result = select_prompts(
        doc_type="grant",
        tier="standard",
        chips=["methodology"],
        review_plan=ReviewPlan(
            map_characteristics=MapCharacteristics(methods_heavy=True),
            track_emphasis={"rigor": "high"}
        )
    )
    assert result.rigor == "rigor_grant.md"  # doc_type wins over chip
    
    # Test 2: Legal brief
    result = select_prompts(
        doc_type="legal_brief",
        tier="deep",
        chips=[],
        review_plan=ReviewPlan(...)
    )
    assert result.clarity == "clarity_legal.md"
    assert result.adversary == "adversary_opposing_counsel.md"
    
    # Test 3: Quick tier skips Adversary
    result = select_prompts(
        doc_type="scientific_manuscript",
        tier="quick",
        chips=[],
        review_plan=ReviewPlan(...)
    )
    assert result.adversary is None
```

---

## Summary

- **Prompt Selector is deterministic** — no LLM calls, pure logic
- **Prompt Library is extensible** — add variants without changing architecture
- **Selection is based on structured inputs** — doc_type, tier, chips, map_characteristics
- **Free text is injected, not used for selection** — attention weighting, not routing
- **Tier controls execution, not prompts** — which agents run, how thorough, what tools