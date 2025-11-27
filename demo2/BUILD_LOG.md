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

### Next Steps
- Backend API setup with FastAPI
- Implement review agents (Planning, Track A/B/C)
- Connect dynamic mode to real backend

---

*Log entries will be added as build progresses*