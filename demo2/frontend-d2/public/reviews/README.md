# Review Data for Demo Mode

This directory contains pre-generated review data for demo mode in the PeerPreview application.

## File Naming Convention

Review files follow the pattern: `{document}_{tier}.json`

- **document**: Base name of the fixture file (e.g., `manuscript_pdf`, `grant_docx`)
- **tier**: Review depth level (`firstpass`, `fullreview`, `deepanalysis`)

## Available Review Files

| File | Document Type | Depth | Issues | Description |
|------|--------------|-------|--------|-------------|
| `manuscript_pdf_firstpass.json` | Academic Manuscript | First Pass | 10 (major only) | Quick review focusing on critical issues |
| `manuscript_pdf_fullreview.json` | Academic Manuscript | Full Review | 28 (all severities) | Comprehensive review with all scopes |
| `grant_docx_fullreview.json` | Grant Application | Full Review | 6 | NIH-style grant review |
| `policy_brief_pdf_fullreview.json` | Policy Brief | Full Review | 5 | Policy analysis review |

## Review Data Schema

Each review file contains:

```json
{
  "review_id": "unique_review_identifier",
  "document_id": "matching_fixture_document_id",
  "document_type": "academic_manuscript|grant_application|policy_brief|legal_brief",
  "depth": "first_pass|full_review|deep_analysis",
  "scopes": ["array", "of", "review", "scopes"],

  "issues": [
    {
      "id": "unique_issue_id",
      "track": "backend_agent_track",
      "scope": "ui_scope_category",
      "persona": "persona_label",
      "severity": "major|moderate|minor",
      "title": "short_issue_title",
      "message": "detailed_issue_description",
      "paragraph_id": "target_paragraph",
      "section_id": "target_section",
      "sentence_ids": ["affected", "sentences"],
      "original_text": "text_to_replace",
      "suggested_rewrite": "proposed_replacement",
      "rationale": "explanation_for_reviewer"
    }
  ],

  "persona_summaries": {
    "scope_name": {
      "label": "Display Name",
      "archetype": "reviewer_personality",
      "summary": "overall_assessment",
      "major_strengths": ["list", "of", "strengths"],
      "major_concerns": ["list", "of", "concerns"],
      "issue_count": {
        "major": 0,
        "moderate": 0,
        "minor": 0
      }
    }
  },

  "metadata": {
    "generated_at": "ISO_date_string",
    "fixture_file": "source_fixture.json",
    "notes": "additional_context"
  }
}
```

## Scope Mappings

### Academic Manuscript
- `rigor` → "Rigor Review" (Methods and statistics)
- `clarity` → "Clarity Review" (Readability and structure)
- `counterpoint` → "Counterpoint" (Adversarial domain expert)

### Grant Application
- `significance` → "Significance Review" (Impact and importance)
- `innovation` → "Innovation Review" (Novel approaches)
- `approach_rigor` → "Approach & Rigor" (Methodology)
- `feasibility` → "Feasibility & Team Fit" (Practicality)

### Policy Brief
- `evidence_quality` → "Evidence Review" (Data quality)
- `stakeholder_objections` → "Stakeholder Objections" (Political feasibility)
- `implementation_feasibility` → "Implementation Feasibility" (Practical execution)
- `clarity` → "Clarity & Messaging" (Communication effectiveness)

## How It Works

1. User selects document and review depth in ReviewSetupScreen
2. DocumentContext checks for matching review file: `/reviews/{document}_{depth}.json`
3. If found, loads pre-generated issues and persona summaries
4. If not found, falls back to `generateMockIssues()` function
5. Review data displayed in ReviewScreen with appropriate personas and scopes

## Adding New Review Files

To add reviews for new documents:

1. Create file following naming convention
2. Match `document_id` with fixture file
3. Include all required schema fields
4. Set appropriate scopes for document type
5. Test with `node demo2/scripts/test-demo-reviews.js`

## Testing

Run the test script to validate all review files:

```bash
cd demo2
node scripts/test-demo-reviews.js
```

This will check:
- File structure and JSON validity
- Required fields presence
- Issue format compliance
- Fixture alignment