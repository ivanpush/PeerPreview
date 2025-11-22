# Prompt Guidelines

## Prompt Organization

Prompts live in `backend/prompts/` as markdown files:
```
backend/prompts/
├── section_reviewers/
│   ├── methods_reviewer.md
│   ├── results_reviewer.md
│   └── ...
├── specialists/
│   ├── citation_police.md
│   ├── figure_agent.md
│   └── cross_doc.md
└── system/
    └── base_instructions.md
```

## Prompt Structure

All prompts follow this pattern:

```markdown
You are a [ROLE] reviewing a scientific manuscript.

## Your Task
[Clear description of what to check]

## Track A: Objective Checks (Pass/Fail)
- [ ] Check 1: [Condition] → Severity: CRITICAL/MAJOR
- [ ] Check 2: [Condition] → Severity: MAJOR

## Track B: Suggestions (Optional Improvements)
- Category 1: [What to look for]
- Category 2: [What to look for]

## Input Data
You receive:
- section_text: [Description]
- context: [Additional data like indices]

## Output Format
Return JSON:
{
  "track_a_issues": [...],
  "track_b_suggestions": [...],
  "passed_checks": [...]
}
```

## Key Principles

1. **Single Response**: Both Track A and B in one LLM call
2. **No Line Numbers**: Use exact quotes for location
3. **Structured Output**: Always return valid JSON
4. **Clear Severity**: Critical > Major > Minor > Suggestion

## Common Instructions

All agents receive:
- Temperature: 0.1 (low for consistency)
- Max tokens: 4000
- Response format: JSON
- Instruction: "Be specific, cite evidence"

## Prompt Variables

Templates use placeholders:
- `{section_text}` - The text to review
- `{ns_found}` - Sample sizes detected
- `{figures}` - Figure list
- `{citations}` - Citation mappings

## Track A vs Track B Examples

**Track A (Objective)**
```
"Missing IRB statement for human subjects research"
Location: Methods section
Severity: CRITICAL
```

**Track B (Subjective)**
```
"Consider breaking Methods into subheadings for clarity"
Location: Methods paragraph 3
Severity: SUGGESTION
```

## Model-Specific Adaptations

- **Claude**: Detailed reasoning, complex checks
- **OpenAI**: Style and consistency analysis
- **Groq**: Simple extraction tasks, binary checks