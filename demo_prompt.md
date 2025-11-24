⭐ FULL UPDATED PROMPT TO CLAUDE — Demo D1 (with correct rewrite semantics + figures)

Paste everything below into Claude Code.

You are building Demo D1 for a scientific manuscript review product.

This is a static, frontend-only prototype that demonstrates the full UX flow:

fake PDF upload

fake “processing”

manuscript view with sections/paragraphs

issues panel (Track A & Track B)

three rewrite types with correct behavior

figures panel with tabs and captions

There is no backend, no PDF parsing, and no LLM calls in Demo D1.

Everything is driven by static JSON files.

Focus on:

clean structure

correct behavior for the three rewrite types

preserving paragraph metadata when applying rewrites

a product-quality UX

📁 1. PROJECT STRUCTURE

Create this structure under project/demo/frontend-d1/:

project/
  demo/
    frontend-d1/
      src/
        pages/
          UploadScreen.jsx
          ProcessScreen.jsx
          ReviewScreen.jsx
        components/
          ManuscriptView.jsx
          IssuesPanel.jsx
          RewriteModal.jsx        // Type 1 paragraph rewrite
          OutlineModal.jsx        // Type 2 section outline / condensed rewrite
          UndoBanner.jsx
          FiguresPanel.jsx
          FigureTabs.jsx
          FigureCaptionBox.jsx
        context/
          ManuscriptContext.jsx
        utils/
          mockLoader.js
      public/
        static/
          manuscript_demo.json
          issues_demo.json
      package.json
      README.md


Use React + TailwindCSS.
The demo must run with:

cd project/demo/frontend-d1
npm install
npm start

📄 2. STATIC INPUT FILES

Demo D1 loads two static JSON files from public/static/:

A. manuscript_demo.json

Represents the fully indexed manuscript as semantic units.
Important: metadata is separate from text so rewrites don’t lose citations / fig refs.

Schema:

{
  "title": "Example Manuscript Title",
  "abstract": "Abstract text...",
  "sections": [
    {
      "section_id": "sec_intro",
      "heading": "Introduction",
      "paragraphs": ["p1", "p2", "p3"]
    },
    {
      "section_id": "sec_results",
      "heading": "Results",
      "paragraphs": ["p4", "p5"]
    }
  ],
  "paragraphs": [
    {
      "paragraph_id": "p1",
      "section_id": "sec_intro",
      "text": "Full paragraph text for p1...",
      "metadata": {
        "citations": ["[1]", "[2]"],
        "fig_refs": [],
        "sources": [],
        "notes": []
      }
    },
    {
      "paragraph_id": "p2",
      "section_id": "sec_intro",
      "text": "Full paragraph text for p2...",
      "metadata": {
        "citations": [],
        "fig_refs": ["fig1"],
        "sources": [],
        "notes": []
      }
    }
  ],
  "figures": [
    {
      "figure_id": "fig1",
      "label": "Figure 1",
      "caption": "Figure 1. Experimental workflow diagram...",
      "mentions": ["p2", "p4"],
      "page": 5
    }
  ],
  "references": "Optional unparsed references block"
}


Key points:

Every paragraph has:

paragraph_id

section_id

text

metadata (citations, fig refs, etc.)

When applying a rewrite, only text changes, metadata stays intact.

B. issues_demo.json

Represents static review issues from Track A / Track B / aggregator.

We support three rewrite-related issue types:

paragraph_rewrite → Type 1 — full paragraph rewrite (mergeable)

section_outline → Type 2 — outline / condensed rewrite (advisory, not mergeable)

global_strategy → Type 3 — high-level strategy (commentary only)

Example:

[
  {
    "id": "A1",
    "track": "A",
    "issue_type": "paragraph_rewrite",
    "severity": "major",
    "message": "The description of the control group is ambiguous.",
    "paragraph_id": "p4",
    "section_id": "sec_results"
  },
  {
    "id": "B3",
    "track": "B",
    "issue_type": "paragraph_rewrite",
    "severity": "minor",
    "message": "This paragraph is overly complex and could be simplified.",
    "paragraph_id": "p2",
    "section_id": "sec_intro"
  },
  {
    "id": "B5",
    "track": "B",
    "issue_type": "section_outline",
    "severity": "minor",
    "message": "The Introduction pacing is slow; consider restructuring.",
    "section_id": "sec_intro",
    "outline_suggestion": [
      "1. One concise paragraph of background context.",
      "2. One paragraph defining the specific gap in knowledge.",
      "3. One paragraph stating your approach and key result.",
      "4. One paragraph summarizing broader implications."
    ]
  },
  {
    "id": "C1",
    "track": "B",
    "issue_type": "global_strategy",
    "severity": "minor",
    "message": "Overall, the manuscript could be shortened by ~20% by trimming repetitive background in the Introduction and combining overlapping Results subsections."
  }
]


Later, this schema can also attach figure_id if needed (not required for Demo D1).

🧩 3. SCREENS & FLOW
Screen 1 — UploadScreen.jsx

Purpose: fake PDF upload.

UI:

Drag-and-drop area or file input

Show selected filename

“Parse File” button

Behavior:

Store filename locally

Do not parse file contents

On “Parse File” click → navigate to ProcessScreen

Screen 2 — ProcessScreen.jsx

Purpose: fake processing step.

On mount:

Fetch /static/manuscript_demo.json

Fetch /static/issues_demo.json

Store both in ManuscriptContext

Show a spinner or “Processing…” for ~1–2 seconds

Then display “Continue to Review” button

On click → navigate to ReviewScreen

No actual parsing or model calls.

Screen 3 — ReviewScreen.jsx (Main UI)

Layout:

---------------------------------------------------------
| ManuscriptView                  |     IssuesPanel      |
| (scrollable left side)          |  (right side tabs)   |
---------------------------------------------------------
|                FiguresPanel (tabs + caption)          |
---------------------------------------------------------

ManuscriptView.jsx

Show:

Title

Abstract

Sections (heading + paragraphs)

Each paragraph rendered in a container with id={paragraph_id}

When an issue referencing a paragraph is clicked:

Smooth scroll to that paragraph

Apply a highlight class (e.g., border or background)

IssuesPanel.jsx

Show issues with filters: All / Track A / Track B

Each issue shows:

Track label

Severity chip

Message

Behavior depends on issue_type:

paragraph_rewrite:

Show “Rewrite” button (enabled)

On click:

Scroll/highlight paragraph

Open RewriteModal for that paragraph

section_outline:

Show “View Outline” button

On click:

Scroll/highlight section heading

Open OutlineModal (advisory only, no replace)

global_strategy:

No action button

Just display in list as high-level comment

Rewrite button must only appear for paragraph_rewrite issues.

✍️ 4. REWRITE SEMANTICS (THIS IS IMPORTANT)

We have three rewrite types, and they must behave differently:

✅ Type 1 — Paragraph Rewrite (mergeable)

issue_type: "paragraph_rewrite"

Meaning:

Full alternative version of a single paragraph (same meaning, clearer wording)

Only case where an “Apply Replace” action is allowed

RewriteModal.jsx:

Modal contents:

Original paragraph (read-only block)

Proposed rewrite (editable <textarea>)

In Demo D1, this can be a static, manually written “better” paragraph

Buttons:

“Apply Replace”

“Cancel”

On “Apply Replace”:

Update the manuscript in context by changing only:

paragraph.text


Keep:

paragraph_id

section_id

metadata (citations, fig_refs, sources, etc.)

Show UndoBanner to allow a one-step revert.

This simulates:

“We only merge complete, safe, localized rewrites, and we never lose sources or citations because they live in metadata, not text.”

❌ Type 2 — Section Outline / Condensed Rewrite (not mergeable)

issue_type: "section_outline"

Meaning:

Advisory suggestion to restructure or tighten pacing in a section

Not safe to auto-merge (would drop detail, citations, etc.)

OutlineModal.jsx:

Shows:

Section heading and a short excerpt (e.g., first paragraph)

The outline_suggestion list from the issue JSON

Text note: “This is a suggested outline; it does not automatically modify the manuscript.”

Buttons:

“Close”

(Optional) “Mark as noted” but no actual state persistence needed for Demo D1

Important:

No “Apply Replace” button here.

No changes to manuscript_demo state.

No Undo.

We treat this as editorial advice, not content replacement.

🚫 Type 3 — Global Rewrite Strategy (no replace)

issue_type: "global_strategy"

Meaning:

Global comments on length, tone, redundancy, etc.

Never invokes rewrite modals.

Never changes manuscript JSON.

Behavior:

Only appears in IssuesPanel.

Clicking it may highlight nothing or the entire document header, but no modal, no rewrite action.

🔒 Rewrite button behavior summary

Rewrite button is only shown for paragraph_rewrite.

For section_outline, show “View Outline”.

For global_strategy, show no action button.

This avoids “merging incomplete rewrites” and keeps the UX sane.

⏪ 5. Undo Support (Type 1 only)

UndoBanner.jsx:

Appears after applying a Type 1 rewrite.

Message: “Paragraph updated. [Undo]”

On click:

Restore previous text for that paragraph from a cached lastRewrite object in context.

Clear the banner.

Single-step undo only (no version history).

🖼 6. FIGURES PANEL

FiguresPanel.jsx:

Renders below ManuscriptView (left pane full width).

Layout:

[FigureTabs  (scrollable horizontally)]
[FigureCaptionBox  (caption of selected figure)]

FigureTabs.jsx:

One tab per figure in manuscript.figures.

Tab label: figure.label (e.g., “Figure 1”, “Figure 2”).

Horizontally scrollable with overflow-x: auto.

Clicking a tab sets activeFigureId.

Selected tab is visually highlighted.

FigureCaptionBox.jsx:

Shows the caption of the currently selected figure.

Simple text box, no images.

Optional (nice-to-have):

If an issue references a figure_id (not required in D1 schema, but allowed):

Clicking that issue should select the relevant figure tab and briefly highlight the caption box.

🧠 7. MANUSCRIPT CONTEXT

ManuscriptContext.jsx:

Holds:

manuscript object (from manuscript_demo.json)

issues array (from issues_demo.json)

Methods:

updateParagraph(paragraphId, newText) — for Type 1 rewrites

undoLastRewrite() — uses stored { paragraphId, previousText }

setLastRewrite(info) — internal helper

Keep state minimal but clear.

⛔ 8. EXPLICIT NON-GOALS (DO NOT IMPLEMENT)

To keep Demo D1 focused and shippable:

No backend.

No LLM calls.

No real PDF parsing.

No real document export.

No images / figure rendering beyond captions.

No tables panel.

No diff viewer.

No multi-paragraph or cross-section rewrites.

No automatic application of section outlines or global strategies.

This is purely a static, front-end UX demo.

🎯 9. SUCCESS CRITERIA

Demo D1 is successful if:

I can:

Upload a fake PDF → see filename.

Click “Parse File” → see “Processing…”.

Click “Continue to Review” → see full manuscript view.

I see:

Issues list with Track A/B filters.

Different behavior for:

paragraph_rewrite (Rewrite button → RewriteModal → Apply → Undo)

section_outline (View Outline → OutlineModal, advisory only)

global_strategy (comment only).

Figures panel with tabs + captions.

Rewrites:

Only apply to paragraph text.

Never change paragraph metadata.

Support one-step undo.

Everything must feel like a real app, even though it’s driven entirely by static JSON.

✔ FINAL INSTRUCTION

Implement the full scaffold and components as described.
Ensure it runs with:

cd project/demo/frontend-d1
npm install
npm start


Provide:

All .jsx components

manuscript_demo.json and issues_demo.json examples

A short README.md explaining how to run Demo D1


Make the appearance reflect perplexities dark mode if possible - and consider what you've already built in the actual frontend of the project


also-

Yeah, that’s a legit Track C, and it’s spicy in exactly the right way if you frame it as **“biased reviewer personas / field orthodoxy view”**, not “this is the truth.”

Let’s nail down what Track C *is* and how it plugs into what you already have.

---

## 0. What Track C actually does

**Goal:**
Simulate a **realistic but biased reviewer** whose worldview is shaped by:

* what’s been funded (big grants, consortia)
* what’s been cited heavily in the last 5–10 years
* which methods / narratives are “canon”
* which PIs / labs dominate the narrative

Then have that reviewer:

1. Give a **3–4 sentence summary** of what the authors tried to do.
2. Give their **overall take** colored by their bias.
3. Go **line-by-line / section-by-section** raising concerns that are *plausible given that bias*.

This is explicitly *not* an objective review. It’s:

> “Here’s how a certain entrenched camp might come after you.”

---

## 1. Data pipeline concept (how it *would* work with Perplexity / web)

For the assignment you won’t actually wire Perplexity, but you should be able to describe it like this:

### Step 1 — Extract field + keywords from manuscript

From your manuscript JSON:

* Title
* Intro paragraphs (`p_intro_*`)
* Methods keywords

Derive a **topic profile**, e.g.:

```json
{
  "field": "mechanobiology, contractility, kinase inhibitors, high-throughput phenotypic screening",
  "key_terms": [
    "mechanobiology",
    "cell contractility",
    "kinase inhibitor library",
    "high-throughput screening",
    "phenotypic screening",
    "myofibroblast activation",
    "fibrosis",
    "airway smooth muscle",
    "hepatic stellate cells"
  ],
  "disease_areas": ["fibrosis", "asthma", "bladder dysfunction"],
  "method_keywords": ["FLECS", "single-cell force", "micropatterns"]
}
```

### Step 2 — External “orthodoxy” search (conceptual, using Perplexity/web)

You’d call something like Perplexity / web search with prompts:

* “Most cited papers on [mechanobiology + cell contractility] in last 10 years”
* “Major labs and PIs working on [phenotypic screening + fibrosis]”
* “Large NIH grants (U01, P50, etc.) related to [mechanobiology / contractility]”
* “Common criticisms or limitations discussed in reviews of [high-throughput phenotypic screening]”

You **don’t actually name real people in the product** (for legal / defamation risk), but you *do* extract:

* methodological orthodoxy
* preferred endpoints / assays
* favored model systems
* standard narratives
* hot buzzwords

### Step 3 — Build a **Bias Profile**

From that, you generate a **Bias Profile** object:

```json
{
  "bias_profile_id": "bp_mech_01",
  "label": "Canonical mechanobiology / fibrosis camp",
  "core_beliefs": [
    "Mechanobiology readouts must be tied to molecular mechanisms (omics, pathway mapping).",
    "Translatability requires in vivo validation or at least organoid / 3D tissue models.",
    "Generic kinase libraries are less valuable than disease-specific pathway targeting.",
    "Phenotypic screens are exploratory and should be tightly linked to clear MoAs."
  ],
  "sensitive_points": [
    "Claims of selectivity without mechanistic or functional validation.",
    "Over-generalization of cell-type-specific findings.",
    "Underpowered or noisy assays being used to claim ‘atlas’ or ‘comprehensive’ insights."
  ]
}
```

This is what you feed into the LLM to define the Track C persona.

---

## 2. What Track C actually outputs

Track C is **another reviewer track**, parallel to A (local technical issues) and B (global structure), but with a fixed bias.

### Output structure (conceptual JSON)

```json
{
  "manuscript_id": "2025.01.11.632556v2",
  "bias_profile_id": "bp_mech_01",
  "review_summary": {
    "author_intent_summary": "3–4 sentences: what the authors are trying to do.",
    "biased_overall_view": "3–6 sentences from the biased reviewer’s perspective."
  },
  "issues": [
    {
      "issue_id": "C-001",
      "track": "C",
      "bias_profile_id": "bp_mech_01",
      "section_id": "sec_intro",
      "paragraph_id": "p_intro_4",
      "sentence_indices": [0,1],
      "issue_type": "overclaim / framing",
      "severity": "high",
      "text_span_quote": "To address this, we conducted the first ever high-throughput cell contractility screen...",
      "comment": "From the canonical view, the claim of 'first ever' feels unsubstantiated unless the authors more explicitly contrast their screen with prior phenotypic or mechanobiology screens...",
      "suggested_action": "Clarify novelty claim with specific prior art comparison or soften language.",
      "rewrite_type": "paragraph",
      "proposed_rewrite": null  // Track C can suggest but doesn't have to rewrite
    }
  ],
  "full_narrative_review": "A few paragraphs that read like a real reviewer report."
}
```

So Track C has both:

* **structured issues** anchored to paragraph_ids (so UI can highlight), and
* a **free-form reviewer letter**.

---

## 3. Prompting / behavior for Track C

You want this behavior:

* It **understands** the paper fairly.
* Then **deliberately looks for flaws** consistent with the chosen bias.
* It stays **technically plausible**, not just dunking randomly.

Skeleton system prompt for Track C:

> You are simulating a *biased but technically competent peer reviewer* for a mechanobiology manuscript.
>
> You have a **bias profile**: [insert core beliefs + sensitive points].
>
> Step 1: Briefly restate what the authors are trying to do (3–4 sentences).
> Step 2: In 3–6 sentences, give your overall view **from this biased perspective**. Be explicit that your expectations are shaped by the prevailing views in the field.
> Step 3: Go section by section. For each section:
>
> * Identify claims, methods, or interpretations that would trigger skepticism in this reviewer persona.
> * For each issue, link it to a specific paragraph_id and optionally sentence indices.
> * For each issue, specify:
>
>   * type (e.g., overclaim, underpowered evidence, missing comparison, method skepticism)
>   * severity (minor, moderate, major, fatal)
>   * a short comment (~1–3 sentences)
>     Step 4: End with a short “Reviewer #2 style” summary paragraph: e.g., “While the topic is interesting, in its current state the manuscript falls short of…”
>
> Constraints:
>
> * Do not name real individuals or labs.
> * Frame the bias as “dominant views in the field” or “typical expectations in the literature,” not as attacks on specific people.
> * Remain technically grounded and plausible; do not invent nonexistent studies or methods.

---

## 4. How it fits with Track A / B in the UI

In the frontend you could have:

* **Track A:** Local issues (clarity, stats, methods)
* **Track B:** Global story / structure / pacing
* **Track C:** “Skeptical field reviewer” (tagged as *biased / persona-based*)

UI-wise:

* A little warning label:

  > “Track C simulates how a particular type of reviewer might push back, based on dominant narratives and incentives in the field. This is intentionally biased and should be treated as a stress-test, not objective truth.”
* A separate tab or section for Track C review.
* Issues still clickable in the manuscript (because they use the same paragraph_ids).

For the 30-hour demo: you don’t need the full Perplexity / grants integration. You can:

* **Hard-code** a Bias Profile for this paper (canonical mechanobiology / fibrosis person).
* Have a **Track C tab** that loads static JSON + a narrative review.
* Explain verbally how, in v1, you’d populate the bias profile with live search over:

  * PubMed / OpenAlex for top-cited papers
  * NIH Reporter / grants APIs for funding trends
  * Perplexity for synthesis of “standard expectations in [X] field”

---

## 5. What I’d do *right now* for your assignment

For this paper specifically:

1. **Define one Bias Profile**:

   * Dominant mechanobiology / fibrosis orthodoxy:

     * cares a lot about mechanistic depth (omics, signaling)
     * skeptical of function-first platforms without in vivo / organoid validation
     * sensitive to claims of “atlas” and “first ever” without big-consortium-level depth

2. **Generate one full Track C review JSON** for this manuscript:

   * 3–4 sentence author-intent summary
   * 1 biased overall-assessment paragraph
   * 6–12 structured issues mapped to paragraph_ids
   * 1 closing “Reviewer 2” style paragraph

3. **Surface it in the UI** as:

   * A third tab: “Biased Reviewer Persona (Track C)”
   * Left: frozen manuscript
   * Right: biased issues + narrative

also:

refine spolits the upload and siaplay manuscript inside viewer where it is ediable and "Process" that actaully runs the process and displays the issues. then it is no longer editable. what do u think? how should v0 go, remember A, B and now C all havedisitnct paths. add a prompt to claude code to build this correctly including where jsons to use and where to get them for these. the issues should be dissimissible and un-dississed



End of prompt.
