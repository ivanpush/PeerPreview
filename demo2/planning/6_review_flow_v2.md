# 06: Review Flow v2

## Overview

This document describes the end-to-end flow from document upload to rendered issue cards. It reflects the v2 agent architecture with:

- Two global passes (Extractor for reasoning, Clarity for editing)
- Deterministic Prompt Selector
- Sentence-level indexed JSON as source of truth
- Cross-section issue handling
- Tier-gated tool access

---

## Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 0: INPUT                                                              │
│                                                                             │
│   User uploads document                                                     │
│   User selects: doc_type, tier, chips                                       │
│   User enters: free_text concerns                                           │
│                                                                             │
│   ┌─────────────┐                                                           │
│   │   Parser    │ (non-LLM, upstream)                                       │
│   │             │                                                           │
│   │  PDF/DOCX   │──→ Indexed JSON (sentence-level IDs)                     │
│   └─────────────┘                                                           │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 1: EXTRACTION (Global Reasoning Pass)                                 │
│                                                                             │
│   ┌─────────────┐                                                           │
│   │  Extractor  │                                                           │
│   │             │                                                           │
│   │  Inputs:    │                                                           │
│   │  - Indexed JSON (full)                                                  │
│   │  - doc_type                                                             │
│   │  - tier                                                                 │
│   │  - chips + free_text                                                    │
│   │             │                                                           │
│   │  Outputs:   │                                                           │
│   │  - ArgumentMap                                                          │
│   │  - ReviewPlan                                                           │
│   │  - RAGSeeds                                                             │
│   └─────────────┘                                                           │
│                                                                             │
│   Tier variations:                                                          │
│   - Quick:    Lite map (claims only)                                        │
│   - Standard: Full map (claims, evidence, methods, definitions)             │
│   - Deep:     Maximal map (+ red flags, effect sizes)                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 2: PROMPT SELECTION (Deterministic)                                   │
│                                                                             │
│   ┌──────────────────┐                                                      │
│   │  Prompt Selector │ (~0ms, no LLM)                                       │
│   │                  │                                                      │
│   │  Inputs:         │                                                      │
│   │  - doc_type                                                             │
│   │  - chips                                                                │
│   │  - ReviewPlan.map_characteristics                                       │
│   │  - ReviewPlan.track_emphasis                                            │
│   │                  │                                                      │
│   │  Outputs:        │                                                      │
│   │  - clarity_prompt    (from prompts/clarity/)                            │
│   │  - rigor_prompt      (from prompts/rigor/)                              │
│   │  - domain_prompt     (from prompts/domain/)                             │
│   │  - adversary_prompt  (from prompts/adversary/)                          │
│   └──────────────────┘                                                      │
│                                                                             │
│   Selection logic examples:                                                 │
│   - doc_type=grant → rigor_grant.md, adversary_grant_panel.md               │
│   - chips=["methodology"] → rigor_methods_heavy.md                          │
│   - map_characteristics.theoretical=true → rigor_theoretical.md             │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 3: PARALLEL AGENT EXECUTION                                           │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │ CLARITY (Global Editing Pass)                          [STREAMS]    │   │
│   │                                                                     │   │
│   │ Inputs: Indexed JSON (full), ArgumentMap slice, ReviewPlan          │   │
│   │ Prompt: Selected clarity prompt                                     │   │
│   │                                                                     │   │
│   │ Pass 1: Sentence-level (grammar, passive voice, word choice)        │   │
│   │ Pass 2: Block-level (transitions, flow, paragraph structure)        │   │
│   │                                                                     │   │
│   │ Output: Clarity cards → CLARITY tab                                 │   │
│   │                                                                     │   │
│   │ Note: Can start streaming before Extractor completes                │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │ RIGOR                                                 [PARALLEL]    │   │
│   │                                                                     │   │
│   │ Inputs: ArgumentMap, sentence lookup access, ReviewPlan             │   │
│   │ Prompt: Selected rigor prompt                                       │   │
│   │                                                                     │   │
│   │ Note: In V0, Rigor does NOT receive DomainReport.                   │   │
│   │       It checks internal consistency only.                          │   │
│   │       (V1: citation verification will add DomainReport dependency)  │   │
│   │                                                                     │   │
│   │ Text Window Policy:                                                 │   │
│   │ - Default: ±1 sentence                                              │   │
│   │ - Methods: ±2-3 sentences                                           │   │
│   │ - Results: Full paragraph                                           │   │
│   │ - Statistics: Include linked table text                             │   │
│   │ - Cross-section: All linked nodes + ±1 each                         │   │
│   │                                                                     │   │
│   │ Checks:                                                             │   │
│   │ - Claim ↔ Evidence alignment                                        │   │
│   │ - Method ↔ Result consistency                                       │   │
│   │ - Definition ↔ Usage consistency                                    │   │
│   │ - Internal statistical consistency (p-values match narrative, N consistent) │   │
│   │                                                                     │   │
│   │ Output: Rigor cards                                                 │   │
│   │         → RIGOR tab                                                 │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │ DOMAIN (RAG for External Context)                     [PARALLEL]    │   │
│   │                                                                     │   │
│   │ Inputs: ArgumentMap (claims), RAGSeeds, tier                        │   │
│   │ Prompt: Selected domain prompt                                      │   │
│   │                                                                     │   │
│   │ V0 Scope: RAG for positioning and field context only.               │   │
│   │           NO citation verification (that's V1).                     │   │
│   │                                                                     │   │
│   │ Search depth (tier-gated):                                          │   │
│   │ - Quick: Skip (no Domain)                                           │   │
│   │ - Standard: 1-3 Perplexity queries                                  │   │
│   │ - Deep: 3-5 Perplexity Pro queries                                  │   │
│   │                                                                     │   │
│   │ What Domain finds:                                                  │   │
│   │ - Field positioning (how does this sit in the literature?)          │   │
│   │ - Related work (what's been done before?)                           │   │
│   │ - Novelty assessment (is the claimed contribution real?)            │   │
│   │ - Field norms (what would experts expect?)                          │   │
│   │                                                                     │   │
│   │ Output:                                                             │   │
│   │ - Domain cards → FIELD tab (V0)                                     │   │
│   │ - DomainReport → passed to Adversary only (V0)                      │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 4: ADVERSARY (Waits for Rigor + Domain)                               │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │ ADVERSARY                                                           │   │
│   │                                                                     │   │
│   │ Inputs:                                                             │   │
│   │ - ArgumentMap                                                       │   │
│   │ - Rigor issues (from Phase 3)                                       │   │
│   │ - DomainReport (from Phase 3)                                       │   │
│   │ - Abstract + Introduction text                                      │   │
│   │                                                                     │   │
│   │ Prompt: Selected adversary prompt                                   │   │
│   │                                                                     │   │
│   │ Tier behavior:                                                      │   │
│   │ - Quick: Skip entirely                                              │   │
│   │ - Standard: Light pass                                              │   │
│   │ - Deep: Full hostile review + bias profile                          │   │
│   │                                                                     │   │
│   │ Output:                                                             │   │
│   │ - Attack cards → FIELD tab                                       │   │
│   │ - Strategic recommendations                                         │   │
│   │ - Bias profile (Deep only)                                          │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 5: ASSEMBLY                                                           │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │ ASSEMBLER                                                           │   │
│   │                                                                     │   │
│   │ Inputs:                                                             │   │
│   │ - All cards from all agents                                         │   │
│   │ - chips (for filtering)                                             │   │
│   │ - doc_type (for voice)                                              │   │
│   │ - tier (for thresholds)                                             │   │
│   │                                                                     │   │
│   │ Actions:                                                            │   │
│   │ 1. Deduplicate overlapping issues                                   │   │
│   │ 2. Cluster by topic/section                                         │   │
│   │ 3. Assign final severity (blocking/major/minor/nit)                 │   │
│   │ 4. Assign confidence scores (consensus mode only)                   │   │
│   │ 5. Apply doc-type voice to card text                                │   │
│   │ 6. Compute rubric scores (soundness, significance, clarity, repro)  │   │
│   │ 7. Filter by chips if specified                                     │   │
│   │                                                                     │   │
│   │ Output:                                                             │   │
│   │ - Final card set for UI                                             │   │
│   │ - Rubric summary                                                    │   │
│   │ - Acceptability band + rationale                                    │   │
│   │                                                                     │   │
│   │ Note: Assembler is fully deterministic and incurs no model cost     │   │
│   │ except for optional LLM-based adjudication in Consensus Mode.       │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 6: RENDER TO UI                                                       │
│                                                                             │
│   Cards routed to tabs:                                                     │
│   - CLARITY ← Clarity cards                                                 │
│   - RIGOR   ← Rigor cards                                                   │
│   - FIELD   ← Adversary cards + Domain cards                                │
│                                                                             │
│   Note: In V1, Domain citation issues may route to RIGOR.                   │
│                                                                             │
│   Each card displays:                                                       │
│   - Title + severity badge                                                  │
│   - Message                                                                 │
│   - Location (section, paragraph)                                           │
│   - "Show diff" button → reveals original_text vs suggested_rewrite         │
│   - Rationale (expandable)                                                  │
│   - Go Deeper button (Deep tier, eligible issues only)                      │
│                                                                             │
│   Summary panel displays:                                                   │
│   - Rubric scores                                                           │
│   - Acceptability band                                                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Tier Behavior Matrix

| Phase | Component | Quick | Standard | Deep |
|-------|-----------|-------|----------|------|
| 1 | Extractor depth | Lite | Full | Maximal |
| 2 | Prompt Selector | ✓ | ✓ | ✓ |
| 3 | Clarity | Major only | Full (2 pass) | Full (2 pass) |
| 3 | Rigor | Major only | Full | Expert |
| 3 | Domain | Skip | 1-3 queries | 3-5 Pro queries |
| 4 | Adversary | Skip | Light | Full + bias profile |
| 5 | Assembler | Basic | Full | Full |
| — | Consensus | No | No | Optional |
| — | Go Deeper | No | No | Available |

---

## Timing Estimates

| Phase | Quick | Standard | Deep |
|-------|-------|----------|------|
| Parser | ~5s | ~5s | ~5s |
| Extractor | ~10s | ~20s | ~30s |
| Prompt Selector | ~0s | ~0s | ~0s |
| Clarity (parallel) | ~15s | ~25s | ~25s |
| Rigor (parallel) | ~10s | ~20s | ~35s |
| Domain (parallel) | — | ~10s | ~20s |
| Adversary (sequential) | — | ~10s | ~20s |
| Assembler | ~5s | ~10s | ~15s |
| **Total** | **~30s** | **~60s** | **~120s** |

Note: Clarity streams results as they're ready. User sees CLARITY tab populating while other agents run.

---

## Consensus Mode Flow (Deep + Toggle)

When consensus is enabled:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ CONSENSUS FLOW                                                              │
│                                                                             │
│ Phase 1-2: Run once (shared)                                                │
│   - Extractor (Opus) → ArgumentMap                                          │
│   - Prompt Selector → prompt variants                                       │
│   - Clarity (run once) → Clarity cards                                      │
│   - Domain (shared RAG) → DomainReport                                      │
│                                                                             │
│ Phase 3-4: Run per model (3×) — ONLY Rigor + Adversary                      │
│   ┌────────────────┐  ┌────────────────┐  ┌────────────────┐                │
│   │     Claude     │  │      GPT       │  │     Gemini     │                │
│   │                │  │                │  │                │                │
│   │ - Rigor        │  │ - Rigor        │  │ - Rigor        │                │
│   │ - Adversary    │  │ - Adversary    │  │ - Adversary    │                │
│   └───────┬────────┘  └───────┬────────┘  └───────┬────────┘                │
│           │                   │                   │                         │
│           └─────────┬─────────┴─────────┬─────────┘                         │
│                     ▼                   ▼                                   │
│             ┌───────────────────────────────────┐                           │
│             │      Consensus Aggregator         │                           │
│             │                                   │                           │
│             │ For each issue:                   │                           │
│             │ - 3/3 agree → Strong signal       │                           │
│             │ - 2/3 agree → Mixed, note dissent │                           │
│             │ - 0/3 agree → Show all 3 views    │                           │
│             │                                   │                           │
│             │ On disagreement:                  │                           │
│             │ - Flag as disputed                │                           │
│             │ - (V1: Auto-trigger issue-level   │                           │
│             │   RAG to attempt resolution)      │                           │
│             └───────────────────────────────────┘                           │
│                               │                                             │
│                               ▼                                             │
│                     Assembler (with confidence)                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Consensus adds:**
- Coverage (3 models catch different things)
- Calibrated confidence
- Disagreement flagging
- V1: Auto-resolution attempts via issue-level RAG

**What runs once (shared):** Extractor, Clarity, Domain
**What runs 3× (per model):** Rigor, Adversary

**Consensus costs:**
- ~3× Rigor + Adversary compute (but shared Extractor + Clarity + Domain)
- +$2-6 depending on doc length

---

## Consensus Clustering

**Problem:** How does Assembler know if two models flagged the "same" issue?

**Solution: Three-stage hybrid clustering**

> **Version breakdown:**
> - **V0:** Stage 1 only (structural anchors)
> - **V1:** Stage 1 + Stage 2 (embeddings, depending on cost budget)
> - **V2:** Stage 1 + Stage 2 + Stage 3 (LLM adjudicator)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ CONSENSUS CLUSTERING                                                        │
│                                                                             │
│ Stage 1: Structural Anchor Matching (~80% of cases)                         │
│ ─────────────────────────────────────────────────────                       │
│ If issues share: sentence_id OR claim_id OR method_id → cluster             │
│ Cost: Free (deterministic)                                                  │
│                                                                             │
│                               │                                             │
│                               ▼                                             │
│                                                                             │
│ Stage 2: Embedding Similarity (~15% of cases)                               │
│ ─────────────────────────────────────────────────────                       │
│ Compute embeddings of issue.title + issue.message                           │
│ If cosine similarity > 0.80 → cluster                                       │
│ Cost: Pennies (embedding API only)                                          │
│                                                                             │
│                               │                                             │
│                               ▼                                             │
│                                                                             │
│ Stage 3: LLM Adjudicator (~5% of cases)                                     │
│ ─────────────────────────────────────────────────────                       │
│ Surgical LLM call: "Are these the same underlying issue?"                   │
│ Input: Issue A, Issue B, ArgumentMap slice, text snippets                   │
│ Output: { same_issue: bool, confidence: float, rationale: string }          │
│ Cost: 3-10 calls per document                                               │
│                                                                             │
│                               │                                             │
│                               ▼                                             │
│                                                                             │
│ Clustered issues → Merge & compute consensus strength                       │
│ - 3/3 agree: Strong signal                                                  │
│ - 2/3 agree: Mixed signal, note dissent                                     │
│ - 0/3 agree: Disputed, show all perspectives                                │
│                                                                             │
│                               │                                             │
│                               ▼                                             │
│                                                                             │
│ Optional: Consensus Resolver Agent (for <60% agreement)                     │
│ ─────────────────────────────────────────────────────                       │
│ Input: 3 model outputs + ArgumentMap + DomainReport                         │
│ Output: Reconciled verdict + confidence + rationale                         │
│ Only called on ~5-20% of clustered issues                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Go Deeper Flow (Post-Review)

Available at Deep tier for eligible issues:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ GO DEEPER FLOW                                                              │
│                                                                             │
│ User clicks "Go Deeper" on an issue card                                    │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │ 1. Domain Agent runs Perplexity Deep Research                       │   │
│   │    - Query constructed from issue + relevant claims                 │   │
│   │    - Returns comprehensive research bundle                          │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                               │                                             │
│                               ▼                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │ 2. Heavy model (Opus) receives:                                     │   │
│   │    - The issue                                                      │   │
│   │    - Relevant ArgumentMap nodes                                     │   │
│   │    - Deep Research results                                          │   │
│   │    - Original text snippets                                         │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                               │                                             │
│                               ▼                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │ 3. Returns:                                                         │   │
│   │    - Expanded analysis                                              │   │
│   │    - Additional sources (with citations)                            │   │
│   │    - Confidence assessment                                          │   │
│   │    - Verdict (confirmed / refuted / inconclusive)                   │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                               │                                             │
│                               ▼                                             │
│   Card updates in-place with Go Deeper results                              │
│   "Go Deeper" button changes to "Expanded ✓"                                │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Eligible issues:**
- Domain/positioning issues (novelty, related work)
- Rigor issues involving external claims
- Adversary issues referencing field norms

**Not eligible:**
- Clarity issues (prose quality, not factual)
- Internal consistency issues (no external lookup helps)

**Cost:** Billed per Go Deeper call. Hard cap per document (e.g., 5 calls).

---

## Cross-Section Issue Handling

When Rigor detects inconsistencies across sections:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ CROSS-SECTION ISSUE FLOW                                                    │
│                                                                             │
│ 1. Rigor detects mismatch in ArgumentMap                                    │
│    - Method M2 (sec_methods) says "Western blot"                            │
│    - Result R3 (sec_results) implies "qPCR"                                 │
│                                                                             │
│ 2. Rigor fetches all involved sentences                                     │
│    - lookup("s_met_4_1") → "Protein expression was measured by Western..."  │
│    - lookup("s_res_5_2") → "We observed a 3.5-fold increase in mRNA..."     │
│                                                                             │
│ 3. Rigor determines rewrite approach                                        │
│    - Clear fix? → Single suggested_rewrite                                  │
│    - Ambiguous? → Conditional suggested_rewrites                            │
│    - Author must decide? → No rewrite, rationale only                       │
│                                                                             │
│ 4. Card output includes:                                                    │
│    - Multiple locations                                                     │
│    - All original_texts                                                     │
│    - Conditional rewrites (if applicable)                                   │
│    - Rationale explaining the conflict                                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Card structure for cross-section issues:**

```json
{
  "issue_type": "cross_section",
  "locations": [
    {"section_id": "sec_methods", "sentence_ids": ["s_met_4_1"], "role": "source"},
    {"section_id": "sec_results", "sentence_ids": ["s_res_5_2"], "role": "conflict"}
  ],
  "original_texts": {
    "s_met_4_1": "Protein expression was measured by Western blot.",
    "s_res_5_2": "We observed a 3.5-fold increase in mRNA levels."
  },
  "suggested_rewrites": [
    {"condition": "If Western blot is correct", "target": "s_res_5_2", "rewrite": "..."},
    {"condition": "If qPCR is correct", "target": "s_met_4_1", "rewrite": "..."}
  ]
}
```

---

## Sentence Lookup Infrastructure

All agents can fetch text from the Indexed JSON:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ SENTENCE LOOKUP                                                             │
│                                                                             │
│ Indexed JSON (source of truth)                                              │
│ ├── sections[]                                                              │
│ │   ├── paragraphs[]                                                        │
│ │   │   ├── sentences[]                                                     │
│ │   │   │   ├── id: "s_met_4_1"                                             │
│ │   │   │   ├── text: "Protein expression was measured by Western blot."   │
│ │   │   │   └── ...                                                         │
│                                                                             │
│ Operations:                                                                 │
│ - lookup(sentence_id) → sentence text                                       │
│ - lookup_many([ids]) → dict of texts                                        │
│ - get_context(id, window=1) → sentence + neighbors                          │
│                                                                             │
│ Usage:                                                                      │
│ - ArgumentMap references IDs, not text                                      │
│ - Agents fetch text when generating rewrites                                │
│ - Assembler ensures all cards have original_text populated                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Error Handling

| Error | Detection | Recovery |
|-------|-----------|----------|
| Extractor fails | No ArgumentMap produced | Retry once, then surface error to user |
| Agent times out | No response in 60s | Use partial results, flag incomplete |
| Perplexity fails | RAG returns error | Continue without RAG results, note limitation |
| Sentence lookup fails | ID not found | Flag issue as "location uncertain" |
| Consensus deadlock | 0/3 agree, RAG inconclusive | Show all 3 views, mark as "disputed" |

---

## Output Summary

**Final output to UI:**

```json
{
  "cards": [
    {
      "id": "...",
      "tab": "CLARITY | RIGOR | FIELD",
      "issue_type": "single_sentence | cross_section | structural",
      "title": "...",
      "message": "...",
      "severity": "blocking | major | minor | nit",
      "locations": [...],
      "original_texts": {...},
      "suggested_rewrite": "..." | null,
      "suggested_rewrites": [...] | null,
      "rationale": "...",
      "confidence": 0.0-1.0,
      "go_deeper_eligible": true | false,
      "consensus_status": "agreed | mixed | disputed" | null
    }
  ],
  
  "rubric": {
    "soundness": 1-10,
    "significance": 1-10,
    "clarity": 1-10,
    "reproducibility": 1-10
  },
  
  "acceptability": {
    "band": "accept | minor_revision | major_revision | reject",
    "rationale": "..."
  },
  
  "meta": {
    "tier": "quick | standard | deep",
    "consensus": true | false,
    "processing_time_ms": 45000,
    "token_usage": {...}
  }
}
```

---

## Summary

**6 phases:**

1. **Input** — Parser produces Indexed JSON
2. **Extraction** — Extractor builds ArgumentMap + ReviewPlan
3. **Prompt Selection** — Deterministic selection from prompt library
4. **Parallel Agents** — Clarity (full text), Rigor + Domain (map + lookups)
5. **Adversary** — Waits for Rigor + Domain, attacks the argument
6. **Assembly** — Dedupe, score, voice, render

**Key properties:**
- Two global passes (Extractor for reasoning, Clarity for editing)
- All other agents work on compressed map
- Sentence lookup for rewrites
- Cross-section issues handled with multi-location cards
- Tiers control depth, not topology
- Consensus is an optional multiplier at Deep tier
- Go Deeper is post-hoc expansion for eligible issues