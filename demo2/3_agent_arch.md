# PeerPreview: Agent Architecture & Pipeline

## Core Insight

**Personas are output frames, not processing units.**

The backend runs a small set of agents that produce raw analysis. An Assembler then reframes that analysis into document-type-specific scopes and personas at render time.

This means:
- Backend agents are reusable across document types
- UI scopes (Rigor, Significance, Precedent, etc.) are views on the same underlying analysis
- Persona voice/tone is applied at the end, not baked into each agent

---

## Backend Agents

All agents run at every tier. Depth controls behavior intensity.

| Agent | Purpose |
|-------|---------|
| `global_map_agent` | Structure, claims, evidence links, argument map |
| `domain_positioning_agent` | Field detection, related work, novelty signals |
| `rigor_agent` | Logic, stats, methods, feasibility |
| `clarity_paragraphs` | Sentence/paragraph level readability |
| `clarity_blocks` | Multi-paragraph flow and structure |
| `global_hostile_agent` | Adversarial synthesis, weakness exploitation |
| `assembler_agent` | Maps backend → scopes → personas |

Full prompts in `05-BASE-AGENT-PROMPTS.md`.

---

## Pipeline

```
ManuscriptObject + UserIntent
            │
            ▼
      Planning Agent
            │
            ▼
   PHASE 1: Global Understanding
   ├── Global Map Agent (depth varies by tier)
   └── Domain Positioning Agent (Full Review+ only)
            │
            ▼
   PHASE 2: Local Track Agents (parallel)
   ├── Rigor Agent (depth varies by tier)
   ├── Clarity B1 (always full)
   └── Clarity B2 (Full Review+ only)
            │
            ▼
   PHASE 3a: Global Hostile Agent (Deep Analysis only)
            │
            ▼
   PHASE 3b: Assembler
   (maps tracks → scopes → personas, merges)
            │
            ▼
      Final Issue[] + Persona Summaries
```

---

## Scope → Backend → Persona Mapping

### Scientific Manuscript

| UI Scope | Backend Agents | Persona Label | Archetype |
|----------|----------------|---------------|-----------|
| rigor | global_map, rigor | "Rigor Review" | Careful grad student |
| clarity | clarity | "Clarity Review" | Journal editor |
| counterpoint | domain_positioning, global_hostile | "Counterpoint" | Hostile domain expert |

### Grant Application

| UI Scope | Backend Agents | Persona Label | Archetype |
|----------|----------------|---------------|-----------|
| significance | domain_positioning, global_hostile | "Significance Review" | Program officer |
| innovation | domain_positioning, global_hostile | "Innovation Review" | Skeptical study section |
| approach_rigor | global_map, rigor | "Approach & Rigor" | Methods reviewer |
| feasibility | rigor, global_hostile | "Feasibility & Team Fit" | Pragmatic PI |

### Policy Brief

| UI Scope | Backend Agents | Persona Label | Archetype |
|----------|----------------|---------------|-----------|
| evidence_quality | global_map, rigor, domain_positioning | "Evidence Review" | Research analyst |
| stakeholder_objections | domain_positioning, global_hostile | "Stakeholder Objections" | Political staffer |
| implementation_feasibility | rigor, global_hostile | "Implementation Feasibility" | Agency bureaucrat |
| clarity | clarity | "Clarity & Messaging" | Comms director |

### Legal Brief

| UI Scope | Backend Agents | Persona Label | Archetype |
|----------|----------------|---------------|-----------|
| precedent_strength | domain_positioning, global_hostile | "Precedent Strength" | Opposing counsel |
| factual_support | global_map, rigor | "Factual Support" | Skeptical judge |
| procedural | rigor, clarity | "Procedural & Technical" | Court clerk |
| persuasive_force | clarity, global_hostile | "Persuasive Force" | Senior partner |

### Generic Document

| UI Scope | Backend Agents | Persona Label | Archetype |
|----------|----------------|---------------|-----------|
| consistency | global_map, rigor | "Consistency Review" | Careful reader |
| clarity | clarity | "Clarity Review" | Editor |
| claim_strength | global_map, rigor, domain_positioning | "Claim Strength" | Skeptic |

---

## Data Models

### ReviewPlan

```python
@dataclass
class ReviewPlan:
    document_type: DocumentType
    depth: Literal['first_pass', 'full_review', 'deep_analysis']
    consensus: bool  # True if consensus mode enabled (deep only)
    
    # Persona schema
    persona_schema: Literal[
        'scientific_manuscript', 'grant_application', 
        'policy_brief', 'legal_brief', 'generic'
    ]
    
    # Which UI scopes to run
    scopes_to_run: list[str]
    
    # Which backend tracks needed (derived from scopes)
    tracks_to_run: list[Literal[
        'global_map', 'rigor', 'clarity', 
        'domain_positioning', 'global_hostile'
    ]]
    
    run_global_hostile: bool
    
    section_priorities: list[str]
    sections_to_skip: list[str]
    
    user_focus_summary: str
    user_constraints: list[str]
    
    max_tokens_per_call: int
    total_budget_tokens: int
```

### Issue

```python
@dataclass
class Issue:
    id: str
    
    # Backend track (which agent produced this)
    track: Literal['global_map', 'rigor', 'clarity', 
                   'domain_positioning', 'global_hostile']
    
    # UI scope (set by Assembler)
    scope: str
    
    # Persona label (set by Assembler)
    persona_label: str
    
    code: str
    severity: Literal['major', 'moderate', 'minor']
    
    location: IssueLocation
    
    rationale: str
    suggestion: str | None
    proposed_rewrite: str | None
    
    source_agent_ids: list[str]
    merged_from_ids: list[str]
    conflicting_issue_ids: list[str]
```

### GlobalMap

```python
@dataclass
class GlobalMap:
    section_roles: dict[str, str]
    argument_flow: list[str]
    claims: list[Claim]
    evidence_links: list[EvidenceLink]
    key_terms: list[str]
    undefined_terms: list[str]
    potential_weaknesses: list[str]
    cross_section_tensions: list[tuple[str, str]]

@dataclass
class Claim:
    id: str
    text: str
    location: IssueLocation
    strength: Literal['strong', 'moderate', 'weak', 'unsupported']

@dataclass  
class EvidenceLink:
    claim_id: str
    supporting_locations: list[str]
    link_strength: Literal['direct', 'indirect', 'missing']
```

---

## Persona Map Config

```json
{
  "scientific_manuscript": {
    "scopes": ["rigor", "clarity", "counterpoint"],
    "scope_to_backend": {
      "rigor": ["global_map", "rigor"],
      "clarity": ["clarity"],
      "counterpoint": ["domain_positioning", "global_hostile"]
    },
    "scope_to_persona": {
      "rigor": {"label": "Rigor Review", "archetype": "careful_grad_student"},
      "clarity": {"label": "Clarity Review", "archetype": "journal_editor"},
      "counterpoint": {"label": "Counterpoint Review", "archetype": "hostile_domain_expert"}
    }
  },
  
  "grant_application": {
    "scopes": ["significance", "innovation", "approach_rigor", "feasibility"],
    "scope_to_backend": {
      "significance": ["domain_positioning", "global_hostile"],
      "innovation": ["domain_positioning", "global_hostile"],
      "approach_rigor": ["global_map", "rigor"],
      "feasibility": ["rigor", "global_hostile"]
    },
    "scope_to_persona": {
      "significance": {"label": "Significance Review", "archetype": "program_officer"},
      "innovation": {"label": "Innovation Review", "archetype": "skeptical_study_section"},
      "approach_rigor": {"label": "Approach & Rigor", "archetype": "methods_reviewer"},
      "feasibility": {"label": "Feasibility & Team Fit", "archetype": "pragmatic_pi"}
    }
  },

  "policy_brief": {
    "scopes": ["evidence_quality", "stakeholder_objections", "implementation_feasibility", "clarity"],
    "scope_to_backend": {
      "evidence_quality": ["global_map", "rigor", "domain_positioning"],
      "stakeholder_objections": ["domain_positioning", "global_hostile"],
      "implementation_feasibility": ["rigor", "global_hostile"],
      "clarity": ["clarity"]
    },
    "scope_to_persona": {
      "evidence_quality": {"label": "Evidence Review", "archetype": "research_analyst"},
      "stakeholder_objections": {"label": "Stakeholder Objections", "archetype": "political_staffer"},
      "implementation_feasibility": {"label": "Implementation Feasibility", "archetype": "agency_bureaucrat"},
      "clarity": {"label": "Clarity & Messaging", "archetype": "comms_director"}
    }
  },

  "legal_brief": {
    "scopes": ["precedent_strength", "factual_support", "procedural", "persuasive_force"],
    "scope_to_backend": {
      "precedent_strength": ["domain_positioning", "global_hostile"],
      "factual_support": ["global_map", "rigor"],
      "procedural": ["rigor", "clarity"],
      "persuasive_force": ["clarity", "global_hostile"]
    },
    "scope_to_persona": {
      "precedent_strength": {"label": "Precedent Strength", "archetype": "opposing_counsel"},
      "factual_support": {"label": "Factual Support Review", "archetype": "skeptical_judge"},
      "procedural": {"label": "Procedural & Technical", "archetype": "court_clerk"},
      "persuasive_force": {"label": "Persuasive Force", "archetype": "senior_partner"}
    }
  },

  "generic": {
    "scopes": ["consistency", "clarity", "claim_strength"],
    "scope_to_backend": {
      "consistency": ["global_map", "rigor"],
      "clarity": ["clarity"],
      "claim_strength": ["global_map", "rigor", "domain_positioning"]
    },
    "scope_to_persona": {
      "consistency": {"label": "Consistency Review", "archetype": "careful_reader"},
      "clarity": {"label": "Clarity Review", "archetype": "editor"},
      "claim_strength": {"label": "Claim Strength", "archetype": "skeptic"}
    }
  }
}
```

---

## Agent Prompts

### Global Map Agent

```
Extract document structure:

1. CLAIMS: Every substantive claim
   - Location, text, strength (strong/moderate/weak/unsupported)

2. EVIDENCE LINKS: What supports each claim?
   - Direct, indirect, or missing support

3. ARGUMENT FLOW: Logical progression of claims

4. TERMINOLOGY: Key terms, undefined terms

5. EARLY HOSTILE SKETCH: What would a skeptic attack?

OUTPUT: JSON with section_roles, claims, evidence_links, argument_flow, 
        key_terms, undefined_terms, potential_weaknesses
```

### Domain Positioning Agent

```
Assess document's field positioning:

1. FIELD DETECTION: What field/subfield?
2. NOVELTY: What's claimed as new? Any overclaiming?
3. RELATED WORK GAPS: What should be cited but isn't?
4. STAKEHOLDERS: Who would oppose? What interests affected?
5. SIGNIFICANCE: If true, how important?

OUTPUT: JSON with field, novelty_assessment, related_work_gaps, 
        stakeholder_concerns, significance_assessment
```

### Rigor Agent

```
Check section for methodological issues:

1. LOGIC: Non-sequiturs, contradictions, circular reasoning
2. METHODOLOGY: Missing details, inappropriate methods
3. STATISTICS: Misinterpretation, missing tests
4. FEASIBILITY: Can this be done? Resources sufficient?

GROUNDEDNESS: Only flag clear violations. May return empty if sound.

OUTPUT: JSON with section_assessment, strengths, issues[]
```

### Clarity Agent

```
Check for clarity issues:

PARAGRAPH LEVEL (B1):
- Ambiguous references
- Jargon without definition
- Overly complex sentences

BLOCK LEVEL (B2):
- Transition quality
- Logical progression
- Section cohesion

Only flag issues that block comprehension. Style preferences ≠ violations.
```

### Global Hostile Agent

```
You are Reviewer 2 — hostile expert.

Find attacks that would SINK this document:
1. BIGGEST LOGICAL GAPS
2. OVERCLAIMING
3. MISSING LIMITATIONS
4. ALTERNATIVE EXPLANATIONS
5. FIELD POSITIONING ATTACKS

Use global_map + domain_positioning + existing issues.
Adversarial but GROUNDED — cannot invent problems.

OUTPUT: JSON with grudging_acknowledgments, killer_issues[]
```

### Assembler Agent

```
Map backend issues → scopes → personas.

TASKS:
1. Assign each issue to appropriate UI scope
2. Merge duplicates (preserve source_agent_ids)
3. Rewrite rationales to be clear and direct

RULES:
- Preserve factual content
- Do not invent new issues
- Keep proposed_rewrite verbatim

OUTPUT: JSON with final_issues[], persona_summaries{}
```

---

## Execution Flow

```python
async def run_review(manuscript, user_intent):
    # 1. Planning
    plan = await planning_agent.plan_review(manuscript, user_intent)
    
    # 2. Phase 1: Global Understanding
    global_map = await global_map_agent.analyze(
        manuscript, plan, depth=plan.depth
    )
    
    # Domain positioning only runs at Full Review and Deep Analysis
    domain_positioning = None
    if plan.depth in ['full_review', 'deep_analysis']:
        domain_positioning = await domain_positioning_agent.analyze(
            manuscript, global_map, plan, depth=plan.depth
        )
    
    # 3. Phase 2: Local Tracks (parallel)
    tasks = [
        rigor_agent.analyze(manuscript, global_map, plan, depth=plan.depth),
        clarity_paragraphs.analyze(manuscript, plan),  # always full
    ]
    
    # Clarity B2 only at Full Review+
    if plan.depth != 'first_pass':
        tasks.append(clarity_blocks.analyze(manuscript, plan))
    
    local_results = await asyncio.gather(*tasks)
    raw_issues = flatten(local_results)
    
    # 4. Phase 3a: Global Hostile (Deep Analysis only)
    if plan.depth == 'deep_analysis':
        hostile_issues = await global_hostile_agent.analyze(
            manuscript, global_map, domain_positioning, raw_issues, plan
        )
        raw_issues.extend(hostile_issues)
    
    # 5. Phase 3b: Assembler
    final_issues, persona_summaries = await assembler_agent.assemble(
        plan, raw_issues, global_map
    )
    
    # 6. Consensus Mode (if enabled, Deep only)
    if plan.consensus and plan.depth == 'deep_analysis':
        final_issues = await run_consensus(
            manuscript, plan, final_issues
        )
    
    return ReviewResult(plan, final_issues, persona_summaries, global_map)
```

---

## Depth → Agent Behavior

Depth scales behavior. Some agents only run at higher tiers.

| Agent | First Pass | Full Review | Deep Analysis |
|-------|------------|-------------|---------------|
| Global Map | Shallow (claims only) | Full (claims + evidence) | Max (+ argument chain) |
| Domain Positioning | Off | Full | Full + retrieval |
| Rigor | Major issues only | Full section-level | Expert-level |
| Clarity B1 | Full | Full | Full |
| Clarity B2 | Off | Full | Full |
| Global Hostile | Off | Off | **ON** |

| Aspect | First Pass | Full Review | Deep Analysis |
|--------|------------|-------------|---------------|
| **Model** | Haiku | Sonnet | Opus + Sonnet |
| **Tokens/call** | 1–3k | 10–20k | 20–40k |
| **Rewrites on** | Major | Major + Moderate | All |
| **Cost** | $0.25–1.00 | $0.50–2.50 | $1.00–4.00 |

See `04-REVIEW-TIERS.md` for full canonical definitions.

---

## File Structure

```
/backend/
├── agents/
│   ├── planning_agent.py
│   ├── global_map_agent.py
│   ├── domain_positioning_agent.py
│   ├── rigor_agent.py
│   ├── clarity_paragraphs.py
│   ├── clarity_blocks.py
│   ├── global_hostile_agent.py
│   └── assembler_agent.py
├── core/
│   ├── models.py
│   ├── persona_map.py
│   └── llm_client.py
├── pipeline/
│   └── orchestrator.py
├── config/
│   └── persona_map.json
└── examples/
```

---

## UI Scope Selection

UI shows document-type-specific scopes:

- **Scientific Manuscript**: `[Rigor] [Clarity] [Counterpoint]`
- **Grant Application**: `[Significance] [Innovation] [Approach] [Feasibility]`
- **Policy Brief**: `[Evidence] [Stakeholders] [Implementation] [Clarity]`
- **Legal Brief**: `[Precedent] [Factual] [Procedural] [Persuasive]`

User selects scopes → Planning Agent derives tracks_to_run.