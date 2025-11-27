# PeerPreview Demo2 - Build Log

## Session 1: Project Setup & Planning
- Read project specs (1_proj_overview.md, 2_pages_and_views, 3_agent_arch.md)
- Created BUILD_PLAN.md with 4-stage approach
- Identified ReviewScreen exists and must not be modified
- Next: Clarifying questions before starting Stage 1

## Session 2: Requirements Clarified
- Modify existing UploadScreen for minimal upload + demo
- Create NEW ReviewSetupScreen for soft parse and user inputs
- Fixtures in `/demo2/frontend-d2/public/fixtures/` (corrected path)
- Backend in `/demo2/backend/` with Python 3.11 + FastAPI
- Backend must match ReviewScreen.tsx format exactly
- Changed nomenclature: manuscriptObject → documentObject
- Build order: Fixtures → Upload/Setup UI → Backend API → Agents → Connect

### Stage 1: Fixtures (COMPLETED)
- Created 4 JSON fixtures in `/demo2/frontend-d2/public/fixtures/`:
  - manuscript_pdf.json (existing academic paper - reformatted to match ReviewScreen)
  - grant_docx.json (NIH-style grant proposal - reformatted)
  - policy_brief_pdf.json (grid modernization policy - reformatted)
  - latex_manuscript.json (quantum physics paper - reformatted)
- All fixtures now use sections/paragraphs structure matching ReviewScreen expectations

### Stage 2: Frontend Updates (COMPLETED)
- **Modified UploadScreen** with:
  - Small unobtrusive demo selector (top-left)
  - File upload area (for V1)
  - Navigation to /setup instead of /process

- **Created ReviewSetupScreen** with:
  - Document info display
  - Document type detection with override
  - **NEW: Review Mode Toggle (Static Demo vs Dynamic Review)**
    - Static: Instant, uses pre-computed data from /public/static/
    - Dynamic: Full AI agent analysis (30-60s)
  - Depth selector (Light/Medium/Heavy with costs)
  - Prompt chips for common review focuses
  - Custom instructions textarea
  - Cost estimation (Free for static, actual cost for dynamic)
  - Warning for large documents

- **Updated ProcessScreen** to:
  - Handle both static and dynamic modes
  - Show different progress steps for each mode
  - Static mode: Quick loading (< 2s)
  - Dynamic mode: Simulated agent stages (Planning, Track A/B/C)

- **Updated App.jsx** routing to include /setup

### Key Features Implemented
1. **Easy toggle between static/dynamic modes** - Switch in ReviewSetupScreen
2. **Static demo uses existing files** in /public/static/ (manuscript_demo.json, issues_demo.json)
3. **Dynamic mode ready for backend** - ProcessScreen has API call structure commented
4. **Seamless user experience** - Same ReviewScreen handles both modes

### Stage 3: Backend Setup (COMPLETED)
- **Created FastAPI backend structure** in `/demo2/backend/`:
  - `main.py` - FastAPI app with CORS configured for frontend
  - `config/settings.py` - Configuration for Claude API and agent settings
  - `requirements.txt` - Python dependencies

- **Implemented Agent Wireframe**:
  - `agents/orchestrator.py` - **Main coordinator** that orchestrates the 3-phase review
    - Called from `/api/run-review` endpoint
    - Manages: Planning → Parallel Tracks → Aggregation
  - `agents/planning_agent.py` - Analyzes document, creates review strategy
  - `agents/global_map_agent.py` - Creates document-wide understanding
  - `agents/track_agents.py` - Three review tracks:
    - Track A: Rigor (A1-A6 rubric codes)
    - Track B: Clarity (B1-B4 rubric codes)
    - Track C: Skeptical (C1-C4 rubric codes)
  - `agents/aggregator_agent.py` - Deduplicates and prioritizes issues
  - `agents/hostile_agent.py` - Extra scrutiny for "heavy" depth

- **Created Data Models**:
  - `models/document.py` - DocumentObject matching frontend structure
  - `models/review.py` - Issue, ReviewResult with rubric codes

- **API Endpoints** (`api/routes.py`):
  - `POST /api/run-review` - **Main entry point** called by ProcessScreen
    - Receives document + config
    - Initiates orchestrator agent
    - Returns mock data for demo (ready for LLM integration)
  - `GET /api/review-status/{job_id}` - Check async job status
  - `POST /api/parse-document` - Parse uploaded documents

### Orchestrator Flow
```
ProcessScreen (dynamic mode)
    ↓ POST /api/run-review
OrchestratorAgent.run_review()
    ↓ Phase 1: Planning + Global Map
    ↓ Phase 2: Track A, B, C (parallel)
    ↓ Phase 3: Aggregation + Hostile (if heavy)
    ↓ Returns ReviewResult
Frontend ReviewScreen displays issues
```

### Stage 4: Frontend-Backend Connection (COMPLETED)
- **Connected ProcessScreen to Backend**:
  - ProcessScreen now calls `POST /api/run-review` in dynamic mode
  - Sends document + configuration to backend
  - Shows progress animation during processing
  - Falls back to static mode if backend unavailable

- **Updated ManuscriptContext**:
  - Checks for backend review results in sessionStorage
  - Uses backend issues when available (dynamic mode)
  - Falls back to static issues otherwise

- **Created Testing Documentation**:
  - README.md with complete testing guide
  - Instructions for both static and dynamic modes
  - API testing examples
  - Troubleshooting guide

### Complete Flow Now Working
1. **Static Mode**: Instant review with pre-computed data
2. **Dynamic Mode**: Calls backend API → Orchestrator → Mock issues
3. **Error Handling**: Graceful fallback if backend unavailable

### Next Steps (Future)
- Add Claude API key to .env
- Implement actual LLM calls in agents
- Integrate with PDF parser pipeline
- Add real document upload support

---

*Log entries will be added as build progresses*