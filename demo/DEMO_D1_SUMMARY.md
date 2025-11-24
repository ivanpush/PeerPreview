# Demo D1 Implementation Summary

## 📋 Project Overview

**Demo D1** is a static, frontend-only React prototype that demonstrates a scientific manuscript review system with AI-powered issue detection and rewrite suggestions.

### Key Features:
- **3 Screens:** Upload → Process → Review
- **3 Rewrite Types:**
  - Type 1: Paragraph rewrites (mergeable)
  - Type 2: Section outlines (advisory only)
  - Type 3: Global strategy (commentary only)
- **Track System:** Issues from Track A (technical) and Track B (clarity)
- **Figures Panel:** Tabbed interface with captions
- **Undo Support:** Single-step undo for paragraph rewrites

---

## 🎯 Critical Implementation Points

### 1. **Rewrite Semantics (MOST IMPORTANT)**

The three rewrite types MUST behave differently:

| Type | issue_type | Action Button | Modal | Can Merge? | Modifies Text? |
|------|------------|---------------|-------|------------|----------------|
| **Type 1** | paragraph_rewrite | "Rewrite" | RewriteModal | ✅ Yes | ✅ Yes |
| **Type 2** | section_outline | "View Outline" | OutlineModal | ❌ No | ❌ No |
| **Type 3** | global_strategy | None | None | ❌ No | ❌ No |

### 2. **Metadata Preservation**

When applying Type 1 rewrites:
- ✅ **Change:** `paragraph.text`
- ❌ **Preserve:** `paragraph_id`, `section_id`, `metadata` (citations, fig_refs, sources)

This simulates that rewrites never lose scientific references.

### 3. **Mock Data Structure**

**manuscript_demo.json:**
- Paragraphs are stored separately from sections
- Each paragraph has unique ID and metadata
- Sections reference paragraph IDs

**issues_demo.json:**
- Each issue has a `track` (A or B)
- `issue_type` determines behavior
- Only Type 1 has `suggested_rewrite`

---

## ❓ Clarifying Questions (Need Answers)

### Critical Decisions:

1. **Existing Code:**
   - Should we refactor the existing `demo/frontend-d1/` or create `frontend-d1-new`?
   - Current demo uses vanilla CSS, prompt specifies TailwindCSS

2. **Mock Data Scale:**
   - How many sections? (Suggested: 5-6)
   - How many paragraphs? (Suggested: 20-25 total)
   - How many issues? (Suggested: 15-20, mixed types)
   - How many figures? (Suggested: 4-5)

3. **UI Polish Level:**
   - Basic functional (fast to build)
   - or Production-quality with animations (more time)

4. **Responsive Design:**
   - Desktop-only (1920x1080 optimized)
   - or Fully responsive (mobile/tablet support)

### Technical Choices:

5. **Routing:**
   - React Router (full navigation)
   - or State-based (simpler, no URLs)

6. **State Management:**
   - Plain React Context (as shown in plan)
   - or Zustand (simpler API)
   - or Redux Toolkit (if complex state needed)

7. **Component Library:**
   - Pure Tailwind (full control)
   - or Headless UI (accessible components)
   - or shadcn/ui (pre-styled components)

---

## 📁 Implementation Plan Location

Full detailed plan with code examples:
**`/demo/DEMO_D1_IMPLEMENTATION_PLAN.md`**

The plan includes:
- Complete component code
- Context implementation
- Modal behaviors
- Mock data schemas
- Testing checklist
- File structure

---

## 🚀 Quick Start (After Implementation)

```bash
cd demo/frontend-d1
npm install
npm start
```

Open: http://localhost:5173

---

## 📊 Phase Breakdown

| Phase | Duration | Components | Status |
|-------|----------|------------|--------|
| **Phase 1** | Day 1 | Setup, Architecture, Mock Data | 🔴 Not Started |
| **Phase 2** | Day 2-3 | Context, Upload, Process screens | 🔴 Not Started |
| **Phase 3** | Day 3-4 | ManuscriptView, IssuesPanel | 🔴 Not Started |
| **Phase 4** | Day 4-5 | RewriteModal, OutlineModal | 🔴 Not Started |
| **Phase 5** | Day 5-6 | Figures Panel, Undo Banner | 🔴 Not Started |
| **Phase 6** | Day 6-7 | Integration, Testing, Polish | 🔴 Not Started |

**Total Timeline:** 5-7 days

---

## 🎨 Design System

### Colors (Suggested):
```css
primary: blue-600 (actions)
secondary: gray (text, borders)
track-a: blue (technical issues)
track-b: purple (clarity issues)
success: green (complete states)
warning: amber (advisory content)
danger: red (major issues)
```

### Components:
- Modals: Centered, max-width 4xl
- Cards: White bg, subtle shadow
- Buttons: Rounded-md, clear hover states
- Badges: Small, colored by severity/track

---

## ✅ Success Criteria

Demo D1 is successful when:

1. **Flow Works:** Upload → Process → Review screens navigate correctly
2. **Issues Display:** Track filtering works, severity badges show
3. **Rewrites Behave Correctly:**
   - Type 1: Opens modal, applies changes, shows undo
   - Type 2: Shows outline, no changes
   - Type 3: No action button
4. **Metadata Preserved:** Citations/fig_refs survive rewrites
5. **Figures Work:** Tabs switch, captions display
6. **Feels Real:** Despite being static, UX feels like a real app

---

## 🔧 Non-Goals (DO NOT BUILD)

- ❌ Backend/API
- ❌ Real PDF parsing
- ❌ LLM integration
- ❌ Multi-paragraph rewrites
- ❌ Version history
- ❌ Export functionality
- ❌ Authentication
- ❌ Real figure images

This is purely a UX demonstration prototype.

---

## 📝 Notes

- All data comes from static JSON files
- No actual file upload processing
- Rewrites are pre-written in mock data
- Focus on correct behavior over features
- This is Demo D1 - more features come in D2/D3

---

## Next Step

**Please answer the clarifying questions above**, then we can begin Phase 1 implementation.