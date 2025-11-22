# PeerPreview - Manuscript Review Assistant

AI-powered manuscript review system that provides deep, actionable feedback for scientific papers. Think Grammarly meets peer review, with special focus on catching desk-reject issues before submission.

**Key differentiators**: Track A/B split (objective vs subjective), Citation Police (detects lazy citations), Figure Agent (unique - analyzes figure-text consistency).

## Quick Start

```bash
# Clone and setup
git clone <repo>
cd PeerPreview

# Run with Docker
docker-compose up

# Or run locally
cd backend && pip install -r requirements.txt && uvicorn main:app --reload
cd frontend && npm install && npm run dev

# Upload PDF at http://localhost:3000
```

## What It Does

Uploads scientific PDF → Parses into sections → Runs 8 parallel review agents → Returns structured feedback in 4 categories: Major Issues, Minor Issues, Suggestions, Guideline Violations.

## Documentation

- [Architecture Overview](docs/ARCHITECTURE.md) - System design
- [Development Phases](docs/PHASES.md) - Build timeline with tasks
- [Agent Specifications](docs/AGENTS.md) - Each reviewer's role
- [Prompt Guidelines](docs/PROMPTS.md) - LLM prompt structure

## Status

Phase 0 complete: PDF parsing, basic UI, API endpoints ready. Next: Agent implementation.