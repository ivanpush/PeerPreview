# Demo D1 Implementation Plan
## PeerPreview Scientific Manuscript Review Product

---

## Executive Summary

Demo D1 is a static, frontend-only prototype demonstrating a scientific manuscript review system with three distinct review tracks (A: local technical issues, B: global structure, C: biased reviewer persona), issue tracking, and figure management. Built with React + TailwindCSS, it uses mock JSON data generated from a **real scientific paper** to simulate a complete review workflow without any backend.

**Timeline:** 5-7 days
**Tech Stack:** React 18, TailwindCSS, Vite, Context API
**Deliverable:** Fully functional demo at `project/demo/frontend-d1/`
**Source Material:** Real scientific paper (FLECS mechanobiology manuscript) parsed and converted to static JSON

---

## Phase 1: Project Setup & Architecture (Day 1)

### 1.1 Environment Setup

#### Tasks:
1. **Clean existing demo or create new directory**
   ```bash
   # Option A: Clean existing
   rm -rf demo/frontend-d1/*

   # Option B: Create new
   mkdir -p demo/frontend-d1-new
   ```

2. **Initialize React + Vite + TailwindCSS**
   ```bash
   cd demo/frontend-d1
   npm create vite@latest . -- --template react
   npm install
   npm install -D tailwindcss postcss autoprefixer
   npx tailwindcss init -p
   ```

3. **Configure Tailwind**
   ```javascript
   // tailwind.config.js
   module.exports = {
     content: [
       "./index.html",
       "./src/**/*.{js,jsx}"
     ],
     theme: {
       extend: {
         colors: {
           primary: { /* scientific blues/purples */ },
           secondary: { /* grays */ },
           accent: { /* highlights */ }
         }
       }
     }
   }
   ```

4. **Setup project structure**
   ```
   frontend-d1/
   ├── src/
   │   ├── pages/
   │   ├── components/
   │   ├── context/
   │   ├── utils/
   │   ├── styles/
   │   │   └── index.css (with @tailwind directives)
   │   ├── App.jsx
   │   └── main.jsx
   ├── public/
   │   └── static/
   └── package.json
   ```

#### Implementation Details for Haiku:
- Use Vite for fast HMR and build times
- Configure path aliases in vite.config.js for cleaner imports
- Setup ESLint and Prettier for code consistency
- Add .env for any configuration variables
- Create README with setup instructions

### 1.2 Mock Data Schema Design

#### Create JSON Schema Files:

**IMPORTANT:** These JSON files will be **generated from a real scientific paper** (FLECS mechanobiology manuscript), not fictional content. The structure below shows the schema, but actual content will come from parsing the real paper.

**manuscript_demo.json Structure:**
```json
{
  "title": "High-throughput single-cell contractility screening identifies novel regulators of mechanobiology",
  "abstract": "Text from real paper abstract...",
  "sections": [
    {
      "section_id": "sec_intro",
      "heading": "Introduction",
      "paragraphs": ["p_intro_1", "p_intro_2", "p_intro_3", "p_intro_4"]
    },
    {
      "section_id": "sec_results",
      "heading": "Results",
      "paragraphs": ["p_results_1", "p_results_2", "..."]
    },
    {
      "section_id": "sec_methods",
      "heading": "Methods",
      "paragraphs": ["p_methods_1", "p_methods_2", "..."]
    }
  ],
  "paragraphs": [
    {
      "paragraph_id": "p_intro_1",
      "section_id": "sec_intro",
      "text": "Actual paragraph text from the real paper...",
      "metadata": {
        "citations": ["[1]", "[2]", "[3]"],
        "fig_refs": ["Figure 1"],
        "sources": [],
        "notes": []
      }
    }
  ],
  "figures": [
    {
      "figure_id": "fig1",
      "label": "Figure 1",
      "caption": "Actual caption from real paper...",
      "mentions": ["p_intro_2", "p_results_1", "..."],
      "page": 3
    }
  ],
  "references": "Actual references from paper..."
}
```

**issues_demo.json Structure:**

**IMPORTANT:** This file will contain **THREE TRACKS** (A, B, and C), all generated to reference real paragraph_ids from the actual paper:

```json
[
  {
    "id": "A1",
    "track": "A",
    "issue_type": "paragraph_rewrite",
    "severity": "major",
    "message": "Statistical analysis description lacks power calculation details.",
    "paragraph_id": "p_methods_7",
    "section_id": "sec_methods",
    "suggested_rewrite": "We performed statistical analysis using... [actual improved text]"
  },
  {
    "id": "B1",
    "track": "B",
    "issue_type": "section_outline",
    "severity": "minor",
    "message": "Introduction is verbose and could be condensed.",
    "section_id": "sec_intro",
    "outline_suggestion": [
      "1. Cell contractility in disease (1 paragraph)",
      "2. Limitations of current screening approaches (1 paragraph)",
      "3. FLECS platform overview and study objectives (1 paragraph)"
    ]
  },
  {
    "id": "B2",
    "track": "B",
    "issue_type": "global_strategy",
    "severity": "minor",
    "message": "Consider restructuring to lead with results for higher impact."
  },
  {
    "id": "C1",
    "track": "C",
    "issue_type": "biased_critique",
    "severity": "major",
    "message": "From the canonical mechanobiology view, claims of 'first ever' require explicit comparison with prior phenotypic screening approaches.",
    "paragraph_id": "p_intro_1",
    "section_id": "sec_intro",
    "bias_profile_id": "bp_mech_01",
    "comment": "The dominant view in mechanobiology expects novel screening platforms to be explicitly contrasted with existing methods and validated through mechanistic depth (omics, pathway mapping)."
  }
]
```

**bias_profile_demo.json Structure:**

**NEW FILE:** This defines the Track C biased reviewer persona. Will be loaded by the frontend to display the bias warning and narrative review.

```json
{
  "bias_profile_id": "bp_mech_01",
  "label": "Canonical Mechanobiology / Fibrosis Orthodoxy",
  "warning_text": "Track C simulates how a particular type of reviewer might push back, based on dominant narratives and incentives in the field. This is intentionally biased and should be treated as a stress-test, not objective truth.",
  "core_beliefs": [
    "Mechanobiology readouts must be tied to molecular mechanisms (omics, pathway mapping).",
    "Translatability requires in vivo validation or at least organoid / 3D tissue models.",
    "Generic kinase libraries are less valuable than disease-specific pathway targeting.",
    "Phenotypic screens are exploratory and should be tightly linked to clear MoAs."
  ],
  "sensitive_points": [
    "Claims of selectivity without mechanistic or functional validation.",
    "Over-generalization of cell-type-specific findings.",
    "Underpowered or noisy assays being used to claim 'atlas' or 'comprehensive' insights."
  ],
  "review_summary": {
    "author_intent_summary": "The authors present a high-throughput screening platform (FLECS) for measuring single-cell contractility across kinase inhibitors, identifying novel regulators relevant to fibrosis and other mechanobiology-driven diseases.",
    "biased_overall_view": "While the technical execution appears sound, the manuscript lacks the mechanistic depth and in vivo validation that the field increasingly expects. The emphasis on phenotypic readouts without pathway mapping limits impact, and generalizability claims across cell types need rigorous support."
  },
  "narrative_review": "The authors tackle an interesting question using an innovative platform. However, from the perspective of established mechanobiology research, several concerns arise:\n\nFirst, the claim of being 'first ever' in high-throughput contractility screening needs careful qualification. Second, reliance on a generic kinase library may miss disease-specific mechanisms. Third, absence of transcriptomic validation makes it difficult to assess mechanistic insights.\n\nThe work would be strengthened by organoid validation or in vivo correlates for top hits. Without this, translatability claims remain speculative."
}
```

#### Implementation Details for Haiku:

**Data Generation Tasks:**
1. **Generate `manuscript_demo.json` from real paper:**
   - Parse actual FLECS paper sections and paragraphs
   - Extract real figure captions and references
   - Create proper paragraph_id mapping (e.g., `p_intro_1`, `p_results_3`)
   - Preserve scientific content verbatim

2. **Generate `issues_demo.json` with all three tracks:**
   - **Track A issues (5-8):** Local technical issues (stats, methods clarity, citations)
   - **Track B issues (4-6):** Global structure (section flow, outline suggestions, strategic reframing)
   - **Track C issues (6-10):** Biased critiques anchored to real paragraphs from intro/results/discussion
   - All paragraph_ids must match those in `manuscript_demo.json`

3. **Generate `bias_profile_demo.json`:**
   - Hard-code one bias profile for mechanobiology/fibrosis orthodoxy
   - Write 3-4 sentence author intent summary
   - Write 4-6 sentence biased overall view
   - Write 2-3 paragraph narrative review in "Reviewer 2" style

4. **Ensure consistency:**
   - All issue `paragraph_id` fields must exist in manuscript JSON
   - All issue `section_id` fields must match manuscript sections
   - Track C issues must reference `bias_profile_id: "bp_mech_01"`

---

## Phase 2: Core Components (Day 2-3)

### 2.1 Context Setup

**ManuscriptContext.jsx:**
```javascript
import React, { createContext, useContext, useState, useCallback } from 'react';

const ManuscriptContext = createContext();

export const useManuscript = () => {
  const context = useContext(ManuscriptContext);
  if (!context) throw new Error('useManuscript must be used within ManuscriptProvider');
  return context;
};

export const ManuscriptProvider = ({ children }) => {
  const [manuscript, setManuscript] = useState(null);
  const [issues, setIssues] = useState([]);
  const [lastRewrite, setLastRewrite] = useState(null);
  const [selectedIssue, setSelectedIssue] = useState(null);
  const [activeFigureId, setActiveFigureId] = useState(null);

  const updateParagraph = useCallback((paragraphId, newText) => {
    // Store previous state for undo
    const paragraph = manuscript.paragraphs.find(p => p.paragraph_id === paragraphId);
    setLastRewrite({
      paragraphId,
      previousText: paragraph.text,
      newText
    });

    // Update paragraph text while preserving metadata
    setManuscript(prev => ({
      ...prev,
      paragraphs: prev.paragraphs.map(p =>
        p.paragraph_id === paragraphId
          ? { ...p, text: newText }
          : p
      )
    }));
  }, [manuscript]);

  const undoLastRewrite = useCallback(() => {
    if (!lastRewrite) return;

    setManuscript(prev => ({
      ...prev,
      paragraphs: prev.paragraphs.map(p =>
        p.paragraph_id === lastRewrite.paragraphId
          ? { ...p, text: lastRewrite.previousText }
          : p
      )
    }));

    setLastRewrite(null);
  }, [lastRewrite]);

  // Load mock data
  const loadMockData = async () => {
    const [manuscriptRes, issuesRes] = await Promise.all([
      fetch('/static/manuscript_demo.json'),
      fetch('/static/issues_demo.json')
    ]);

    const manuscriptData = await manuscriptRes.json();
    const issuesData = await issuesRes.json();

    setManuscript(manuscriptData);
    setIssues(issuesData);

    // Set first figure as active by default
    if (manuscriptData.figures?.length > 0) {
      setActiveFigureId(manuscriptData.figures[0].figure_id);
    }
  };

  const value = {
    manuscript,
    issues,
    lastRewrite,
    selectedIssue,
    activeFigureId,
    updateParagraph,
    undoLastRewrite,
    setSelectedIssue,
    setActiveFigureId,
    loadMockData
  };

  return (
    <ManuscriptContext.Provider value={value}>
      {children}
    </ManuscriptContext.Provider>
  );
};
```

#### Implementation Details for Haiku:
- Implement all state management methods
- Add loading and error states
- Include helper methods for filtering issues by track
- Add method to get paragraph by ID
- Include scroll-to-paragraph functionality

### 2.2 Screen Components

**UploadScreen.jsx:**
```javascript
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const UploadScreen = () => {
  const [fileName, setFileName] = useState('');
  const [isDragging, setIsDragging] = useState(false);
  const navigate = useNavigate();

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file && file.type === 'application/pdf') {
      setFileName(file.name);
    }
    setIsDragging(false);
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFileName(file.name);
    }
  };

  const handleParse = () => {
    if (fileName) {
      navigate('/process');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full">
        <h1 className="text-4xl font-bold text-gray-800 mb-2 text-center">
          PeerPreview
        </h1>
        <p className="text-gray-600 text-center mb-8">
          AI-Powered Scientific Manuscript Review
        </p>

        <div
          className={`
            border-2 border-dashed rounded-xl p-12 text-center transition-all
            ${isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300 bg-white'}
            ${fileName ? 'border-green-500' : ''}
          `}
          onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={handleDrop}
        >
          <svg className="mx-auto h-16 w-16 text-gray-400 mb-4">
            {/* PDF icon SVG */}
          </svg>

          {fileName ? (
            <div className="space-y-4">
              <p className="text-lg font-medium text-gray-900">
                {fileName}
              </p>
              <button
                onClick={handleParse}
                className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
              >
                Parse File
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              <p className="text-lg text-gray-600">
                Drag and drop your PDF here, or
              </p>
              <label className="inline-block">
                <input
                  type="file"
                  accept=".pdf"
                  onChange={handleFileSelect}
                  className="hidden"
                />
                <span className="px-6 py-3 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 cursor-pointer transition">
                  Browse Files
                </span>
              </label>
            </div>
          )}
        </div>

        <p className="text-sm text-gray-500 text-center mt-4">
          Demo mode: Upload any PDF to see the example manuscript
        </p>
      </div>
    </div>
  );
};
```

#### Implementation Details for Haiku:
- Add proper drag-and-drop visual feedback
- Include file type validation
- Show file size if available
- Add animation transitions
- Include error states for invalid files

---

## Phase 3: Review Screen Components (Day 3-4)

### 3.1 ManuscriptView Component

**ManuscriptView.jsx:**
```javascript
import React, { useEffect, useRef } from 'react';
import { useManuscript } from '../context/ManuscriptContext';

const ManuscriptView = () => {
  const { manuscript, selectedIssue } = useManuscript();
  const paragraphRefs = useRef({});

  useEffect(() => {
    // Scroll to paragraph when issue is selected
    if (selectedIssue?.paragraph_id) {
      const element = paragraphRefs.current[selectedIssue.paragraph_id];
      element?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }, [selectedIssue]);

  if (!manuscript) return <div>Loading manuscript...</div>;

  const renderParagraph = (paragraphId) => {
    const paragraph = manuscript.paragraphs.find(p => p.paragraph_id === paragraphId);
    if (!paragraph) return null;

    const isHighlighted = selectedIssue?.paragraph_id === paragraphId;

    return (
      <div
        key={paragraphId}
        ref={el => paragraphRefs.current[paragraphId] = el}
        className={`
          mb-4 p-4 rounded-lg transition-all duration-300
          ${isHighlighted ? 'bg-yellow-50 border-2 border-yellow-400' : ''}
        `}
      >
        <p className="text-gray-800 leading-relaxed">
          {paragraph.text}
        </p>

        {/* Metadata indicators */}
        <div className="mt-2 flex gap-2 flex-wrap">
          {paragraph.metadata.citations.length > 0 && (
            <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">
              {paragraph.metadata.citations.length} citations
            </span>
          )}
          {paragraph.metadata.fig_refs.length > 0 && (
            <span className="text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded">
              References: {paragraph.metadata.fig_refs.join(', ')}
            </span>
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="h-full overflow-y-auto p-6 bg-white">
      {/* Title */}
      <h1 className="text-3xl font-bold text-gray-900 mb-4">
        {manuscript.title}
      </h1>

      {/* Abstract */}
      <div className="mb-8 p-4 bg-gray-50 rounded-lg">
        <h2 className="text-xl font-semibold text-gray-800 mb-2">Abstract</h2>
        <p className="text-gray-700 leading-relaxed">{manuscript.abstract}</p>
      </div>

      {/* Sections */}
      {manuscript.sections.map(section => (
        <div key={section.section_id} className="mb-8">
          <h2
            className="text-2xl font-semibold text-gray-800 mb-4 pb-2 border-b"
            id={section.section_id}
          >
            {section.heading}
          </h2>
          {section.paragraphs.map(renderParagraph)}
        </div>
      ))}

      {/* References (optional) */}
      {manuscript.references && (
        <div className="mt-12 pt-8 border-t">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">References</h2>
          <div className="text-sm text-gray-600 whitespace-pre-wrap">
            {manuscript.references}
          </div>
        </div>
      )}
    </div>
  );
};
```

#### Implementation Details for Haiku:
- Implement smooth scrolling with offset for header
- Add paragraph numbering (optional)
- Include hover states for paragraphs
- Show line numbers if needed
- Add search/find functionality (bonus)

### 3.2 IssuesPanel Component

**IssuesPanel.jsx:**
```javascript
import React, { useState } from 'react';
import { useManuscript } from '../context/ManuscriptContext';

const IssuesPanel = ({ onOpenRewriteModal, onOpenOutlineModal, onOpenBiasedReviewModal }) => {
  const { issues, setSelectedIssue, manuscript } = useManuscript();
  const [filterTrack, setFilterTrack] = useState('all');

  const filteredIssues = issues.filter(issue =>
    filterTrack === 'all' || issue.track === filterTrack
  );

  const getSeverityColor = (severity) => {
    switch(severity) {
      case 'major': return 'bg-red-100 text-red-700 border-red-200';
      case 'minor': return 'bg-yellow-100 text-yellow-700 border-yellow-200';
      default: return 'bg-gray-100 text-gray-700 border-gray-200';
    }
  };

  const getTrackColor = (track) => {
    switch(track) {
      case 'A': return 'bg-blue-500';
      case 'B': return 'bg-purple-500';
      case 'C': return 'bg-amber-500';
      default: return 'bg-gray-500';
    }
  };

  const handleIssueClick = (issue) => {
    setSelectedIssue(issue);

    // Determine action based on issue type
    switch(issue.issue_type) {
      case 'paragraph_rewrite':
        // Scroll to paragraph (handled by ManuscriptView)
        break;
      case 'section_outline':
        // Scroll to section
        const section = document.getElementById(issue.section_id);
        section?.scrollIntoView({ behavior: 'smooth' });
        break;
      case 'global_strategy':
        // No scroll action
        break;
    }
  };

  const renderActionButton = (issue) => {
    switch(issue.issue_type) {
      case 'paragraph_rewrite':
        return (
          <button
            onClick={(e) => {
              e.stopPropagation();
              onOpenRewriteModal(issue);
            }}
            className="mt-3 px-4 py-2 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700 transition"
          >
            Rewrite
          </button>
        );

      case 'section_outline':
        return (
          <button
            onClick={(e) => {
              e.stopPropagation();
              onOpenOutlineModal(issue);
            }}
            className="mt-3 px-4 py-2 bg-purple-600 text-white text-sm rounded-md hover:bg-purple-700 transition"
          >
            View Outline
          </button>
        );

      case 'biased_critique':
        return (
          <button
            onClick={(e) => {
              e.stopPropagation();
              onOpenBiasedReviewModal(issue);
            }}
            className="mt-3 px-4 py-2 bg-amber-600 text-white text-sm rounded-md hover:bg-amber-700 transition"
          >
            View Biased Review
          </button>
        );

      case 'global_strategy':
        return null; // No action button

      default:
        return null;
    }
  };

  return (
    <div className="h-full flex flex-col bg-gray-50">
      {/* Header with filters */}
      <div className="p-4 bg-white border-b">
        <h2 className="text-xl font-semibold text-gray-800 mb-3">
          Issues ({filteredIssues.length})
        </h2>

        <div className="flex gap-2">
          <button
            onClick={() => setFilterTrack('all')}
            className={`px-3 py-1 rounded-md text-sm font-medium transition ${
              filterTrack === 'all'
                ? 'bg-gray-800 text-white'
                : 'bg-gray-200 text-gray-600 hover:bg-gray-300'
            }`}
          >
            All
          </button>
          <button
            onClick={() => setFilterTrack('A')}
            className={`px-3 py-1 rounded-md text-sm font-medium transition ${
              filterTrack === 'A'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 text-gray-600 hover:bg-gray-300'
            }`}
          >
            Track A
          </button>
          <button
            onClick={() => setFilterTrack('B')}
            className={`px-3 py-1 rounded-md text-sm font-medium transition ${
              filterTrack === 'B'
                ? 'bg-purple-600 text-white'
                : 'bg-gray-200 text-gray-600 hover:bg-gray-300'
            }`}
          >
            Track B
          </button>
          <button
            onClick={() => setFilterTrack('C')}
            className={`px-3 py-1 rounded-md text-sm font-medium transition ${
              filterTrack === 'C'
                ? 'bg-amber-600 text-white'
                : 'bg-gray-200 text-gray-600 hover:bg-gray-300'
            }`}
          >
            Track C
          </button>
        </div>
      </div>

      {/* Issues list */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {filteredIssues.map(issue => (
          <div
            key={issue.id}
            onClick={() => handleIssueClick(issue)}
            className="bg-white rounded-lg p-4 border cursor-pointer hover:shadow-md transition-shadow"
          >
            {/* Issue header */}
            <div className="flex items-center gap-2 mb-2">
              <span className={`w-8 h-8 rounded-full flex items-center justify-center text-white text-xs font-bold ${getTrackColor(issue.track)}`}>
                {issue.track}
              </span>
              <span className={`px-2 py-1 rounded text-xs font-medium border ${getSeverityColor(issue.severity)}`}>
                {issue.severity}
              </span>
              <span className="text-xs text-gray-500 ml-auto">
                {issue.issue_type.replace('_', ' ')}
              </span>
            </div>

            {/* Issue message */}
            <p className="text-gray-700 text-sm mb-2">
              {issue.message}
            </p>

            {/* Location info */}
            {issue.paragraph_id && (
              <p className="text-xs text-gray-500">
                Paragraph: {issue.paragraph_id}
              </p>
            )}
            {issue.section_id && !issue.paragraph_id && (
              <p className="text-xs text-gray-500">
                Section: {manuscript?.sections.find(s => s.section_id === issue.section_id)?.heading}
              </p>
            )}

            {/* Action button */}
            {renderActionButton(issue)}
          </div>
        ))}
      </div>
    </div>
  );
};
```

#### Implementation Details for Haiku:
- Add issue counts per track in filter buttons
- Include issue type icons
- Add animation for issue selection
- Implement keyboard navigation
- Add search/filter by severity

---

## Phase 4: Modal Components (Day 4-5)

### 4.1 RewriteModal Component (Type 1)

**RewriteModal.jsx:**
```javascript
import React, { useState, useEffect } from 'react';
import { useManuscript } from '../context/ManuscriptContext';

const RewriteModal = ({ issue, onClose }) => {
  const { manuscript, updateParagraph } = useManuscript();
  const [rewriteText, setRewriteText] = useState('');
  const [isEdited, setIsEdited] = useState(false);

  const paragraph = manuscript.paragraphs.find(
    p => p.paragraph_id === issue.paragraph_id
  );

  useEffect(() => {
    // Load suggested rewrite or generate placeholder
    const suggested = issue.suggested_rewrite ||
      `[Improved version of the paragraph with clearer language and better structure. This maintains all citations ${paragraph.metadata.citations.join(', ')} and figure references ${paragraph.metadata.fig_refs.join(', ')}.}]`;
    setRewriteText(suggested);
  }, [issue, paragraph]);

  const handleApply = () => {
    updateParagraph(issue.paragraph_id, rewriteText);
    onClose();
  };

  const handleTextChange = (e) => {
    setRewriteText(e.target.value);
    setIsEdited(true);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="px-6 py-4 border-b flex items-center justify-between">
          <div>
            <h2 className="text-xl font-semibold text-gray-800">Paragraph Rewrite</h2>
            <p className="text-sm text-gray-600 mt-1">{issue.message}</p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6">
          <div className="grid md:grid-cols-2 gap-6">
            {/* Original */}
            <div>
              <h3 className="text-sm font-medium text-gray-700 mb-2">Original Paragraph</h3>
              <div className="p-4 bg-gray-50 rounded-lg border border-gray-200">
                <p className="text-gray-700 leading-relaxed">
                  {paragraph.text}
                </p>
              </div>

              {/* Show metadata */}
              <div className="mt-3 space-y-1">
                {paragraph.metadata.citations.length > 0 && (
                  <p className="text-xs text-gray-500">
                    Citations: {paragraph.metadata.citations.join(', ')}
                  </p>
                )}
                {paragraph.metadata.fig_refs.length > 0 && (
                  <p className="text-xs text-gray-500">
                    Figure refs: {paragraph.metadata.fig_refs.join(', ')}
                  </p>
                )}
              </div>
            </div>

            {/* Rewrite */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-medium text-gray-700">Proposed Rewrite</h3>
                {isEdited && (
                  <span className="text-xs text-amber-600">Modified</span>
                )}
              </div>
              <textarea
                value={rewriteText}
                onChange={handleTextChange}
                className="w-full h-64 p-4 bg-white rounded-lg border border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 resize-none"
                placeholder="Enter rewritten text..."
              />

              <p className="mt-2 text-xs text-gray-500">
                Note: Citations and figure references are preserved in metadata
              </p>
            </div>
          </div>

          {/* Comparison metrics (optional) */}
          <div className="mt-6 p-4 bg-blue-50 rounded-lg">
            <p className="text-sm text-blue-800">
              <strong>Important:</strong> This rewrite will replace the paragraph text while preserving all metadata (citations, figure references, sources). Changes can be undone.
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="px-6 py-4 border-t flex justify-end gap-3">
          <button
            onClick={onClose}
            className="px-4 py-2 text-gray-600 hover:text-gray-800"
          >
            Cancel
          </button>
          <button
            onClick={handleApply}
            className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition"
          >
            Apply Replace
          </button>
        </div>
      </div>
    </div>
  );
};
```

### 4.2 OutlineModal Component (Type 2)

**OutlineModal.jsx:**
```javascript
import React from 'react';
import { useManuscript } from '../context/ManuscriptContext';

const OutlineModal = ({ issue, onClose }) => {
  const { manuscript } = useManuscript();

  const section = manuscript.sections.find(
    s => s.section_id === issue.section_id
  );

  // Get first paragraph of section for preview
  const firstParagraphId = section?.paragraphs[0];
  const firstParagraph = manuscript.paragraphs.find(
    p => p.paragraph_id === firstParagraphId
  );

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl max-w-3xl w-full max-h-[80vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="px-6 py-4 border-b">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-semibold text-gray-800">Section Outline Suggestion</h2>
              <p className="text-sm text-gray-600 mt-1">{section?.heading}</p>
            </div>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6">
          {/* Current section preview */}
          <div className="mb-6">
            <h3 className="text-sm font-medium text-gray-700 mb-2">Current Section Beginning</h3>
            <div className="p-4 bg-gray-50 rounded-lg border border-gray-200">
              <p className="text-gray-600 text-sm line-clamp-4">
                {firstParagraph?.text}
              </p>
              <p className="text-xs text-gray-400 mt-2">
                ... ({section?.paragraphs.length} total paragraphs)
              </p>
            </div>
          </div>

          {/* Suggested outline */}
          <div className="mb-6">
            <h3 className="text-sm font-medium text-gray-700 mb-3">Suggested Outline</h3>
            <div className="space-y-3">
              {issue.outline_suggestion?.map((item, index) => (
                <div key={index} className="flex gap-3">
                  <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <span className="text-purple-700 text-sm font-medium">{index + 1}</span>
                  </div>
                  <p className="text-gray-700 text-sm leading-relaxed pt-1">
                    {item}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Advisory note */}
          <div className="p-4 bg-amber-50 rounded-lg border border-amber-200">
            <div className="flex gap-3">
              <svg className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
              </svg>
              <div>
                <p className="text-sm text-amber-800 font-medium mb-1">Advisory Only</p>
                <p className="text-sm text-amber-700">
                  This is a suggested outline for restructuring. It does not automatically modify the manuscript.
                  You may use this as guidance for manual editing.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="px-6 py-4 border-t flex justify-between">
          <button
            onClick={() => {/* Mark as noted logic */}}
            className="px-4 py-2 text-purple-600 hover:text-purple-700"
          >
            Mark as Noted
          </button>
          <button
            onClick={onClose}
            className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
```

### 4.3 BiasedReviewModal Component (Type 3 - Track C)

**BiasedReviewModal.jsx:**
```javascript
import React, { useState, useEffect } from 'react';
import { useManuscript } from '../context/ManuscriptContext';

const BiasedReviewModal = ({ issue, onClose }) => {
  const { manuscript } = useManuscript();
  const [biasProfile, setBiasProfile] = useState(null);

  useEffect(() => {
    // Load bias profile
    fetch('/static/bias_profile_demo.json')
      .then(res => res.json())
      .then(data => setBiasProfile(data));
  }, []);

  const paragraph = issue.paragraph_id
    ? manuscript.paragraphs.find(p => p.paragraph_id === issue.paragraph_id)
    : null;

  if (!biasProfile) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl max-w-5xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header with warning */}
        <div className="px-6 py-4 bg-amber-50 border-b border-amber-200">
          <div className="flex items-start gap-3">
            <svg className="w-6 h-6 text-amber-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            <div className="flex-1">
              <h2 className="text-lg font-semibold text-amber-900 mb-1">
                Track C: Biased Reviewer Perspective
              </h2>
              <p className="text-sm text-amber-800">
                {biasProfile.warning_text}
              </p>
            </div>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6">
          {/* Bias Profile Info */}
          <div className="mb-6 p-4 bg-gray-50 rounded-lg border">
            <h3 className="font-medium text-gray-900 mb-2">
              Reviewer Profile: {biasProfile.label}
            </h3>

            <div className="mb-4">
              <h4 className="text-sm font-medium text-gray-700 mb-2">Core Beliefs:</h4>
              <ul className="text-sm text-gray-600 space-y-1 list-disc list-inside">
                {biasProfile.core_beliefs.map((belief, i) => (
                  <li key={i}>{belief}</li>
                ))}
              </ul>
            </div>

            <div>
              <h4 className="text-sm font-medium text-gray-700 mb-2">Sensitive Points:</h4>
              <ul className="text-sm text-gray-600 space-y-1 list-disc list-inside">
                {biasProfile.sensitive_points.map((point, i) => (
                  <li key={i}>{point}</li>
                ))}
              </ul>
            </div>
          </div>

          {/* Specific Issue Context */}
          {paragraph && (
            <div className="mb-6">
              <h3 className="text-sm font-medium text-gray-700 mb-2">Flagged Text:</h3>
              <div className="p-4 bg-amber-50 rounded-lg border border-amber-200">
                <p className="text-gray-700 text-sm leading-relaxed mb-3">
                  {paragraph.text}
                </p>
                <div className="pt-3 border-t border-amber-300">
                  <p className="text-sm font-medium text-amber-900 mb-1">Critique:</p>
                  <p className="text-sm text-amber-800">{issue.comment || issue.message}</p>
                </div>
              </div>
            </div>
          )}

          {/* Overall Review Summary */}
          <div className="mb-6">
            <h3 className="text-sm font-medium text-gray-700 mb-3">Overall Assessment</h3>

            <div className="mb-4 p-4 bg-blue-50 rounded-lg border border-blue-200">
              <p className="text-sm font-medium text-blue-900 mb-2">Author Intent (as understood):</p>
              <p className="text-sm text-blue-800 leading-relaxed">
                {biasProfile.review_summary.author_intent_summary}
              </p>
            </div>

            <div className="p-4 bg-red-50 rounded-lg border border-red-200">
              <p className="text-sm font-medium text-red-900 mb-2">Biased Reviewer View:</p>
              <p className="text-sm text-red-800 leading-relaxed">
                {biasProfile.review_summary.biased_overall_view}
              </p>
            </div>
          </div>

          {/* Full Narrative Review */}
          <div className="mb-6">
            <h3 className="text-sm font-medium text-gray-700 mb-3">Full Narrative Review</h3>
            <div className="p-4 bg-white rounded-lg border border-gray-300">
              <p className="text-sm text-gray-700 leading-relaxed whitespace-pre-line">
                {biasProfile.narrative_review}
              </p>
            </div>
          </div>

          {/* Explanation */}
          <div className="p-4 bg-purple-50 rounded-lg border border-purple-200">
            <div className="flex gap-3">
              <svg className="w-5 h-5 text-purple-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
              </svg>
              <div>
                <p className="text-sm text-purple-800 font-medium mb-1">How to Use This</p>
                <p className="text-sm text-purple-700">
                  This simulated review helps you anticipate pushback from reviewers with specific field biases or orthodoxies.
                  Use it to strengthen your framing, add missing comparisons, or prepare rebuttals.
                  In a full system, this profile would be generated from literature/funding analysis via Perplexity/web search.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="px-6 py-4 border-t flex justify-between">
          <button
            onClick={() => {/* Mark as noted logic */}}
            className="px-4 py-2 text-amber-600 hover:text-amber-700"
          >
            Mark as Noted
          </button>
          <button
            onClick={onClose}
            className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default BiasedReviewModal;
```

#### Implementation Details for Haiku:
- Load bias_profile_demo.json on mount
- Display warning prominently at top
- Show both the specific issue AND the full narrative review
- Use amber/warning color scheme to distinguish from Tracks A/B
- Include explanation of how this would work in production (Perplexity integration)
- Make it clear this is NOT objective criticism

---

## Phase 5: Additional Components (Day 5-6)

### 5.1 FiguresPanel Component

**FiguresPanel.jsx:**
```javascript
import React from 'react';
import FigureTabs from './FigureTabs';
import FigureCaptionBox from './FigureCaptionBox';
import { useManuscript } from '../context/ManuscriptContext';

const FiguresPanel = () => {
  const { manuscript, activeFigureId } = useManuscript();

  if (!manuscript?.figures || manuscript.figures.length === 0) {
    return null;
  }

  const activeFigure = manuscript.figures.find(
    f => f.figure_id === activeFigureId
  );

  return (
    <div className="border-t bg-gray-50">
      <FigureTabs />
      {activeFigure && <FigureCaptionBox figure={activeFigure} />}
    </div>
  );
};
```

**FigureTabs.jsx:**
```javascript
const FigureTabs = () => {
  const { manuscript, activeFigureId, setActiveFigureId } = useManuscript();

  return (
    <div className="bg-white border-b">
      <div className="overflow-x-auto">
        <div className="flex px-4 py-2 gap-2 min-w-max">
          {manuscript.figures.map(figure => (
            <button
              key={figure.figure_id}
              onClick={() => setActiveFigureId(figure.figure_id)}
              className={`
                px-4 py-2 rounded-md text-sm font-medium whitespace-nowrap transition
                ${activeFigureId === figure.figure_id
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }
              `}
            >
              {figure.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};
```

**FigureCaptionBox.jsx:**
```javascript
const FigureCaptionBox = ({ figure }) => {
  return (
    <div className="p-4">
      <div className="bg-white rounded-lg p-4 border">
        <h3 className="font-medium text-gray-800 mb-2">{figure.label}</h3>
        <p className="text-gray-700 text-sm leading-relaxed">
          {figure.caption}
        </p>

        {figure.mentions?.length > 0 && (
          <div className="mt-3 pt-3 border-t">
            <p className="text-xs text-gray-500">
              Referenced in paragraphs: {figure.mentions.join(', ')}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};
```

### 5.2 UndoBanner Component

**UndoBanner.jsx:**
```javascript
import React, { useEffect, useState } from 'react';
import { useManuscript } from '../context/ManuscriptContext';

const UndoBanner = () => {
  const { lastRewrite, undoLastRewrite } = useManuscript();
  const [show, setShow] = useState(false);

  useEffect(() => {
    if (lastRewrite) {
      setShow(true);
      const timer = setTimeout(() => setShow(false), 10000); // Auto-hide after 10s
      return () => clearTimeout(timer);
    }
  }, [lastRewrite]);

  if (!show || !lastRewrite) return null;

  return (
    <div className="fixed bottom-4 left-1/2 transform -translate-x-1/2 z-40">
      <div className="bg-gray-800 text-white px-6 py-3 rounded-lg shadow-lg flex items-center gap-4">
        <span>Paragraph updated</span>
        <button
          onClick={() => {
            undoLastRewrite();
            setShow(false);
          }}
          className="text-blue-300 hover:text-blue-200 font-medium"
        >
          Undo
        </button>
        <button
          onClick={() => setShow(false)}
          className="text-gray-400 hover:text-gray-300"
        >
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
          </svg>
        </button>
      </div>
    </div>
  );
};
```

---

## Phase 6: Integration & Testing (Day 6-7)

### 6.1 App.jsx Main Router

```javascript
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ManuscriptProvider } from './context/ManuscriptContext';
import UploadScreen from './pages/UploadScreen';
import ProcessScreen from './pages/ProcessScreen';
import ReviewScreen from './pages/ReviewScreen';

function App() {
  return (
    <BrowserRouter>
      <ManuscriptProvider>
        <Routes>
          <Route path="/" element={<UploadScreen />} />
          <Route path="/process" element={<ProcessScreen />} />
          <Route path="/review" element={<ReviewScreen />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </ManuscriptProvider>
    </BrowserRouter>
  );
}

export default App;
```

### 6.2 ProcessScreen.jsx

```javascript
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useManuscript } from '../context/ManuscriptContext';

const ProcessScreen = () => {
  const navigate = useNavigate();
  const { loadMockData } = useManuscript();
  const [status, setStatus] = useState('loading');

  useEffect(() => {
    const process = async () => {
      setStatus('loading');
      await loadMockData();
      setStatus('complete');
    };
    process();
  }, [loadMockData]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 flex items-center justify-center">
      <div className="text-center">
        {status === 'loading' ? (
          <>
            <div className="w-16 h-16 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <h2 className="text-2xl font-semibold text-gray-800 mb-2">Processing Manuscript</h2>
            <p className="text-gray-600">Analyzing content and detecting issues...</p>
          </>
        ) : (
          <>
            <div className="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">Analysis Complete</h2>
            <button
              onClick={() => navigate('/review')}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
            >
              Continue to Review
            </button>
          </>
        )}
      </div>
    </div>
  );
};
```

### 6.3 ReviewScreen.jsx (Main Layout)

```javascript
import React, { useState } from 'react';
import ManuscriptView from '../components/ManuscriptView';
import IssuesPanel from '../components/IssuesPanel';
import FiguresPanel from '../components/FiguresPanel';
import RewriteModal from '../components/RewriteModal';
import OutlineModal from '../components/OutlineModal';
import BiasedReviewModal from '../components/BiasedReviewModal';
import UndoBanner from '../components/UndoBanner';

const ReviewScreen = () => {
  const [rewriteModalIssue, setRewriteModalIssue] = useState(null);
  const [outlineModalIssue, setOutlineModalIssue] = useState(null);
  const [biasedReviewModalIssue, setBiasedReviewModalIssue] = useState(null);

  return (
    <div className="h-screen flex flex-col bg-gray-100">
      {/* Header */}
      <div className="bg-white border-b px-6 py-3 flex items-center justify-between">
        <h1 className="text-xl font-semibold text-gray-800">PeerPreview - Manuscript Review</h1>
        <div className="flex gap-3">
          <button className="px-4 py-2 text-gray-600 hover:text-gray-800">
            Export
          </button>
          <button className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
            Save Review
          </button>
        </div>
      </div>

      {/* Main content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Manuscript view (left) */}
        <div className="flex-1 flex flex-col">
          <div className="flex-1 overflow-hidden">
            <ManuscriptView />
          </div>
          <FiguresPanel />
        </div>

        {/* Issues panel (right) */}
        <div className="w-96 border-l">
          <IssuesPanel
            onOpenRewriteModal={setRewriteModalIssue}
            onOpenOutlineModal={setOutlineModalIssue}
            onOpenBiasedReviewModal={setBiasedReviewModalIssue}
          />
        </div>
      </div>

      {/* Modals */}
      {rewriteModalIssue && (
        <RewriteModal
          issue={rewriteModalIssue}
          onClose={() => setRewriteModalIssue(null)}
        />
      )}

      {outlineModalIssue && (
        <OutlineModal
          issue={outlineModalIssue}
          onClose={() => setOutlineModalIssue(null)}
        />
      )}

      {biasedReviewModalIssue && (
        <BiasedReviewModal
          issue={biasedReviewModalIssue}
          onClose={() => setBiasedReviewModalIssue(null)}
        />
      )}

      {/* Undo banner */}
      <UndoBanner />
    </div>
  );
};
```

---

## Testing Checklist

### Functionality Tests:
- [ ] Upload screen accepts PDF files
- [ ] Process screen loads mock data from real paper
- [ ] Manuscript displays all sections and paragraphs correctly
- [ ] Issues panel filters by track (All, A, B, C)
- [ ] Clicking issue scrolls to paragraph/section
- [ ] Track A: Type 1 rewrite modal opens and applies changes
- [ ] Track B: Type 2 outline modal shows advisory content
- [ ] Track B: Type 3 global issues show no action button
- [ ] Track C: Biased review modal opens with warning
- [ ] Track C: Modal displays bias profile, flagged text, and narrative review
- [ ] Undo banner appears and functions after rewrite
- [ ] Figure tabs are scrollable and clickable
- [ ] Figure captions display correctly

### Edge Cases:
- [ ] Empty sections handle gracefully
- [ ] Missing paragraphs don't crash
- [ ] Long captions wrap properly
- [ ] Multiple rapid rewrites handle correctly
- [ ] Filter with no matching issues shows empty state

### Performance:
- [ ] Smooth scrolling to paragraphs
- [ ] No lag with 20+ issues
- [ ] Modal transitions are smooth
- [ ] Tab switching is instant

---

## Deployment Instructions

1. **Build for production:**
```bash
npm run build
```

2. **Test production build:**
```bash
npm run preview
```

3. **Deploy to Vercel/Netlify:**
```bash
# Vercel
vercel --prod

# Netlify
netlify deploy --prod
```

---

## File Structure Summary

```
demo/frontend-d1/
├── src/
│   ├── pages/
│   │   ├── UploadScreen.jsx
│   │   ├── ProcessScreen.jsx
│   │   └── ReviewScreen.jsx
│   ├── components/
│   │   ├── ManuscriptView.jsx
│   │   ├── IssuesPanel.jsx
│   │   ├── RewriteModal.jsx (Track A)
│   │   ├── OutlineModal.jsx (Track B)
│   │   ├── BiasedReviewModal.jsx (Track C - NEW)
│   │   ├── FiguresPanel.jsx
│   │   ├── FigureTabs.jsx
│   │   ├── FigureCaptionBox.jsx
│   │   └── UndoBanner.jsx
│   ├── context/
│   │   └── ManuscriptContext.jsx
│   ├── utils/
│   │   └── mockLoader.js
│   ├── styles/
│   │   └── index.css
│   ├── App.jsx
│   └── main.jsx
├── public/
│   └── static/
│       ├── manuscript_demo.json (generated from real FLECS paper)
│       ├── issues_demo.json (Tracks A, B, and C)
│       └── bias_profile_demo.json (Track C reviewer persona)
├── package.json
├── tailwind.config.js
├── vite.config.js
└── README.md
```

---

## Next Steps After Demo D1

1. **User Testing:**
   - Deploy to staging
   - Gather feedback on UX flow
   - Identify pain points

2. **Backend Integration (Demo D2):**
   - Real PDF parsing
   - LLM integration for rewrites
   - Database for persistence

3. **Advanced Features:**
   - Multi-paragraph rewrites
   - Version history
   - Collaborative review
   - Export functionality

---

This plan is designed to be executed by any developer with React experience. Each component is fully specified with implementation details, making it suitable for parallel development if needed.