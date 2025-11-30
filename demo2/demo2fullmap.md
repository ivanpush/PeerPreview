# 🗺️ Demo2 Complete Directory Map

## Overview
Demo2 is the production-ready version of PeerPreview with a full React frontend, FastAPI backend, and sophisticated multi-agent review pipeline architecture. It supports both static (pre-computed) and dynamic (API-driven) review modes.

## Directory Structure

```
demo2/
├── 📄 README.md                    # Quick start guide, testing instructions, troubleshooting
├── 📁 backend/                     # FastAPI backend server
├── 📁 frontend-d2/                 # React frontend application
├── 📁 planning/                    # Architecture documents and design specs
└── 📁 scripts/                     # Utility scripts for testing and data processing
```

---

## 🎯 Backend (`/backend`)

The FastAPI backend implements the multi-agent review orchestration system.

### Root Files
```
backend/
├── 📄 main.py                      # FastAPI app entry point, CORS config, routes mounting
├── 📄 requirements.txt             # Python dependencies (FastAPI, Pydantic, Anthropic)
├── 📄 start.sh                     # Startup script: creates venv, installs deps, launches server
└── 📄 .env.example                 # Template for environment variables (Claude API key)
```

### `/api` - API Routes
```
api/
└── 📄 routes.py                    # Core API endpoints
```

**Key Endpoints:**
- `POST /api/run-review` - Main review orchestration endpoint. Receives document + review settings, returns issues array
- `GET /api/review-status/{job_id}` - Check async job status (for future async implementation)
- `POST /api/parse-document` - Convert uploaded documents to DocumentObject format

**Current State:** Returns mock data for demo. Ready for LLM integration.

### `/models` - Data Models
```
models/
├── 📄 document.py                  # Document structure models
└── 📄 review.py                    # Review and issue models
```

**document.py:**
- `DocumentObject` - Main document container with sections, paragraphs, metadata
- `Section` - Document section with title and paragraph references
- `Paragraph` - Text blocks with sentences and IDs for issue targeting
- `Sentence` - Individual text units for precise issue location

**review.py:**
- `RubricCode` - Enum of issue types (A1-A6: Rigor, B1-B4: Clarity, C1-C4: Skeptical)
- `Issue` - Individual review finding with severity, location, recommendations
- `ReviewResult` - Complete review output with issues array and summary
- `ReviewRequest` - Input model from frontend with document, depth, user_prompt

### `/agents` - Review Engine
```
agents/
├── 📄 orchestrator.py              # Master coordinator for 3-phase pipeline
├── 📄 planning_agent.py            # Phase 1: Strategy + global document mapping
├── 📄 track_agents.py              # Phase 2: Three parallel review tracks
├── 📄 aggregator_agent.py          # Phase 3a: Issue deduplication and prioritization
└── 📄 hostile_agent.py             # Phase 3b: Extra-critical review (heavy depth only)
```

**orchestrator.py:**
- Implements 3-phase review pipeline
- Manages agent lifecycle
- Coordinates data flow between phases
- Error handling and retry logic

**planning_agent.py:**
- Single-pass global document analysis
- Creates review strategy based on doc type
- Builds document map (themes, claims, critical passages)
- Eliminates redundant full-document LLM calls

**track_agents.py:**
- `TrackAAgent` - Rigor review (logic, evidence, methodology, statistics)
- `TrackBAgent` - Clarity review (writing quality, organization, flow)
- `TrackCAgent` - Skeptical review (overstated claims, missing alternatives)

**aggregator_agent.py:**
- Deduplicates similar issues across tracks
- Ensures global consistency
- Prioritizes by severity
- Generates unified summary

**hostile_agent.py:**
- "Reviewer 2" perspective
- Only activated in heavy depth mode
- Challenges fundamental assumptions
- Questions novelty and significance

### `/config` - Configuration
```
config/
└── 📄 settings.py                  # App configuration and environment settings
```

Contains:
- Claude API configuration (models: Sonnet for review, Haiku for classification)
- Agent timeouts and retry settings
- Document size limits (100 pages, 50k words)
- Debug mode settings

### `/services` - Service Layer
```
services/
└── (empty)                         # Ready for LLM integration services
```

Future home for:
- LLM service layer (Claude API integration)
- Document parser service
- Export service
- Database service

---

## 🎨 Frontend (`/frontend-d2`)

React application with TypeScript support and Tailwind CSS styling.

### Root Configuration
```
frontend-d2/
├── 📄 index.html                   # HTML entry point
├── 📄 package.json                 # Node dependencies and scripts
├── 📄 package-lock.json            # Locked dependency versions
├── 📄 vite.config.js               # Vite bundler configuration
├── 📄 tailwind.config.js           # Tailwind CSS configuration
├── 📄 postcss.config.js            # PostCSS configuration for Tailwind
├── 📄 .gitignore                   # Git ignore patterns
├── 📄 README.md                    # Frontend-specific documentation
└── 📄 IMPLEMENTATION_SUMMARY.md    # Detailed implementation notes
```

### `/src` - Source Code

#### `/src/pages` - Main Application Screens
```
pages/
├── 📄 UploadScreen.jsx             # Initial screen: demo selector or file upload
├── 📄 UploadScreen.css             # Styling for upload screen
├── 📄 ReviewSetupScreen.jsx        # Mode selection (static/dynamic) and review config
├── 📄 ProcessScreen.jsx            # API communication and progress display
├── 📄 ProcessScreen.css            # Styling for processing screen
├── 📄 ReviewScreen.jsx             # Main review interface (3-pane layout)
└── 📄 ReviewScreen.css             # Styling for review screen
```

**Screen Flow:**
1. `UploadScreen` → Select demo document or upload
2. `ReviewSetupScreen` → Choose static/dynamic mode, set depth
3. `ProcessScreen` → (Dynamic only) Call backend API
4. `ReviewScreen` → Display and interact with review results

#### `/src/components` - Reusable Components
```
components/
├── 📄 ManuscriptView.jsx           # Document display with inline issue indicators
├── 📄 ManuscriptView.css           # Document styling
├── 📄 IssuesPanel.jsx              # Issue list with filtering and actions
├── 📄 IssuesPanel.css              # Issue panel styling
├── 📄 RewriteModal.jsx             # Modal for rewrite suggestions
├── 📄 RewriteModal.css             # Rewrite modal styling
├── 📄 OutlineModal.jsx             # Document outline generation modal
├── 📄 BiasedReviewModal.jsx        # Alternative perspective review modal
├── 📄 ComparisonModal.jsx          # Compare different review versions
├── 📄 ConsensusToggle.jsx          # Toggle between review perspectives
├── 📄 UndoBanner.jsx               # Undo action notification
└── 📄 UndoBanner.css               # Undo banner styling
```

#### `/src/context` - State Management
```
context/
└── 📄 DocumentContext.jsx          # Global state management for document and reviews
```

Manages:
- Document data (manuscript object)
- Issues array
- Review mode (static/dynamic)
- API communication
- Accept/dismiss state
- User edits tracking

#### `/src/utils` - Utility Functions
```
utils/
└── 📄 mockLoader.js                # Load mock data for static mode
```

#### `/src/styles` - Theme and Styling
```
styles/
└── 📄 theme.js                     # Color palette and design tokens
```

#### Root Source Files
```
src/
├── 📄 App.jsx                      # Main app component with routing
├── 📄 main.jsx                     # React app entry point
└── 📄 index.css                    # Global CSS and Tailwind imports
```

### `/public` - Static Assets

#### `/public/fixtures` - Demo Documents
```
fixtures/
├── 📄 manuscript_pdf.json          # Academic paper example
├── 📄 grant_docx.json              # Grant application example
├── 📄 policy_brief_pdf.json        # Policy brief example
└── 📄 latex_manuscript.json        # LaTeX document example
```

Pre-parsed documents in DocumentObject format for demo purposes.

#### `/public/reviews` - Pre-computed Reviews
```
reviews/
├── 📄 README.md                    # Documentation for review files
├── 📄 manuscript_pdf_firstpass.json    # Light review example
├── 📄 manuscript_pdf_fullreview.json   # Heavy review example
├── 📄 grant_docx_fullreview.json       # Grant review example
├── 📄 policy_brief_pdf_fullreview.json # Policy review example
└── 📄 latex_manuscript_fullreview.json # LaTeX review example
```

Pre-computed review results for static mode (instant loading).

#### `/public/static` - Additional Static Data
```
static/
├── 📄 bias_profile_demo.json      # Sample bias analysis data
└── 📄 issues_demo.json             # Legacy issues format
```

### `/dist` - Production Build
```
dist/                               # Production-ready built files
├── 📄 index.html                   # Minified HTML
├── assets/                         # Bundled JS and CSS
├── fixtures/                       # Copied demo documents
└── static/                         # Copied static data
```

---

## 📋 Planning (`/planning`)

Architecture documentation and design specifications.

### Current Architecture
```
planning/
├── 📄 1_proj_overview_v2.md        # Project overview and goals
├── 📄 2_pages_and_views.md         # Frontend page specifications
├── 📄 3_agent_arch_v2.md           # Agent architecture design
├── 📄 4_review_tiers.md            # Review depth tier definitions
├── 📄 5_prompt_selector_and_library.md # Prompt management system
├── 📄 6_review_flow_v2.md          # Complete review flow diagram
├── 📄 7_tier_value_comparison.md   # Tier pricing and value props
├── 📄 8_document_persona_types.md  # Document types and review personas
├── 📄 BUILD_LOG.md                 # Development progress log
└── 📄 BUILD_PLAN.md                # Implementation roadmap
```

### Deprecated Versions
```
deprecated/
├── 📄 1_proj_overview.md           # Original project spec
├── 📄 3_agent_arch.md              # V1 agent architecture
└── 📄 5_base_agent_prompts.md      # Initial prompt templates
```

---

## 🛠️ Scripts (`/scripts`)

Utility scripts for testing and data processing.

```
scripts/
├── 📄 test-demo-reviews.js         # Validate review JSON structure
├── 📄 index_script.py              # Document indexing utility
├── 📄 index_script2.py             # Alternative indexing approach
├── 📄 parsed_manuscript.json       # Sample parsed document
├── 📄 scehma.json                  # JSON schema definitions
└── 📄 manuscript.txt.rtf           # Sample manuscript text
```

---

## 🔄 Data Flow

### User Journey
```
1. User selects demo or uploads document
2. Choose review mode:
   - Static: Load pre-computed review → Display
   - Dynamic: Configure → Call API → Display
3. Interact with review (accept/dismiss/edit)
4. Export final document
```

### API Flow (Dynamic Mode)
```
Frontend                    Backend
    |                          |
    ├─ POST /api/run-review ─→ |
    |                          ├─ OrchestratorAgent
    |                          ├─ Phase 1: Planning
    |                          ├─ Phase 2: Tracks A,B,C
    |                          ├─ Phase 3: Aggregation
    |                          ├─ (Optional) Hostile
    | ←── Review Results ──────┤
    |                          |
Display Issues                 |
```

### Static Mode Flow
```
Frontend
    ├─ Load fixture document
    ├─ Load pre-computed review
    └─ Display immediately
```

---

## 🚀 Current State & Next Steps

### ✅ Completed
- Full frontend with static/dynamic modes
- Backend API structure
- Agent architecture defined
- Mock data pipeline working
- Error handling and fallbacks
- Review interaction (accept/dismiss/edit)

### ⏳ To Implement
1. **LLM Integration** - Connect agents to Claude API
2. **Document Parser** - Integrate PDF parser pipeline
3. **Agent Prompts** - Implement actual review logic
4. **Async Jobs** - Add job queue for long reviews
5. **Database** - Persist reviews and user data
6. **Export** - Generate final documents

### 🔧 Configuration Needed
1. Add `.env` file with Claude API key
2. Configure document parser connection
3. Set up database (PostgreSQL recommended)
4. Configure Redis for job queue (optional)

---

## 💡 Key Design Decisions

1. **Dual Mode Support** - Static for demos, dynamic for real reviews
2. **Three-Phase Pipeline** - Planning → Parallel Tracks → Aggregation
3. **Rubric-Based Issues** - Standardized issue codes for consistency
4. **Track Specialization** - Separate agents for different review aspects
5. **Depth Tiers** - Light/Medium/Heavy with different issue counts
6. **Fallback Strategy** - Static mode when backend unavailable

---

## 📊 Review Depth Comparison

| Depth | Issues | Agents Used | Use Case |
|-------|--------|-------------|----------|
| Light | ~8 | Planning + Tracks | Quick feedback |
| Medium | ~15 | All standard agents | Balanced review |
| Heavy | ~25 | All + Hostile agent | Thorough critique |

---

## 🔗 Integration Points

- **Frontend ↔ Backend:** REST API on port 8000
- **Backend ↔ LLM:** Claude API (Sonnet/Haiku models)
- **Backend ↔ Parser:** DocumentObject creation
- **Static ↔ Dynamic:** Seamless fallback mechanism

This architecture supports sophisticated multi-agent review while maintaining simplicity for demo purposes and extensibility for production use.