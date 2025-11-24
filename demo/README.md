# PeerPreview Demo

This directory contains the **static prototype** for user touchpoint testing.

## Purpose

Build a non-functional demo to:
1. Test UX flows with potential users
2. Validate UI/UX decisions before backend investment
3. Gather feedback on interaction patterns
4. Demonstrate value proposition to stakeholders

## What's Inside

### `frontend-d1/`
React-based static prototype with:
- 3 main screens (Upload → Process → Review)
- Mock data loaded from JSON files
- No backend integration
- Focuses on visual design and UX flow

### `backend-stub/`
Reserved for future minimal backend if needed for demo (currently empty)

## Quick Start

```bash
cd frontend-d1
npm install
npm run dev
```

Open http://localhost:5173

## Development Flow

1. **Build demo** (current phase)
   - Create static UI with mock data
   - Test with users
   - Iterate on feedback

2. **After validation**
   - Build real frontend in `/frontend`
   - Build real backend in `/backend`
   - Connect with actual APIs

## Key Features to Test

- Upload flow and feedback
- Issue detection presentation
- Rewrite suggestion UX
- Accept/reject workflow
- Overall navigation and clarity

## Notes

- This is **intentionally non-functional**
- Focus is on UX, not implementation
- Real app will be built separately after validation
