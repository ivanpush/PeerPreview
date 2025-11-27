# PeerPreview Demo2 - Testing Guide

## Quick Start

### 1. Start the Backend (Terminal 1)
```bash
cd demo2/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```
Backend will run on http://localhost:8000

### 2. Start the Frontend (Terminal 2)
```bash
cd demo2/frontend-d2
npm install
npm start
```
Frontend will run on http://localhost:3000

## Testing the Complete Flow

### Static Mode (Instant, Pre-computed)
1. Open http://localhost:3000
2. Select a demo document from dropdown (e.g., "Academic Manuscript")
3. Click "Continue to Setup"
4. Choose **"Static Demo"** mode (green)
5. Select review depth (Light/Medium/Heavy)
6. Click "View Demo Review"
7. Review loads instantly with pre-computed issues

### Dynamic Mode (Backend API)
1. Open http://localhost:3000
2. Select a demo document from dropdown
3. Click "Continue to Setup"
4. Choose **"Dynamic Review"** mode (blue)
5. Select review depth (affects number of issues)
6. Optionally add custom instructions
7. Click "Start AI Review"
8. Watch progress as it calls backend API
9. Review loads with backend-generated issues

## API Testing

### Test Backend Directly
```bash
# Check health
curl http://localhost:8000/health

# Test review endpoint
curl -X POST http://localhost:8000/api/run-review \
  -H "Content-Type: application/json" \
  -d '{
    "document": {
      "document_id": "test_001",
      "document_type": "academic_manuscript",
      "title": "Test Document",
      "sections": [],
      "paragraphs": []
    },
    "depth": "medium"
  }'
```

## Architecture

### Frontend Flow
```
UploadScreen → ReviewSetupScreen → ProcessScreen → ReviewScreen
              (select mode)        (calls API)     (displays issues)
```

### Backend Flow (Dynamic Mode)
```
/api/run-review
    ↓
OrchestratorAgent
    ↓
Phase 1: Planning + Global Map
    ↓
Phase 2: Track A, B, C (parallel)
    ↓
Phase 3: Aggregation + Hostile
    ↓
Return issues to frontend
```

## Key Features

- **Toggle between modes**: Static (instant) vs Dynamic (API)
- **Three review depths**: Light (8 issues), Medium (15 issues), Heavy (25 issues)
- **Rubric-based review**: A1-A6, B1-B4, C1-C4 issue codes
- **Mock data ready**: Backend returns properly formatted issues
- **Error handling**: Falls back to static if backend unavailable

## Files Structure

```
demo2/
├── frontend-d2/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── UploadScreen.jsx      # Demo selector
│   │   │   ├── ReviewSetupScreen.jsx # Mode toggle
│   │   │   ├── ProcessScreen.jsx     # API caller
│   │   │   └── ReviewScreen.tsx      # Unchanged
│   │   └── context/
│   │       └── ManuscriptContext.jsx # Handles backend data
│   └── public/
│       ├── fixtures/                 # Demo documents
│       └── static/                   # Pre-computed reviews
│
└── backend/
    ├── main.py                       # FastAPI app
    ├── api/routes.py                 # /api/run-review endpoint
    └── agents/
        ├── orchestrator.py           # Main coordinator
        ├── planning_agent.py         # Review strategy
        ├── track_agents.py           # A, B, C tracks
        └── aggregator_agent.py       # Issue deduplication
```

## Troubleshooting

- **Backend not running**: Frontend falls back to static mode
- **CORS errors**: Check backend is on port 8000
- **Toggle not visible**: Refresh page, it's always shown now
- **No issues showing**: Check browser console for errors

## Next Steps

To add real LLM integration:
1. Add Claude API key to `.env` file
2. Implement LLM calls in agent methods
3. Remove mock data generation
4. Test with actual document parsing