# PeerPreview Frontend - CLAUDE.md

## Project Overview

PeerPreview is an AI-powered document review system. This is the React frontend that displays manuscripts and review issues.

## Tech Stack

- React 18 with hooks
- React Router for navigation
- Framer Motion for animations
- Tailwind CSS (inline styles primarily)
- No state management library (Context API only)

## Project Structure

```
frontend-d2/
├── src/
│   ├── components/           # Reusable UI components
│   │   ├── IssuesPanel.jsx   # Main issues display with track tabs
│   │   ├── ManuscriptView.jsx # Document renderer with highlighting
│   │   ├── RewriteModal.jsx  # Edit suggested rewrites
│   │   ├── BiasedReviewModal.jsx # Track C detailed view
│   │   ├── OutlineModal.jsx  # Section outline suggestions
│   │   └── UndoBanner.jsx    # Undo rewrite notifications
│   ├── context/
│   │   └── DocumentContext.jsx # Global state for document + issues
│   ├── pages/
│   │   ├── UploadScreen.jsx     # Demo document selection
│   │   ├── ReviewSetupScreen.jsx # Configure review depth/focus
│   │   ├── ProcessScreen.jsx    # Loading/processing view
│   │   └── ReviewScreen.jsx     # Main review interface
│   ├── styles/
│   │   └── theme.js          # Color constants and helpers
│   └── utils/
│       └── mockLoader.js     # Static file loading utilities
├── public/
│   ├── fixtures/             # Pre-parsed document JSON files
│   │   ├── manuscript_pdf.json
│   │   ├── grant_docx.json
│   │   └── ...
│   ├── reviews/              # Pre-generated review results
│   │   ├── manuscript_pdf_fullreview.json
│   │   └── ...
│   └── static/               # Legacy demo files (deprecated)
└── package.json
```

## Key Data Models

### Document Object
```javascript
{
  document_id: string,
  document_type: 'academic_manuscript' | 'grant_proposal' | 'policy_brief' | 'legal_brief',
  title: string,
  authors: string,
  affiliations: string,
  source_format: 'pdf' | 'docx' | 'tex',
  sections: Section[],
  paragraphs: Paragraph[],
  figures: Figure[],
  references: string,
  meta: { page_count, word_count, ... }
}
```

### Issue Object (what backend returns)
```javascript
{
  id: string,                    // "issue_001"
  track: 'A' | 'B' | 'C',        // A=Rigor, B=Clarity, C=Counterpoint
  issue_type: 'paragraph_rewrite' | 'biased_critique' | 'section_outline',
  severity: 'major' | 'minor',
  title: string,
  message: string,
  paragraph_id: string,
  section_id: string,
  sentence_ids: string[],
  original_text: string | null,
  
  // Track A/B
  suggested_rewrite: string | null,
  rationale: string,
  
  // Track C only
  critique: string | null,
  suggested_revision: string | null,
  category: string | null,
  addressable: boolean | null,
  
  // Section outline type only
  outline_suggestion: string[] | null
}
```

### Review Response (from backend API)
```javascript
{
  review_id: string,
  document_id: string,
  issues: Issue[],
  summary: string,
  rubric: {
    soundness: number,      // 1-5
    significance: number,   // 1-5
    clarity: number,        // 1-5
    reproducibility: number, // 1-5
    overall_band: 'A' | 'B' | 'C' | 'D' | 'F',
    rationale: string
  },
  metadata: {
    tier: 'quick' | 'standard' | 'deep',
    document_type: string,
    completion_time: string,
    issue_counts: { track_a, track_b, track_c, total }
  }
}
```

## User Flow

1. **UploadScreen**: Select demo document from dropdown (V0) or upload file (V1)
2. **ReviewSetupScreen**: Configure depth (First Pass / Full Review / Deep Analysis), add focus chips, custom instructions
3. **ProcessScreen**: 
   - Static mode: Load pre-generated review from `/reviews/`
   - Dynamic mode: Call backend API, show progress
4. **ReviewScreen**: Display manuscript + issues panel, accept/dismiss issues, edit rewrites

## API Contract

### POST /api/run-review
```javascript
// Request
{
  document: DocumentObject,      // Full parsed document
  depth: 'light' | 'medium' | 'heavy',
  user_prompt: string | null,    // Custom focus instructions
  document_type: string
}

// Response
{
  review_id: string,
  document_id: string,
  issues: Issue[],
  summary: string,
  rubric: Rubric,
  metadata: ReviewMetadata
}
```

## State Management

All state lives in `DocumentContext`:
- `document`: Current document object
- `issues`: Array of review issues
- `selectedIssue`: Currently highlighted issue
- `dismissedIssues`: Set of dismissed issue IDs
- `lastRewrite`: For undo functionality

## Track Mapping

| Track | Internal Name | Tab Label | Agent |
|-------|---------------|-----------|-------|
| A | Rigor | Rigor | Rigor Agent |
| B | Clarity | Clarity | Clarity Agent |
| C | Counterpoint | Counterpoint | Adversary Agent |

## Styling Conventions

- Use inline styles with `theme.js` constants
- Colors: `theme.track.rigor` (#3E63DD), `theme.track.clarity` (#8E4EC6), `theme.track.counterpoint` (#C75A7A)
- Dark theme: background #151515, cards #1D1D1D, borders #2E2E2E
- Use `withOpacity(color, 0.15)` helper for backgrounds

## Testing Modes

1. **Static Demo**: Select fixture from dropdown, check "Static Demo" radio → loads from `/reviews/{fixture}_{depth}.json`
2. **Dynamic**: Check "Dynamic" radio → calls backend API at `http://localhost:8000/api/run-review`

## Common Tasks

### Add new issue type
1. Add to Issue interface
2. Handle in `IssuesPanel.jsx` render logic
3. Add modal if needed

### Add new document type
1. Add to `documentTypes` in `ReviewSetupScreen.jsx`
2. Add chips in `chipsByType`
3. Create fixture in `/public/fixtures/`

### Modify issue display
- Card layout: `IssuesPanel.jsx` → `renderCollapsedCard()` / `renderExpandedCard()`
- Highlighting: `ManuscriptView.jsx` → paragraph/sentence highlighting logic

## Do NOT

- Don't use localStorage (session data goes in sessionStorage)
- Don't add new npm dependencies without asking
- Don't modify theme colors without design review
- Don't change the Track A/B/C naming convention