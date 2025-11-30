Stage 1: Frontend Foundation --

UploadScreen (/) – minimalist

File drop for user uploads (not fully wired yet in V0)

Demo doc selector (small, unobtrusive)

“Continue” button

No depth slider, chips, or type controls here

ReviewSetupScreen (/setup/:sessionId) – soft parse & intent

Shows:

detected doc type (with override selector)

title (from ManuscriptObject) if available

Controls:

Depth slider (Light / Standard / Heavy + cost hints)

Prompt chips

Free-form custom instructions

“Run Review” button → calls /api/run-review

ReviewScreen (/review/:sessionId) – EXISTS, DO NOT MODIFY

Already has 3-pane viewer, issues, accept/dismiss, etc.

It should just receive:

{
  manuscript: ManuscriptObject,
  issues: Issue[]
}


We only change how data is fetched (from new backend endpoints).

ExportModal

Simple modal within ReviewScreen to trigger /api/export.

Stage 2: Backend API Structure

Core data models (Python):

ManuscriptObject (canonical document representation)

Issue (rubric-coded A1–A6, B1–B4, C1–C4)

UserIntent (depth, chips, custom prompt)

ReviewPlan (tracks, priorities, budget, tone)

Backend location & tech

Create in: /demo2/backend/

Use Python 3.11 + FastAPI

API endpoints

POST /api/intake

Input: { fixtureId } (V0) or upload reference

Output: { manuscript: ManuscriptObject, type_guess: DocumentType }

Used by ReviewSetupScreen

POST /api/run-review

Input: { manuscript: ManuscriptObject, user_intent: UserIntent }

Runs full review pipeline (Stage 3)

Output: { manuscript: ManuscriptObject, issues: Issue[] }

Used by ReviewScreen

POST /api/decisions

Input: issue accept/dismiss decisions

For now, can be a no-op or log-only

POST /api/export

Input: { manuscript, issues, decisions }

Output: file/blob handle (V0 can stub this)

Stage 3: Review Pipeline (Python/FastAPI)
Phase 1 – Global Understanding

Planning Agent

Input: ManuscriptObject + UserIntent

Output: ReviewPlan (tracks_to_run, tone, budgets, concurrency)

Global Map Agent

Input: full document

Output:

claims list

terminology/acronym map

section summaries

argument/narrative map

early hostile sketch (coarse Reviewer 2)

Phase 2 – Local Reviews (parallel)

All use the global map & plan.

Track A (Rigor, per section)

Check A1–A6 issues:

Claim-evidence mismatch

Contradictions

Stats validity

Missing methods details

Cross-section disagreements (local hints; heavy consistency is Phase 3)

Track B1 (Clarity, per paragraph)

Check B1–B4:

Ambiguity

Cohesion breaks

Undefined terms

Tone that undermines professionalism

Provide paragraph-level rewrites for diff

Track B2 (Flow, multi-paragraph blocks)

Operate on 2–6 paragraph windows

Improve transitions, remove redundancy, suggest merge/split/reorder

Optional combined rewrites

Note: Track C does not run here.

Phase 3 – Global (Heavy only)

Track C (Hostile / Skeptic, global only)

Runs once over:

full manuscript

global map

early hostile sketch from Phase 1

all A/B issues from Phase 2

Produces:

cross-section consistency issues

overclaiming & missing limitations

prioritized global critique

Stage 4: Integration & Testing

Connect frontend → backend:

UploadScreen → /api/intake (via ReviewSetup)

ReviewSetupScreen → /api/run-review

ReviewScreen → /api/decisions, /api/export (stub OK for V0)

Use 4 fixtures, stored at:

/demo2/frontend/public/fixtures/

ManuscriptObject should match what ReviewScreen already expects

Validate:

rubric codes only (A/B/C codes enforced)

issues tie to specific paragraphs/sentences

cost estimates derived from depth + doc size

Confirm:

ManuscriptObject is canonical

HTML is not source-of-truth

Export preserves original structure (V0 can be simplified)