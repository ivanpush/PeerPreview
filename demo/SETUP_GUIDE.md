# PeerPreview Demo Setup Guide

## Project Structure Created

```
demo/
├── frontend-d1/          # Static React prototype
│   ├── src/
│   │   ├── pages/        # 3 main screens
│   │   │   ├── UploadScreen.jsx
│   │   │   ├── ProcessScreen.jsx
│   │   │   └── ReviewScreen.jsx
│   │   ├── components/   # UI components
│   │   │   ├── ManuscriptView.jsx
│   │   │   ├── IssuesPanel.jsx
│   │   │   ├── RewriteModal.jsx
│   │   │   └── UndoBanner.jsx
│   │   └── utils/
│   │       └── mockLoader.js
│   ├── public/static/    # Mock data
│   │   ├── manuscript_demo.json
│   │   └── issues_demo.json
│   └── package.json
└── backend-stub/         # (empty - for future use)
```

## Installation & Running

```bash
cd demo/frontend-d1
npm install
npm run dev
```

Then open: **http://localhost:5173**

## Demo Flow

1. **Upload Screen**
   - Shows branding and upload UI
   - Click "Choose File (Demo)" to proceed
   - No actual upload happens

2. **Process Screen**
   - Shows animated "analyzing" state
   - Displays fake processing steps
   - Auto-transitions after 3 seconds

3. **Review Screen** (Main UI)
   - **Left Panel:** Full manuscript view
     - Scrollable document
     - Sections and paragraphs
     - Highlights selected issue's paragraph

   - **Right Panel:** Issues list
     - 6 detected issues (mock data)
     - Severity badges (High/Medium/Low)
     - Filter buttons
     - Click issue to highlight in manuscript
     - "View AI Rewrite" button shows modal

4. **Rewrite Modal**
   - Side-by-side comparison
   - Original text vs. suggested rewrite
   - Rationale explanation
   - Accept/Cancel buttons

## Mock Data

### `manuscript_demo.json`
Sample CRISPR/HSC research paper with:
- Title and authors
- 6 sections (Abstract, Intro, Methods, Results, Discussion, Conclusion)
- Multiple paragraphs per section

### `issues_demo.json`
6 AI-detected issues covering:
- Statistical rigor problems
- Methodology gaps
- Claims vs. evidence mismatches
- Missing controls
- Clarity improvements
- Writing style suggestions

Each issue includes:
- Severity level
- Issue type
- Description
- Location (section + paragraph index)
- Original text
- Suggested rewrite
- Rationale

## Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool (fast dev server)
- **CSS** - Vanilla CSS (no frameworks - keep it simple)
- **No routing** - State-based screen switching
- **No state management** - Plain React hooks

## Key Design Decisions

1. **Static data** - Everything loads from JSON files
2. **No API calls** - Simulated with setTimeout
3. **Simple styling** - Pure CSS for maintainability
4. **Component isolation** - Each component self-contained
5. **No external UI library** - Custom components for full control

## What's Next

### User Testing
- Share with potential users
- Observe navigation patterns
- Note pain points and confusion
- Gather feedback on issue presentation
- Test rewrite acceptance workflow

### After Validation
- Build real frontend in `/frontend`
- Integrate with real backend
- Implement actual LLM agents
- Add authentication
- Build collaboration features

## Customization Tips

### To Add More Issues
Edit `public/static/issues_demo.json`:
```json
{
  "id": 7,
  "severity": "high",
  "type": "Your Type",
  "title": "Issue title",
  "description": "What's wrong",
  "location": { "section": "Results", "paragraph": 2 },
  "originalText": "The problematic text",
  "suggestedRewrite": "Better version",
  "rationale": "Why this is better"
}
```

### To Change Mock Paper
Edit `public/static/manuscript_demo.json` with your own sections/paragraphs.

### To Adjust Timing
In `src/utils/mockLoader.js`, change the delay:
```js
export function simulateProcessing(ms = 3000) { // <- Change 3000
```

## Troubleshooting

**Port already in use:**
```bash
npm run dev -- --port 5174
```

**Dependencies not installing:**
```bash
rm -rf node_modules package-lock.json
npm install
```

**Build errors:**
```bash
npm run build
```

## File Overview

### Core App Files
- `src/main.jsx` - Entry point
- `src/App.jsx` - Screen router
- `src/index.css` - Global styles

### Screens
- `UploadScreen` - Initial upload interface
- `ProcessScreen` - Animated processing state
- `ReviewScreen` - Main review interface

### Components
- `ManuscriptView` - Document display with highlighting
- `IssuesPanel` - Sidebar with issue cards
- `RewriteModal` - Full-screen comparison modal
- `UndoBanner` - Floating undo notification (placeholder)

### Utils
- `mockLoader.js` - Fake API calls

## Questions?

Check the main README in `/demo` or `/demo/frontend-d1` for more details.
