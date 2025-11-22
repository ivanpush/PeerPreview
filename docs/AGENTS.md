# Agent Specifications

## Agent Overview Table

| Agent | Type | Input | Output | Track A | Track B | Priority |
|-------|------|-------|---------|---------|---------|----------|
| **MethodsReviewer** | Section | Methods text + CrossDocIndex | SectionReviewReport | IRB/ethics, sample size, stats methods | Structure, detail, clarity | P1 |
| **ResultsReviewer** | Section | Results text + FigureIndex | SectionReviewReport | Figure refs, N consistency, data-claim | Presentation order, viz suggestions | P1 |
| **AbstractReviewer** | Section | Abstract text + full doc | SectionReviewReport | Structure complete, claims match paper | Impact statement, quantitative results | P3 |
| **IntroductionReviewer** | Section | Intro text + CitationIndex | SectionReviewReport | Citations present, hypothesis stated | Flow, gap statement, scope | P3 |
| **DiscussionReviewer** | Section | Discussion text + results | SectionReviewReport | References results, limitations present | Alternative explanations, future work | P3 |
| **CrossDocConsistency** | Specialist | Full doc + all indices | CrossDocReport | N values, notation, terminology match | Redundancy, narrative arc | P2 |
| **CitationPolice** | Specialist | Citations + bibliography | CitationPoliceReport | Lazy citations (general→specific) | Citation appropriateness | P2 |
| **FigureAgent** | Specialist | Figures + references | FigureReport | Dangling refs, orphaned figs, numbering | Caption quality, consolidation | P2 |

## Agent Architecture

### Base Pattern
```python
class BaseAgent:
    async def run(ctx: AgentContext) → Report:
        prompt = self.build_prompt(ctx)
        response = await llm.complete(prompt)
        return self.parse_response(response)
```

### Track A vs Track B

**Track A (Objective)**
- Binary pass/fail checks
- Verifiable without domain expertise
- Severity: Critical or Major only
- Example: "Missing IRB statement"

**Track B (Subjective)**
- Improvement suggestions
- Style and clarity
- Severity: Minor or Suggestion only
- Example: "Consider using subheadings"

### LLM Assignment

- **Claude**: Primary section reviewers (Methods, Results, Discussion)
- **OpenAI**: Style and consistency (CrossDoc, Figure)
- **Groq/Mini**: Fast extraction (section splitting, citation extraction)

## Agent Context

Each agent receives:
```python
AgentContext:
    doc: ParsedDocument        # Full document
    cross: CrossDocIndex       # N values, terms
    citations: CitationIndex   # Citation mappings
    figures: FigureIndex       # Figure mappings
```

## Parallel Execution

All 8 agents run concurrently via `asyncio.gather()`:
- Total time = slowest agent (~30s)
- Fallback on failure
- Cache identical inputs