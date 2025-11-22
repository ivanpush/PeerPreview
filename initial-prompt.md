Create a small set of canonical docs from this spec

Create the bare repo skeleton

Set up a build log

After that, you work off the smaller docs, not this wall of text.

Here’s a prompt you can paste to Claude Code (edit filenames if you want):

You’re my engineering copilot for a 2-week solo build.

I’m going to paste a huge architecture spec for a project called “Manuscript Review Assistant”. From that, I want you to do ONLY documentation and scaffolding — no full implementations yet.

GOAL FOR THIS PASS:
1. Create a minimal doc set inside the repo:
   - README.md  → short, investor/interviewer-facing overview + quickstart
   - docs/ARCHITECTURE.md → concise summary of the architecture (1–2 screens, NOT the whole giant spec)
   - docs/PHASES.md → my phase plan with checklists (use GitHub-style [ ] / [x] checkboxes)
   - docs/AGENTS.md → table listing each agent, its responsibility, inputs, outputs
   - docs/PROMPTS.md → where prompts live, how they’re structured (don’t repeat full prompt bodies)

2. Create the code skeleton, NO real logic:
   - backend/ and frontend/ directories as in the spec
   - Empty or stub Python modules/classes for the main components (DocumentBuilder, BaseAgent, ReviewOrchestrator, etc.)
   - A docs/ directory with the markdown files above.
   - A BUILD_LOG.md at repo root with today’s date and a single entry “Project scaffold created.”

Rules:
- Don’t re-dump my whole spec into ARCHITECTURE.md. Summarize ruthlessly.
- Keep each markdown file readable in < 2–3 screenfuls.
- In PHASES.md, keep my phase names but make the task lists scannable and realistic for a solo dev.
- All TODO-style items should be GitHub-checkbox lists (- [ ] …).
- Don’t implement any real parsing/agents yet — just stubs and function signatures.

Once you propose the file tree and the contents, I’ll copy it into my repo.
Now I’ll paste the spec:


Then paste the giant spec once.

That gives you a clean doc + code skeleton so you’re not dragging this 10-page spec around every time.

2. How to organize planning docs like a PM (inside the repo)

I’d structure it like this:

/README.md
/docs/
  ARCHITECTURE.md     ← high-level system picture
  PHASES.md           ← timeline + checklists
  AGENTS.md           ← each agent’s contract
  PROMPTS.md          ← where prompts live, conventions
  DESIGN_NOTES_v1.md  ← (optional) dump of your original giant spec
/BUILD_LOG.md         ← ongoing dev log


Roles:

README.md

2–3 paragraphs on what it does.

“How to run locally” in 5–10 lines.

That’s what interviewers and future you will skim.

ARCHITECTURE.md

One diagram (ASCII is fine) + bullet list:

Frontend

API layer

Parsing layer

Agent layer

Orchestrator

This is your “how the system hangs together” doc.

PHASES.md

Your Phase 0–5 plan, but shortened and with GitHub checkboxes.

This is your working plan, not a novel.

AGENTS.md

Table like:

Agent	Type	Inputs	Outputs	Track A/B	Notes

One row each for Abstract/Intro/Methods/Results/Discussion + CrossDoc + CitationPolice + FigureAgent.

PROMPTS.md

Where prompt files live (e.g. /backend/prompts/methods_reviewer.md).

A few rules: “All prompts return JSON with schema X”, “Track A/B combined”, etc.

Actual prompt bodies stay as separate .md files near the code.

DESIGN_NOTES_v1.md (optional)

Paste the giant spec there if you want it in-git without cluttering the “real” docs.

3. What to ask Claude Code to do every time after that

Once the doc set exists, your pattern with Claude Code is:

“For Phase 0, read docs/PHASES.md and docs/ARCHITECTURE.md. Implement only the items marked Phase 0 in backend/app/services/parser and wire the /upload endpoint. Update BUILD_LOG.md with what you did.”

You don’t need to feed the whole spec again. Just:

Context for this task:
- ARCHITECTURE.md
- PHASES.md (Phase 0 section)
- AGENTS.md (if relevant)

Task:
- Implement P0.4–P0.7.
- Keep function signatures aligned with the schemas in backend/app/schemas/.
- Update BUILD_LOG.md with a new dated entry listing what changed.


You’re basically treating Claude as a dev who reads your docs and then does one phase/cluster at a time.

4. Build logs: simple, cheap, super useful

Two low-friction options.

Option A: Single BUILD_LOG.md at repo root

Pattern:

# Build Log

## 2025-11-20
- [x] Scaffolded repo (frontend/backend structure)
- [x] Added docs/ARCHITECTURE.md, docs/PHASES.md, docs/AGENTS.md
- [x] Implemented /upload endpoint stub in FastAPI
- Notes:
  - PDF parsing not wired yet — just returns dummy ParsedDocument.
  - Next: hook up pymupdf4llm and section splitter.

## 2025-11-21
- [x] Wired PdfParser → pymupdf4llm
- [x] Implemented SectionSplitter.regex version
- [ ] LLM fallback for section splitting
- Notes:
  - Need to add tests for weird 2-column layouts.


You (or Claude) append a section per day or per major session.

Option B: Per-phase logs (logs/phase-1.md, etc.)

If you want more granularity:

/logs/
  phase-0-foundation.md
  phase-1-core-agents.md
  phase-2-crossdoc-figure-citation.md


But honestly, for 2 weeks solo, one BUILD_LOG.md is enough.

You can explicitly tell Claude:

“Any time you make code changes in this session, also update BUILD_LOG.md with a new ## YYYY-MM-DD entry summarizing what changed and which PHASE/Tasks were touched.”