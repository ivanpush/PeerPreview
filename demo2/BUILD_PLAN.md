# PeerPreview Demo2 - Build Plan

## Overview
Build a document review system with rubric-based AI critique. V0 uses 4 JSON fixtures (no parsing).

## Stage 1: Frontend Foundation ✅
1. **UploadScreen** (`/`) - Already have base, needs:
   - Small demo doc selector (top-left, unobtrusive)
   - Depth slider (Light/Medium/Heavy with costs)
   - Prompt chips
   - Type detection display with override
   - Start Review button

2. **ReviewScreen** (`/review/:sessionId`) - **EXISTS, DO NOT MODIFY**
   - Already has 3-pane viewer, issues, accept/dismiss
   - Just needs to fetch from new endpoints

3. **ExportModal** - Simple modal in ReviewScreen

## Stage 2: Backend API Structure
1. Core data models:
   - `ManuscriptObject` (canonical document representation)
   - `Issue` (with rubric codes A1-A6, B1-B4, C1-C4)
   - `ReviewPlan`, `UserIntent`

2. API endpoints:
   - `POST /api/intake` - Load fixture, detect type
   - `POST /api/run-review` - Execute review pipeline
   - `POST /api/decisions` - Save accept/dismiss
   - `POST /api/export` - Generate output file

## Stage 3: Review Pipeline (Python/FastAPI)
1. **Phase 1 - Global Understanding**:
   - Planning Agent → ReviewPlan
   - Global Map Agent → claims, terminology, section summaries

2. **Phase 2 - Local Reviews** (parallel):
   - Track A (Rigor) - per section
   - Track B1 (Clarity) - per paragraph
   - Track B2 (Flow) - multi-paragraph

3. **Phase 3 - Global** (Heavy only):
   - Track C (Hostile/Skeptic) - global reasoning only

## Stage 4: Integration & Testing
1. Connect frontend to backend
2. Test with 4 fixtures
3. Validate rubric enforcement
4. Cost estimation accuracy

## Key Constraints
- ManuscriptObject is single source of truth
- HTML is interaction only (not truth)
- Rubric codes ONLY (no free-form critique)
- Export matches input format
- Demo dropdown is temporary (V1 will have real upload)