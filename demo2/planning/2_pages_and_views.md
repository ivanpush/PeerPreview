PeerPreview: Pages & Views Specification (Updated V0 Architecture)

(Claude-Code friendly, minimal cognitive load)

View Map
/                           → Upload / Intake View
/review/:sessionId          → Reviewer View (ReviewScreen)
/(reviewer modal)           → Export Modal


Note:
The old “progress view” is removed for V0 — ReviewScreen shows a simple loading spinner while results are fetched.

View 1: Upload / Intake (/)
Purpose

The intake surface where the user:

Selects a demo document (V0 only — small, unobtrusive)

Sees detected type + document stats (from the fixture)

Chooses review depth

Optionally specifies instructions

Starts the review

V0 does not implement full file upload — but the UI is structured so real uploads can replace the demo dropdown seamlessly.

Layout (clean, low load)
┌───────────────────────────────────────────────────────────┐
│ PEERPREVIEW                                               │
├───────────────────────────────────────────────────────────┤

   Demo Document (V0 only)
   ┌────────────────────────────────────────────┐
   │  Select demo document…              ▼      │
   └────────────────────────────────────────────┘
   (Small, faded, top-left — out of the way)

   Detected: Academic Manuscript  [Change ▼]
   Format: PDF • Pages: 12 • Words: ~4,200

   Review Depth
   ○ Light      ● Medium      ○ Heavy
   ~$0.35         ~$0.85        ~$2.50

   Focus your review (optional)
   [Desk-reject] [Methods rigor] [Hostile] [Clarity]

   Additional instructions…
   ┌───────────────────────────────┐
   │                               │
   └───────────────────────────────┘

   Estimated cost: ~$0.85

                             [Start Review →]

└───────────────────────────────────────────────────────────┘

Design Notes for Claude
V0 Demo Selector (Small, unobtrusive)

Appears top-left, small font, light gray border

Label: “Demo document (V0)”

Dropdown options:

“Academic Manuscript (PDF)”

“Grant Proposal (DOCX)”

“Policy Brief (PDF)”

“LaTeX Manuscript (.tex)”

Preloads metadata + detected type

Real upload will replace this entire block in V1

Document Stats Block

Not framed like a giant card

Just a simple text row under the selector

Mirrors Google Docs simplicity:

Detected: Academic Manuscript  [Change]
Format: PDF • Pages: 12 • Words: 4,200

Depth Slider

Plain 3-option radio

Shows cost + quick description

Cleanest possible interaction model

Prompt Chips

Simple inline pills

Click = append phrase to textarea

Cost Estimate

Minimal text, no fancy UI

Start Review Button

Primary CTA

Sits bottom-right

On click → start session → navigate to /review/:sessionId

Functional Requirements

Selecting demo document loads fixture metadata

Show:

detected type

page count

word count

User may override type (dropdown)

Depth radio updates cost estimate

Prompt chips append to instructions

Validation:

60 pages = block and show message

On submit:

POST /api/review/start
→ { sessionId }


Navigate to /review/:sessionId

Submit API
POST /api/review/start
{
  "demoDocId": "manuscript_pdf",
  "depth": "medium",
  "userPrompt": "Focus on methods rigor",
  "overrideType": null
}

View 2: Reviewer View (/review/:sessionId)
Purpose

This is your existing ReviewScreen component
(we do not modify architecture or layout).

It handles:

Manuscript rendering

Issue listing

Accept/Dismiss

Rewrite modals

Figure panel

Undo banner

Export button

Loading Behavior

Before issues load, ReviewScreen shows your built-in spinner:

Loading manuscript…


No separate “progress screen" in V0.

View 3: Export Modal (inside ReviewScreen)
Purpose

Create same-format export from ReviewScreen's “Export” button.

Minimal fields

Original format (PDF/DOCX/LaTeX)

Summary of accepted/dismissed

Optional “Include Change Log” toggle

“Generate and Download” button

Backend
POST /api/review/:sessionId/export
→ returns file blob

API Endpoints
Method	Endpoint	Purpose
POST	/api/review/start	Start session
GET	/api/review/:id/manuscript	Returns documentObject
GET	/api/review/:id/issues	Returns Issues[]
POST	/api/review/:id/decisions	Save user decisions
POST	/api/review/:id/export	Download output file
Component Hierarchy (simplified)
App
 ├── UploadPage
 │    ├── DemoDocSelector (V0 only, small)
 │    ├── DocStats
 │    ├── TypeOverrideDropdown
 │    ├── DepthSelector
 │    ├── PromptChips
 │    ├── InstructionsInput
 │    └── StartReviewButton
 │
 ├── ReviewScreen (your existing component)
 │    ├── ManuscriptView
 │    ├── IssuesPanel
 │    ├── RewriteModal
 │    ├── OutlineModal
 │    ├── BiasedReviewModal
 │    ├── UndoBanner
 │    └── ExportModal (triggered from top-right)
 │
 └── ExportModal

Specifically Addressing Your Final Ask

“I want the V0 select doc to be small and out of the way, just a demo dropdown that stands in for future real uploads.”

✔️ Implemented
✔️ Minimal
✔️ Top-left
✔️ Clearly marked “Demo document (V0)”
✔️ Does not dominate the intake screen
✔️ Fully removable for V1 real upload integration

Everything else (review depth, instructions, chips, cost) remains identical.