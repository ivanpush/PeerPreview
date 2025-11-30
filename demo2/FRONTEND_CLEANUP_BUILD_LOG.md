# Frontend Cleanup Build Log

**Date:** 2025-11-30
**Task:** Remove mock issue generation to prepare for backend integration

## Changes Made

### 1. Removed Mock Generation Functions

**File:** `frontend-d2/src/context/DocumentContext.jsx`

**Removed Functions:**
- `generateMockIssues` (lines 6-207) - ~200 lines of mock issue generation based on document type
- `generateMockBiases` (lines 209-246) - ~37 lines of mock bias generation

These functions generated fake issues for demo purposes. The backend now provides real issues.

### 2. Updated loadMockData Function

#### Dynamic Mode Branch (line ~180)
**Changed:**
```javascript
// OLD
const mockBiasProfile = {
  document_id: fixtureData.manuscript_id || fixtureData.document_id,
  biases: generateMockBiases(fixtureData.document_type)
};
```

**To:**
```javascript
// NEW
const mockBiasProfile = {
  document_id: fixtureData.manuscript_id || fixtureData.document_id,
  biases: []  // Backend will provide real bias analysis
};
```

#### Static Demo Branch (lines ~273-277, ~279-283)
**Changed:**
```javascript
// OLD
if (!issuesData) {
  issuesData = fixtureData.issues || generateMockIssues(fixtureData);
}

const mockBiasProfile = {
  document_id: fixtureData.manuscript_id || fixtureData.document_id,
  biases: generateMockBiases(fixtureData.document_type)
};
```

**To:**
```javascript
// NEW
if (!issuesData) {
  issuesData = fixtureData.issues || [];
  console.warn('No review file found and no issues in fixture');
}

const mockBiasProfile = {
  document_id: fixtureData.manuscript_id || fixtureData.document_id,
  biases: []  // Backend will provide real bias analysis
};
```

## Issue Schema Compatibility

Verified that `IssuesPanel.jsx` expects the following fields from issues:

**Core Fields:**
- `id` - unique issue identifier
- `track` - 'A'|'B'|'C' (Rigor/Clarity/Counterpoint)
- `severity` - 'major'|'minor'
- `title` - issue title
- `message` - issue description
- `paragraph_id` - target paragraph
- `section_id` - target section

**Track A/B Fields:**
- `suggested_rewrite` - proposed text replacement
- `rationale` - explanation of the issue

**Track C Fields:**
- `critique` - critical analysis
- `category` - issue category
- `addressable` - whether issue can be addressed

This matches the backend's issue schema exactly.

## Testing Status

### What Should Work
1. **Static Demo Mode:**
   - Loads fixtures from `/public/fixtures/`
   - Attempts to load review from `/public/reviews/`
   - Falls back to empty issues array if no review file exists
   - Shows console warning when no issues found

2. **Dynamic Mode:**
   - Uses backend-provided issues from `reviewResult.issues`
   - No mock generation needed

### What To Test
1. Load a static demo without a review file → should show empty issues panel
2. Load a static demo with a review file → should show real issues
3. Dynamic mode with backend → should use backend issues

## Files Modified
- `frontend-d2/src/context/DocumentContext.jsx`

## Files NOT Modified
- `IssuesPanel.jsx` - Already handles correct schema
- `ProcessScreen.jsx` - API call structure is correct
- Fixture files in `/public/fixtures/`
- Review files in `/public/reviews/`

## Impact
- **Lines removed:** ~240 lines
- **Dependencies removed:** None (no external dependencies)
- **Breaking changes:** None (API contract unchanged)
- **Performance:** Slight improvement (no mock generation overhead)

## Next Steps
1. Test frontend with empty issues array
2. Test with real backend integration
3. Monitor for console errors during demo selection