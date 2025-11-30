# PeerPreview Backend - CLAUDE.md

## Project Overview

PeerPreview is an AI-powered document review system. This is the Python/FastAPI backend that orchestrates LLM agents to analyze documents and produce structured reviews.

## Tech Stack

- Python 3.11+
- FastAPI for API server
- Pydantic v2 for data validation
- Anthropic SDK for Claude API
- instructor for structured LLM output
- asyncio for parallel agent execution

## Project Structure

```
backend/
├── main.py                    # FastAPI app entry point
├── api/
│   └── routes.py              # API endpoints
├── models/
│   ├── __init__.py
│   ├── document.py            # DocumentObject, Paragraph, Section, etc.
│   ├── argument_map.py        # ArgumentMap, Claim, Evidence, Method
│   ├── review_plan.py         # ReviewPlan, AgentConfig
│   ├── issue.py               # IssueCard, Tab, Severity
│   └── output.py              # ReviewOutput, Rubric
├── agents/
│   ├── __init__.py
│   ├── extractor.py           # Extracts ArgumentMap from document
│   ├── planner.py             # Creates ReviewPlan from ArgumentMap
│   ├── clarity.py             # Prose/grammar issues (Track B)
│   ├── rigor.py               # Logic/methods issues (Track A)
│   ├── domain.py              # Field-specific issues (Track A)
│   ├── adversary.py           # Skeptical review (Track C)
│   └── assembler.py           # Deduplicates and finalizes issues
├── services/
│   ├── __init__.py
│   ├── pipeline.py            # Main orchestration pipeline
│   ├── composer.py            # Prompt assembly from modules
│   └── perplexity.py          # RAG integration (V1)
├── prompts/
│   ├── agents/
│   │   ├── extractor/core.md
│   │   ├── clarity/
│   │   │   ├── core.md
│   │   │   └── voice/{scientific,grant,legal,policy}.md
│   │   ├── rigor/...
│   │   ├── domain/...
│   │   └── adversary/...
│   ├── modifiers/
│   │   ├── tier/{quick,standard,deep}.md
│   │   ├── focus/{methodology,statistics,novelty,...}.md
│   │   └── instruction/{none,sparse,moderate,dense}.md
│   └── schema/
│       └── {issue_card,argument_map,...}.md
├── utils/
│   ├── __init__.py
│   └── llm_client.py          # Anthropic + instructor wrapper
├── fixtures/                   # Test fixtures (mirrors frontend)
│   ├── sample_document.json
│   ├── sample_argument_map.json
│   └── sample_issues.json
├── tests/
│   ├── test_models.py
│   ├── test_pipeline.py
│   └── test_api.py
├── requirements.txt
└── .env                        # ANTHROPIC_API_KEY
```

## Architecture Overview

```
Document → Extractor → ArgumentMap → Planner → ReviewPlan
                                         ↓
                          ┌──────────────┼──────────────┐
                          ↓              ↓              ↓
                      Clarity        Rigor          Adversary
                      (Track B)    (Track A)       (Track C)
                          ↓              ↓              ↓
                          └──────────────┼──────────────┘
                                         ↓
                                    Assembler
                                         ↓
                                   ReviewOutput
```

## Key Data Models

### DocumentObject (input from frontend)
```python
class DocumentObject(BaseModel):
    document_id: str
    document_type: str  # academic_manuscript, grant_proposal, etc.
    title: str
    authors: str | None
    affiliations: str | None
    source_format: str  # pdf, docx, tex
    sections: list[Section]
    paragraphs: list[Paragraph]
    figures: list[Figure]
    meta: dict
```

### ArgumentMap (internal, from Extractor)
```python
class ArgumentMap(BaseModel):
    claims: list[Claim]       # Main assertions with sentence_ids
    evidence: list[Evidence]  # Supporting data linked to claims
    methods: list[Method]     # Methodology descriptions
    definitions: list[Definition]
    structure: Structure      # Section relationships
```

### ReviewPlan (internal, from Planner)
```python
class ReviewPlan(BaseModel):
    agents: dict[str, AgentConfig]  # Per-agent settings
    section_priorities: dict[str, float]  # section_id → weight
    skip_sections: list[str]
    high_risk_sections: list[str]
    anticipated_issues: list[str]
    go_deeper_candidates: list[str]
    expected_issue_count: str  # few, moderate, many
    reasoning: str
```

### IssueCard (output to frontend)
```python
class IssueCard(BaseModel):
    id: str
    track: Literal['A', 'B', 'C']  # Frontend uses A/B/C
    issue_type: str  # paragraph_rewrite, biased_critique, section_outline
    severity: Literal['major', 'minor']
    title: str
    message: str
    paragraph_id: str
    section_id: str
    sentence_ids: list[str]
    original_text: str | None
    
    # Track A/B fields
    suggested_rewrite: str | None
    rationale: str
    
    # Track C fields
    critique: str | None
    suggested_revision: str | None
    category: str | None
    addressable: bool | None
    
    # Special types
    outline_suggestion: list[str] | None
```

### ReviewOutput (API response)
```python
class ReviewOutput(BaseModel):
    review_id: str
    document_id: str
    issues: list[IssueCard]
    summary: str
    rubric: Rubric
    metadata: ReviewMetadata
```

## Agent → Track Mapping

| Agent | Track | Tab Label | Focus |
|-------|-------|-----------|-------|
| Clarity | B | Clarity | Prose, grammar, flow, explanations |
| Rigor | A | Rigor | Logic, methods, stats, controls |
| Domain | A | Rigor | Field-specific, citations (V1) |
| Adversary | C | Counterpoint | Overclaims, alternatives, limitations |

## Pipeline Flow

1. **parse_request()**: Validate incoming request
2. **extractor()**: Document → ArgumentMap (Opus)
3. **planner()**: ArgumentMap + user input → ReviewPlan (Sonnet)
4. **compose_prompts()**: ReviewPlan → agent prompts (deterministic)
5. **run_agents()**: Execute Clarity ‖ Rigor ‖ Domain, then Adversary
6. **assembler()**: Dedupe, route to tracks, compute rubric (deterministic)
7. **format_response()**: Package for frontend

## LLM Usage

| Agent | Model | Why |
|-------|-------|-----|
| Extractor | claude-opus-4-20250514 | Deep reasoning for structure extraction |
| Planner | claude-sonnet-4-20250514 | Fast, smart routing decisions |
| Clarity | varies by tier | Haiku (quick), Sonnet (standard), Opus (deep) |
| Rigor | varies by tier | Same as Clarity |
| Adversary | varies by tier | Same as Clarity |

## Tier Configuration

| Tier | Extractor | Planner | Agents | Adversary |
|------|-----------|---------|--------|-----------|
| quick | Opus | Sonnet | Haiku | disabled |
| standard | Opus | Sonnet | Sonnet | Sonnet |
| deep | Opus | Sonnet | Opus | Opus |

## API Endpoints

### POST /api/run-review
Main review endpoint. Returns full review result.

```python
# Request
class ReviewRequest(BaseModel):
    document: dict  # DocumentObject as dict
    depth: Literal['light', 'medium', 'heavy']
    user_prompt: str | None
    document_type: str

# Response: ReviewOutput
```

### GET /api/health
Health check endpoint.

## Environment Variables

```
ANTHROPIC_API_KEY=sk-ant-...
MOCK_MODE=false              # Set true for testing without API calls
LOG_LEVEL=INFO
```

## Testing

```bash
# Run all tests
pytest

# Run with mock mode (no API calls)
MOCK_MODE=true pytest

# Run specific test file
pytest tests/test_pipeline.py -v
```

## Common Tasks

### Add new agent
1. Create `agents/new_agent.py` with `run_new_agent()` function
2. Add prompts in `prompts/agents/new_agent/`
3. Add to pipeline in `services/pipeline.py`
4. Update `assembler.py` to handle output

### Modify issue output
1. Update `models/issue.py` IssueCard
2. Update agent output parsing
3. Ensure frontend compatibility

### Add new document type
1. Add voice prompts in `prompts/agents/*/voice/`
2. Update Planner to handle routing
3. Add fixture for testing

## Do NOT

- Don't call LLM without instructor wrapper (use `llm_client.py`)
- Don't modify IssueCard schema without frontend coordination
- Don't add database dependencies (V0 is stateless)
- Don't use synchronous API calls (use async throughout)
- Don't skip the Extractor (all agents need ArgumentMap)

## V0 Scope

✅ Included:
- Extractor, Planner, Clarity, Rigor, Adversary agents
- Three review tiers
- Basic deduplication
- Rubric generation

❌ Not included (V1+):
- Domain agent with RAG
- Consensus mode
- Go Deeper functionality
- File upload/parsing
- Database persistence
- User authentication