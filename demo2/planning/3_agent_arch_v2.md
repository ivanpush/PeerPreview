# 03: Agent Architecture v2

## Design Philosophy

**Compress, then reason.**

One heavy pass builds a structured understanding of the document. All subsequent agents reason over that structure plus targeted text lookups.

**Two global passes, not one:**
- **Extractor** — global *reasoning* pass (builds the map)
- **Clarity** — global *editing* pass (fixes prose)

Clarity is the principled exception. It does surface-form work (grammar, flow, transitions) that requires seeing actual sentences and neighboring context. You can't fix prose you can't see. All other agents (Rigor, Domain, Adversary) operate on the compressed map plus targeted lookups.

**We are reviewers, not editors.**

PeerPreview returns issue cards with suggested fixes. Users apply changes in their own tools. We surface problems and recommendations — we don't modify documents.

**Deterministic routing, not LLM planning.**

Agent topology is fixed. A deterministic Prompt Selector chooses prompt variants based on document type, user chips, and map characteristics. No LLM router for V1 — it adds latency, debugging complexity, and failure modes without proportional benefit.

---

## Inputs

| Input | Source | Description |
|-------|--------|-------------|
| **Indexed JSON** | Upstream parser | Document with sentence-level IDs already assigned |
| **Document Type** | User selected or auto-detected | manuscript, grant, policy_brief, legal_brief, generic |
| **Depth Tier** | User selected | Quick, Standard, Deep |
| **Chips** | User selected | Structured focus areas (methodology, novelty, Nature-tier, etc.) |
| **Free Text** | User written | Unstructured concerns ("worried about stats", "focus on novelty claims") |

---

## Outputs

### Issue Cards

Each card contains:

```json
{
  "id": "A-7",
  "tab": "RIGOR",
  "issue_type": "single_sentence | cross_section | structural",
  "title": "Overstated effect size",
  "message": "Your claim says 20% but Table 1 shows 15%.",
  "severity": "major",
  
  "locations": [
    {
      "section_id": "sec_results",
      "paragraph_id": "p_res_3",
      "sentence_ids": ["s_res_3_2"],
      "role": "primary"
    }
  ],
  
  "original_texts": {
    "s_res_3_2": "We found a 20% improvement in all conditions."
  },
  
  "suggested_rewrite": "We found a 15% improvement in most conditions tested.",
  
  "rationale": "Table 1 shows 15% average improvement. Only 3 of 5 conditions showed significant improvement."
}
```

### Multi-Location Issues (Cross-Section Inconsistencies)

When an issue spans multiple locations (e.g., Methods says X, Results implies Y):

```json
{
  "id": "A-12",
  "tab": "RIGOR",
  "issue_type": "cross_section",
  "title": "Methods/Results technique mismatch",
  "message": "Methods describes Western blot but Results reports qPCR-style data.",
  "severity": "major",
  
  "locations": [
    {
      "section_id": "sec_methods",
      "paragraph_id": "p_met_4",
      "sentence_ids": ["s_met_4_1"],
      "role": "source"
    },
    {
      "section_id": "sec_results",
      "paragraph_id": "p_res_5",
      "sentence_ids": ["s_res_5_2"],
      "role": "conflict"
    }
  ],
  
  "original_texts": {
    "s_met_4_1": "Protein expression was measured by Western blot.",
    "s_res_5_2": "We observed a 3.5-fold increase in mRNA levels."
  },
  
  "suggested_rewrites": [
    {
      "condition": "If Western blot is correct",
      "target_sentence": "s_res_5_2",
      "rewrite": "We observed a 3.5-fold increase in protein levels."
    },
    {
      "condition": "If qPCR is correct",
      "target_sentence": "s_met_4_1",
      "rewrite": "mRNA expression was measured by qPCR."
    }
  ],
  
  "rationale": "Western blot measures protein; qPCR measures mRNA. These cannot both be correct as written."
}
```

### Rubric Summary (from Assembler)

```json
{
  "rubric_scores": {
    "soundness": 6,
    "significance": 7,
    "clarity": 8,
    "reproducibility": 5
  },
  
  "acceptability_band": "major_revision",
  "acceptability_rationale": "Strong technical execution but methodology gaps and statistical concerns require revision."
}
```

---

## Agent Roster (5 + Meta)

### Agent 0: Parser (Non-LLM, Upstream)

Already exists. Produces the Indexed JSON with sentence-level IDs.

Not counted as a cognitive agent.

---

### Agent 1: Extractor (Mapper & Planner)

**Role:** Read the entire Indexed JSON once. Produce structured outputs for all downstream agents.

**Inputs:**
- Full Indexed JSON
- Document type
- Tier
- User intent (chips + free text)

**Outputs:**

1. **ArgumentMap** — structured representation of claims, evidence, methods, definitions
2. **ReviewPlan** — which sections matter, which tracks to emphasize, hotspots
3. **RAGSeeds** — search queries for Domain Agent

**This is the only agent that sees the full document.**

---

### Agent 2: Clarity Agent

**Role:** Surface readability, flow, grammar, and structure issues.

**Inputs:**
- Indexed JSON (full text, streamed in chunks)
- ArgumentMap slice (to preserve terminology)
- ReviewPlan directives

**Two-Pass Operation:**

| Pass | Scope | Checks |
|------|-------|--------|
| **Pass 1: Sentence-level** | Individual sentences | Grammar, passive voice, word choice, sentence length, jargon |
| **Pass 2: Block-level** | Paragraphs and sections | Transitions, flow, argument progression, paragraph structure, section coherence |

Same agent, explicit phases in prompt. The cognitive mode is the same (prose quality), but context window differs. If evals show interference between passes, split into `clarity_sentences` and `clarity_blocks` agents later.

**Outputs:**
- Clarity cards with `original_text` + `suggested_rewrite`
- Pass tagged on each card (`sentence_level` or `block_level`)

**Notes:**
- Streams immediately (doesn't wait for Extractor)
- Free rewrites allowed (low semantic risk)
- The principled exception to "compress then reason" — prose editing requires prose

**Tab:** CLARITY

---

### Agent 3: Rigor Agent

**Role:** Check internal correctness and consistency.

**Inputs:**
- ArgumentMap (skeleton)
- Sentence lookup access (fetch by ID)
- ReviewPlan (priority sections, hotspots)

**Text Window Policy:**

When fetching sentences for analysis, Rigor applies context-appropriate windowing:

| Context | Window | Rationale |
|---------|--------|-----------|
| Default | ±1 sentence | Sufficient for most claims |
| Methods | ±2-3 sentences | Procedures need fuller context |
| Results | Full paragraph | Data interpretation spans blocks |
| Statistics | Include linked table text | Numbers need their source |
| Cross-section | All linked nodes + ±1 each | Consistency checks need both ends |

This prevents hallucination from missing context and overreach from too much context.

**Checks:**
- Claim ↔ Evidence alignment
- Method ↔ Result consistency
- Definition ↔ Usage consistency
- Statistical sanity

**Outputs:**
- Rigor cards (single-sentence or cross-section)

**Rewrite Behavior:**
- Single-sentence issues: direct `suggested_rewrite`
- Cross-section issues: `suggested_rewrites` array with conditions
- Ambiguous issues: no rewrite, rationale only

**Notes:**
- V0: No tools, internal consistency only
- V1: Citation verification via Perplexity

**Tab:** RIGOR

---

### Agent 4: Domain Agent (RAG Orchestrator)

**Role:** External knowledge — novelty, positioning, field context.

**V0 Scope:** RAG for positioning only. NO citation verification.
**V1 Addition:** Citation verification engine.

**Inputs:**
- ArgumentMap (claims)
- RAGSeeds (from Extractor)
- Tier (controls search depth)

**Actions (V0):**
- Quick: Skip (no Domain)
- Standard: 1-3 Perplexity queries
- Deep: 3-5 Perplexity Pro queries + Go Deeper available

**What Domain finds:**
- Field positioning (how does this sit in the literature?)
- Related work (what's been done before?)
- Novelty assessment (is the claimed contribution real?)
- Field norms (what would experts expect?)

**Citation Verification Engine (V1 — NOT V0):**

| Step | Action |
|------|--------|
| 1 | Extract citation metadata from Indexed JSON (author, year, title) |
| 2 | Query Perplexity for each citation (or batched) |
| 3 | Compare what paper *claims* citation says vs. what it *actually* says |
| 4 | Flag: fabricated refs, misrepresented findings, inaccurate claims |

**Citation flags (V1):**
- `citation_not_found` — reference doesn't exist
- `citation_misrepresented` — paper says X, but source actually says Y
- `citation_outdated` — superseded by newer work
- `citation_tangential` — source doesn't support the claim it's attached to

**Outputs:**
- Domain cards (novelty concerns, positioning issues)
- DomainReport (field positioning summary for Adversary)

**Tab routing:**
- **V0:** All Domain cards → FIELD only (positioning, novelty, field context)
- **V1:** Citation-verification issues → RIGOR; all other Domain cards → FIELD

---

### Agent 5: Adversary Agent

**Role:** Reviewer 2. Attack the paper's argument, positioning, and strategy.

**Inputs:**
- ArgumentMap
- Rigor issues (from Agent 3)
- DomainReport (from Agent 4)
- Abstract + Introduction text

**Outputs:**
- Attack cards (weak points, vulnerability paths)
- Strategic recommendations (preemptive defenses)
- Bias profile (optional, at Deep tier)

**Notes:**
- Fed both internal findings (Rigor) and external context (Domain)
- Operates at strategic/global level, not line-by-line

**Tab:** FIELD

---

### Meta-Agent: Assembler

**Role:** Merge, deduplicate, calibrate, render.

**Note:** Assembler is deterministic — it uses rule-based logic, not an LLM prompt. The `assembler_consensus.md` prompt is used ONLY for the inner consensus-resolution LLM call when models disagree, not for the main assembly logic.

**Inputs:**
- All cards from all agents
- Chips (for filtering)
- Document type (for voice)
- Tier (for thresholds)

**Actions:**
1. Deduplicate overlapping issues
2. Cluster by topic/section
3. Assign final severity (blocking / major / minor / nit)
4. Assign confidence scores (consensus mode only — via LLM adjudicator)
5. Apply document-type voice to card text
6. Compute rubric scores

**Outputs:**
- Final card set for UI
- Rubric summary
- Acceptability band + rationale

---

## ArgumentMap Schema

```json
{
  "document_type": "scientific_manuscript",
  "title": "...",
  "abstract_summary": "2-3 sentence summary",
  
  "structure": {
    "sections": [
      {
        "id": "sec_methods",
        "name": "Methods",
        "paragraphs": ["p_met_1", "p_met_2", "..."]
      }
    ]
  },
  
  "claims": [
    {
      "id": "C1",
      "claim_text": "Our method improves accuracy by 20%",
      "sentence_ids": ["s_res_3_2"],
      "claim_type": "main | supporting | background",
      "evidence_links": ["E1", "E3"],
      "effect_size": {
        "value": "20%",
        "comparison": "vs baseline"
      },
      "red_flags": ["no_ablation", "single_study"]
    }
  ],
  
  "evidence": [
    {
      "id": "E1",
      "type": "experimental_data | simulation | theoretical | citation",
      "sentence_ids": ["s_res_4_1"],
      "data_availability": "public | on_request | not_stated",
      "citation_ref": "smith2023"
    }
  ],
  
  "methods": [
    {
      "id": "M1",
      "technique": "Western blot",
      "sentence_ids": ["s_met_4_1"],
      "supports_claims": ["C1", "C3"]
    }
  ],
  
  "definitions": [
    {
      "term": "HLF",
      "definition": "Human lung fibroblasts",
      "sentence_ids": ["s_met_1_1"],
      "usage_locations": ["s_res_2_1", "s_res_5_3"]
    }
  ],
  
  "statistics": [
    {
      "id": "STAT1",
      "text": "p < 0.05, N=500",
      "sentence_ids": ["s_res_6_2"],
      "values": {"p": 0.05, "n": 500}
    }
  ]
}
```

---

## ReviewPlan Schema

```json
{
  "priority_sections": ["sec_methods", "sec_results"],
  
  "hotspots": [
    {
      "location": "p_res_11",
      "reason": "Cluster selection by visual inspection"
    },
    {
      "location": "p_met_2", 
      "reason": "Placeholder citation [x]"
    }
  ],
  
  "track_emphasis": {
    "rigor": "high",
    "clarity": "medium",
    "domain": "high",
    "hostile": "high"
  },
  
  "user_focus_parsed": ["statistical methodology", "novelty claims"],
  
  "rag_seeds": [
    "kinase inhibitor contractility screen",
    "FLECS micropatterning platform",
    "fibrosis mechanobiology"
  ]
}
```

---

## Prompt Selector (Deterministic Routing)

**Not an LLM agent.** A deterministic function that selects prompt variants for each agent based on structured inputs.

### Why Not a Full Planner?

| Approach | Latency | Debuggability | Failure Modes |
|----------|---------|---------------|---------------|
| LLM Planner | +2-5s | Hard (why did it route this way?) | Misrouting cascades |
| Deterministic Selector | ~0ms | Easy (inspect the logic) | Predictable, testable |

LLM routers are warranted when:
- Agent set is large and heterogeneous
- User queries are unstructured and routing is hard

Neither applies here. Topology is fixed, doc types are known, and Extractor/Map provides structured signals.

### Prompt Library Structure

```
prompts/
├── clarity/
│   ├── clarity_base.md
│   ├── clarity_technical.md
│   └── clarity_legal.md
├── rigor/
│   ├── rigor_base.md
│   ├── rigor_methods_heavy.md
│   ├── rigor_theoretical.md
│   ├── rigor_clinical.md
│   └── rigor_grant.md
├── domain/
│   ├── domain_base.md
│   ├── domain_nature_tier.md
│   └── domain_legal.md
├── adversary/
│   ├── adversary_base.md
│   ├── adversary_reviewer2.md
│   ├── adversary_grant_panel.md
│   └── adversary_opposing_counsel.md
└── assembler/
    ├── assembler_base.md
    └── assembler_consensus.md
```

### Selection Logic

```python
def select_prompts(doc_type: str, tier: str, chips: list, review_plan: ReviewPlan) -> dict:
    """
    Deterministic prompt selection based on structured inputs.
    Returns dict mapping agent -> prompt path.
    
    tier: "quick" | "standard" | "deep"
    """
    prompts = {}
    
    # Clarity selection
    if doc_type == "legal_brief":
        prompts["clarity"] = "clarity_legal.md"
    elif review_plan.track_emphasis.get("clarity") == "high":
        prompts["clarity"] = "clarity_technical.md"
    else:
        prompts["clarity"] = "clarity_base.md"
    
    # Rigor selection
    if doc_type == "grant":
        prompts["rigor"] = "rigor_grant.md"
    elif "methodology" in chips:
        prompts["rigor"] = "rigor_methods_heavy.md"
    elif review_plan.map_characteristics.get("data_heavy"):
        prompts["rigor"] = "rigor_clinical.md"
    elif review_plan.map_characteristics.get("theoretical"):
        prompts["rigor"] = "rigor_theoretical.md"
    else:
        prompts["rigor"] = "rigor_base.md"
    
    # Domain selection (skipped at quick tier by orchestrator)
    if "nature-tier" in chips:
        prompts["domain"] = "domain_nature_tier.md"
    elif doc_type == "legal_brief":
        prompts["domain"] = "domain_legal.md"
    else:
        prompts["domain"] = "domain_base.md"
    
    # Adversary selection — suppressed at quick tier
    if tier == "quick":
        prompts["adversary"] = None  # Adversary skipped at quick tier
    elif doc_type == "grant":
        prompts["adversary"] = "adversary_grant_panel.md"
    elif doc_type == "legal_brief":
        prompts["adversary"] = "adversary_opposing_counsel.md"
    else:
        prompts["adversary"] = "adversary_reviewer2.md"
    
    return prompts
```

### Selector Inputs

| Input | Source | Used For |
|-------|--------|----------|
| `doc_type` | User selected or auto-detected | Primary routing key |
| `chips` | User selected | Focus area modifiers |
| `review_plan.track_emphasis` | Extractor output | Intensity adjustments |
| `review_plan.map_characteristics` | Extractor output | Content-based routing |

### Map Characteristics (Added to ReviewPlan)

Extractor flags structural characteristics that inform prompt selection:

```json
{
  "map_characteristics": {
    "methods_heavy": true,
    "data_heavy": false,
    "theoretical": false,
    "multi_study": false,
    "clinical": false,
    "has_code": false,
    "citation_density": "high"
  }
}
```

These are boolean/categorical flags, not free text — keeps selection logic simple.

---

## Pipeline Flow

```
Indexed JSON + User Inputs (doc_type, tier, chips, free_text)
         │
         ▼
    ┌──────────┐
    │ Extractor │──→ ArgumentMap + ReviewPlan + RAGSeeds
    └──────────┘
         │
         ▼
    ┌─────────────────┐
    │ Prompt Selector │──→ Selects prompt variants per agent
    │ (deterministic) │    based on doc_type, chips, map_characteristics
    └─────────────────┘
         │
    ┌────┴─────┬──────────┬────────────┐
    ▼          ▼          ▼            ▼
┌─────────┐ ┌───────┐ ┌────────┐ ┌───────────┐
│ Clarity │ │ Rigor │ │ Domain │ │ Adversary │
│ (full   │ │ (map+ │ │ (map+  │ │ (map+     │
│  text)  │ │ lookup│ │  RAG)  │ │  reports) │
│         │ │       │ │        │ │           │
│ Pass 1: │ │       │ │        │ │           │
│ sentence│ │       │ │        │ │           │
│ Pass 2: │ │       │ │        │ │           │
│ block   │ │       │ │        │ │           │
└────┬────┘ └───┬───┘ └───┬────┘ └─────┬─────┘
     │          │         │            │
     │          │         └──────┬─────┘
     │          │                │
     │          │    ┌───────────┘
     │          │    │ (Adversary receives Rigor + Domain outputs)
     │          │    │
     └────┬─────┴────┴────┐
          ▼               │
    ┌───────────┐         │
    │ Assembler │◄────────┘
    └─────┬─────┘
          ▼
    UI (CLARITY / RIGOR / FIELD)
```

**Execution order:**
1. Extractor runs (full doc → map)
2. Prompt Selector runs (deterministic, ~0ms)
3. Clarity starts streaming immediately with base prompt + full text. Once Extractor finishes, ArgumentMap term definitions are injected for consistency checking.
4. Rigor, Domain run in parallel after map ready
5. Adversary waits for Rigor + Domain outputs
6. Assembler collects incrementally

---

## Tier Matrix

| Capability | Quick | Standard | Deep |
|------------|-------|----------|------|
| **Extractor** | Lite (claims only) | Full | Maximal |
| **ReviewPlan** | Basic | Full | Full + hotspot detection |
| **Clarity** | Major issues only | Full | Full |
| **Rigor** | Major issues, no tools | Full | Expert (V1: + stats tools) |
| **Domain searches** | 0 | 1-3 queries | 3-5 queries + Go Deeper |
| **Adversary** | Skip | Light | Full + bias profile |
| **Consensus** | No | No | Optional (3× models) |
| **Latency** | ~30s | ~60s | ~120s+ |
| **Cost** | $ | $$ | $$$ |

**Tier value proposition:**
- **Quick** — "Fast polish before sharing this draft"
- **Standard** — "Prepare for peer review"
- **Deep** — "Stress-test before high-stakes submission"

---

## Consensus Mode (Deep Tier Only)

When enabled:

1. **Shared across models:** Extractor + Domain run once (frontier model)
2. **Per-model:** Rigor + Adversary run on 3 models (Claude, GPT, Gemini)
3. **Aggregation:** Assembler receives 3× cards, computes:
   - **Strong signal:** All 3 agree → high confidence
   - **Mixed signal:** 2/3 agree → medium confidence, note dissent
   - **Weak signal:** All disagree → show all perspectives

---

## Consensus Clustering (Assembler)

**Problem:** How does Assembler know if two models flagged the "same" issue?

Naïve string matching fails. Different models phrase issues differently even when detecting the same underlying problem.

**Solution: Three-stage hybrid clustering**

| Stage | Method | Coverage | Cost |
|-------|--------|----------|------|
| 1 | Structural anchor matching | ~80% | Free |
| 2 | Embedding similarity | ~15% | Pennies |
| 3 | LLM adjudicator | ~5% | 3-10 calls/doc |

### Stage 1: Structural Anchors (Deterministic)

Every issue card contains location metadata:

```json
{
  "locations": [{"section_id": "sec_results", "sentence_ids": ["s_res_5_2"]}],
  "claim_links": ["C3"],
  "method_links": ["M2"]
}
```

If two issues share:
- Same sentence ID(s), OR
- Same claim ID, OR
- Same method/evidence ID

→ Cluster them together. No LLM needed.

### Stage 2: Embedding Similarity

For partial anchor matches, compute embeddings of:
- `issue.title`
- `issue.message`

If cosine similarity > 0.80 → cluster together.

Cost: pennies (embedding API calls only).

### Stage 3: LLM Adjudicator (Surgical)

Only when Stage 1 + 2 are inconclusive:

**Input:**
- Issue A JSON
- Issue B JSON
- ArgumentMap slice
- Relevant text snippets

**Prompt:**
```
You are determining whether two reviewer comments refer to the same underlying issue.

Focus on:
- Same claim or assertion?
- Same methodological flaw?
- Same statistical or logical mismatch?
- Same evidence-based conflict?

Return JSON:
{
  "same_issue": true/false,
  "confidence": 0.0-1.0,
  "rationale": "..."
}
```

**Output:**
```json
{
  "same_issue": true,
  "confidence": 0.87,
  "rationale": "Both identify overclaiming in the effect size, though Model A focuses on the abstract while Model B focuses on results."
}
```

Expected: 3-10 adjudicator calls per document, even in full Consensus mode.

### Clustering Algorithm

```python
for issueA in model_a_issues:
    for issueB in model_b_issues + model_c_issues:
        if share_structural_anchor(issueA, issueB):
            cluster(issueA, issueB)
        elif embedding_similarity(issueA, issueB) > 0.80:
            cluster(issueA, issueB)
        else:
            result = adjudicate_with_llm(issueA, issueB)
            if result.same_issue:
                cluster(issueA, issueB)

# After clustering
merged_issues = deduplicate_and_merge(clusters)
```

### Consensus Resolver Agent (Optional)

For issues where clustering shows <60% agreement or contradictory severities:

**Input:**
- 3 model outputs for one issue cluster
- ArgumentMap slice
- DomainReport

**Output:**
- Reconciled verdict
- Confidence score
- Rationale

Only called on ~5-20% of clustered issues. Optional for V1 but improves tie-breaking.

---

## Tab Routing

| Agent | CLARITY | RIGOR | FIELD |
|-------|---------|-------|-------|
| Clarity | ✓ | | |
| Rigor | | ✓ | |
| Domain | | (V1 only) | ✓ |
| Adversary | | | ✓ |

**Note:** Domain → RIGOR only in V1 when citation verification is added.

---

## Cross-Section Issue Handling

**Problem:** Rigor operates on the compressed map, but rewrites need actual text. Some issues span multiple sentences across different sections.

**Solution:**

1. **Map nodes include sentence IDs** — every claim, evidence, method points to source locations
2. **Rigor detects inconsistency via map** — e.g., Method M2 technique ≠ Result R3 technique
3. **Rigor fetches all involved sentences** — multi-lookup from Indexed JSON
4. **Card includes multiple locations + original texts**
5. **Rewrite depends on ambiguity:**
   - Clear fix → single `suggested_rewrite`
   - Ambiguous → `suggested_rewrites` array with conditions
   - Author must decide → no rewrite, rationale only

**Issue type taxonomy:**

| Type | Sentences | Rewrite Approach |
|------|-----------|------------------|
| Single-sentence error | 1 | Direct rewrite |
| Cross-section inconsistency | 2+ | Conditional rewrites or none |
| Structural issue | N/A | Recommendation only |
| Logic gap (missing evidence) | 1 claim | Flag, suggest what to add |

---

## Sentence Lookup Infrastructure

The Indexed JSON is the source of truth.

**Operations:**
- `lookup(sentence_id)` → returns sentence text
- `lookup_many([sentence_ids])` → returns dict of texts
- `get_context(sentence_id, window=1)` → returns sentence + surrounding

**All agents can call lookup.** The map stays small; text is fetched on demand.

---

## Document-Type Profiles

Profiles control:
1. **Voice** — persona for card text (see 08-DOCUMENT-TYPE-PERSONAS.md)
2. **Track emphasis** — which agents matter most
3. **Strictness** — severity thresholds

```json
{
  "doc_type": "scientific_manuscript",
  "voice_profile": {
    "clarity": "copy_editor",
    "rigor": "grad_student_methodologist",
    "strategy": "hostile_reviewer_2"
  },
  "track_emphasis": {
    "rigor": "high",
    "clarity": "medium",
    "domain": "high",
    "hostile": "high"
  }
}
```

```json
{
  "doc_type": "legal_brief",
  "voice_profile": {
    "clarity": "court_clerk",
    "rigor": "skeptical_judge",
    "strategy": "opposing_counsel"
  },
  "track_emphasis": {
    "rigor": "high",
    "clarity": "medium",
    "domain": "medium",
    "hostile": "high"
  }
}
```

---

## User Input Handling

**Chips (structured):**
- Filter which cards surface
- Adjust severity thresholds
- Configure track emphasis

**Free text (unstructured):**
- Injected into agent prompts
- Weights attention toward user concerns
- Parsed into `user_focus_parsed` in ReviewPlan

**Example injection for Rigor Agent:**
```
USER FOCUS: The author is particularly concerned about statistical methodology.
Prioritize issues related to stats, p-values, sample sizes, and analytical rigor.
```

---

## Token Economics

Assuming 50-page paper ≈ 50k tokens:

| Component | Tokens |
|-----------|--------|
| Indexed JSON (full) | 50k |
| ArgumentMap | ~5-10k |
| ReviewPlan | ~1k |
| Clarity input (streamed) | 50k |
| Rigor input (map + lookups) | ~15k |
| Domain input (map + abstract) | ~12k |
| Adversary input (map + reports) | ~15k |
| **Total processed** | ~150k |

**vs. naive 7-agent × full doc:** 350k

**Savings:** ~60%

---

## Go Deeper (Deep Tier Add-on)

Per-issue deep dive when user requests more investigation.

**Triggers:** User clicks "Go Deeper" on a card.

**Flow:**
1. Domain Agent runs Perplexity Deep Research for that issue
2. Heavy model (Opus) receives:
   - The issue
   - Relevant ArgumentMap nodes
   - Deep Research results
3. Returns:
   - Expanded analysis
   - Additional sources
   - Confidence assessment

**Cost:** Billed per Go Deeper call. Hard cap per document.

---

## Summary

**5 cognitive agents + 1 meta-agent + deterministic routing:**

| # | Agent | Reads | Outputs |
|---|-------|-------|---------|
| 1 | Extractor | Full doc (once) | ArgumentMap + ReviewPlan + RAGSeeds |
| 2 | Clarity | Full doc (two passes) | Clarity cards (sentence + block level) |
| 3 | Rigor | Map + lookups | Rigor cards |
| 4 | Domain | Map + RAG | Domain cards + DomainReport |
| 5 | Adversary | Map + Rigor + Domain | Attack cards + strategic recs |
| M | Assembler | All cards | Final cards + rubric + acceptability |

**Plus:**
- **Prompt Selector** — deterministic function that picks prompt variants from library

**Key principles:**
- Two global passes: Extractor (reasoning), Clarity (editing)
- All other agents work on compressed map + targeted lookups
- Clarity runs two explicit phases: sentence-level then block-level
- Deterministic prompt selection, not LLM routing
- Prompt library enables doc-type and chip-based specialization
- Cross-section issues get multi-location cards with conditional rewrites
- Tiers control depth, not topology
- We're reviewers, not editors — users apply their own fixes