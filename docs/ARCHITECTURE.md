# Architecture Overview

## System Flow

```
PDF Upload → Parser → Indexer → Agents → Aggregator → UI
     ↓          ↓         ↓         ↓          ↓        ↓
   FastAPI  pymupdf4llm  Pure   8 Parallel  Combine  Next.js
            → Markdown   Python    LLMs     Results
```

## Core Components

### 1. **Parser Layer** (`backend/services/parser/`)
- `DocumentBuilder`: Orchestrates PDF → ParsedDocument
- `SectionSplitter`: Regex-based section detection
- `SentenceIndexer`: NLTK sentence tokenization with char positions

### 2. **Index Layer** (`backend/services/indexers/`)
- `CrossDocIndexer`: Extracts N values, p-values, terms (no LLM)
- `CitationIndexer`: Maps citations ↔ bibliography
- `FigureIndexer`: Maps figures ↔ references, finds orphans

### 3. **Agent Layer** (`backend/services/agents/`)
- **Section Reviewers** (5): Abstract, Intro, Methods, Results, Discussion
- **Specialists** (3): CrossDoc, CitationPolice, FigureAgent
- All return Track A (objective) + Track B (subjective) in single call

### 4. **LLM Service** (`backend/services/llm/`)
- Multi-provider: Claude (primary), OpenAI (style), Groq (speed)
- Fallback chain with exponential backoff
- Cost tracking per agent

### 5. **API Layer** (`backend/main.py`)
- `/upload`: PDF → ParsedDocument
- `/review`: Trigger agent pipeline
- `/results/{id}`: Get FullReviewOutput

### 6. **Frontend** (`frontend/`)
- Upload with drag-drop
- Section display
- Issue cards grouped by severity
- Quote-based highlighting (no line numbers)

## Data Models

**Key Types**: `ParsedDocument`, `Issue`, `AgentContext`, `FullReviewOutput`

**Issue Grouping**:
1. Major Issues (Critical/Major, non-guideline)
2. Minor Issues
3. Suggestions
4. Guideline Violations (IRB, COI, etc.)

## Technical Decisions

- **No line numbers** - Use quotes for location (avoid hallucination)
- **Single agent call** - Both tracks in one response (cost/latency)
- **DEMO_MODE** - Pre-baked results for demo paper
- **Local-first** - Docker Compose, no cloud deps for V0