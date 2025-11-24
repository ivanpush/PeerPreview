# Frontend Integration Notes - Pipeline Refactor

**Date:** 2024-11-22
**Status:** Backend Ready, Frontend Needs Update

---

## Backend Status: ✅ READY

The backend has been updated and is running successfully with the refactored pipeline.

### Working Endpoints

#### 1. Upload Endpoint
```bash
POST /upload
```
**Status:** ✅ Working
**Test Result:** Successfully uploaded test2.pdf and parsed with refactored pipeline

#### 2. Pipeline Stages Debug Endpoint
```bash
GET /debug/pipeline-stages/{document_id}
```
**Status:** ✅ Working
**Returns:** All 12 pipeline stages with updated labels

**Current Stages Returned:**
```json
{
  "document_id": "...",
  "stages": [
    {
      "id": "01_raw_pdf",
      "label": "1. Raw PDF Text",
      "content": "..."
    },
    {
      "id": "02_analyze_structure",
      "label": "2. Structure Analysis (Title, Abstract, Sections)",
      "content": "Title: ...\nAbstract: ...\nSections found: 7"
    },
    {
      "id": "03_geometric_cleaning",
      "label": "3. Geometric Cleaning (Crop + Caption Detection + Figure Detection)",
      "content": "Cropped text:\n...\n\nCaptions detected (on cropped pages): 8\nFigure regions detected: 8"
    },
    {
      "id": "04_extract_markdown",
      "label": "4. Extract Markdown (with Figure Filtering)",
      "content": "..."
    },
    // ... stages 5-12
  ]
}
```

---

## What Changed in the Pipeline

### Stage Key Updates

**BEFORE (Old Frontend Expected):**
- `03_after_crop` - After Geometric Crop

**AFTER (What Backend Returns Now):**
- `03_geometric_cleaning` - Geometric Cleaning (Crop + Caption Detection + Figure Detection)

### Stage 3 Content Updates

**BEFORE:**
```
Cropped text:
[... cropped text ...]
```

**AFTER:**
```
Cropped text:
[... cropped text ...]

Captions detected (on cropped pages): 8
Figure regions detected: 8
```

**New Info Available:**
- Number of captions detected (after footer removal)
- Number of figure regions detected (for garbage filtering)

---

## Frontend Updates Needed

### Issue: Stage ID Mismatch

The frontend likely looks for stage ID `03_after_crop`, but backend now returns `03_geometric_cleaning`.

**Frontend files to check:**
- Any component that renders pipeline stages
- Any component expecting stage IDs
- Stage navigation/selection logic

### Recommended Changes

#### 1. Update Stage ID Mapping

If frontend has hardcoded stage IDs:
```typescript
// BEFORE
const stageIds = [
  '03_after_crop',
  // ...
];

// AFTER
const stageIds = [
  '03_geometric_cleaning',
  // ...
];
```

#### 2. Use Dynamic Stage Labels

Better approach - use labels from backend response:
```typescript
// Fetch stages
const response = await fetch(`/debug/pipeline-stages/${docId}`);
const data = await response.json();

// Use dynamic labels
data.stages.forEach(stage => {
  console.log(stage.label); // "3. Geometric Cleaning (...)"
  console.log(stage.content); // actual content
});
```

#### 3. Display New Metadata

Stage 3 now includes caption/figure counts. Frontend can parse and display:
```typescript
// Parse stage 3 content
const stage3 = stages.find(s => s.id === '03_geometric_cleaning');
const content = stage3.content;

// Extract metadata
const captionMatch = content.match(/Captions detected.*: (\d+)/);
const regionMatch = content.match(/Figure regions detected: (\d+)/);

if (captionMatch && regionMatch) {
  displayMetadata({
    captions: parseInt(captionMatch[1]),
    figureRegions: parseInt(regionMatch[1])
  });
}
```

#### 4. Add Visual Indicators

Show that Stage 3 now does more:
```
Stage 3: Geometric Cleaning
  ✓ Margins cropped
  ✓ 8 captions detected (footer-free)
  ✓ 8 figure regions identified
  → Ready for figure garbage filtering
```

---

## Testing the Integration

### 1. Start Backend (if not running)
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### 2. Test Upload
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@backend/docs/testPDFs/test2.pdf"
```

Expected response:
```json
{
  "document_id": "...",
  "title": "Elastomeric sensor surfaces...",
  "sections": ["preamble", "introduction", ...],
  "message": "Document uploaded and parsed successfully"
}
```

### 3. Test Pipeline Stages
```bash
curl "http://localhost:8000/debug/pipeline-stages/{document_id}"
```

Expected: 12 stages with proper labels and content

### 4. Verify Stage 3 Content
Should include:
- Cropped text
- "Captions detected (on cropped pages): X"
- "Figure regions detected: X"

---

## Frontend Checklist

- [ ] Update stage ID from `03_after_crop` to `03_geometric_cleaning`
- [ ] Update stage labels to match backend (or fetch dynamically)
- [ ] Parse and display caption count from Stage 3
- [ ] Parse and display figure region count from Stage 3
- [ ] Test navigation between stages
- [ ] Test with multiple PDFs to ensure all work
- [ ] Update any documentation referencing old stage names

---

## Backward Compatibility

If you need to support old pipeline temporarily:

```typescript
// Handle both old and new stage IDs
const getStage3 = (stages) => {
  return stages.find(s =>
    s.id === '03_geometric_cleaning' ||  // New
    s.id === '03_after_crop'             // Old
  );
};
```

---

## Additional Endpoints Available

### Health Check
```bash
GET /health
```

### Get Document Details
```bash
GET /document/{document_id}
```

### List All Documents (Debug)
```bash
GET /debug/documents
```

---

## Next Steps

1. **Update frontend stage IDs** to match new backend
2. **Test end-to-end** with a test PDF upload
3. **Verify stage navigation** works correctly
4. **Add metadata display** for caption/figure counts (optional but nice)
5. **Deploy** when frontend updates complete

---

## Contact

If you encounter issues:
- Check backend logs: Backend should log at INFO level
- Check browser console: Frontend errors will show there
- Verify stage IDs match between frontend and backend
- Test `/debug/pipeline-stages/{doc_id}` endpoint directly

---

**Status:** Backend is production-ready, frontend needs stage ID updates.
