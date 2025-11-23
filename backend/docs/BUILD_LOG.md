# Build Log

## 2025-11-22: Enhanced Figure Caption Detection

### Feature: Comprehensive Caption Detection with Multi-line Support

Implemented robust figure caption detection in the PDF parser to accurately extract captions while filtering out inline text references and figure artifacts.

### Changes Made:

#### Caption Detection (Stage 2: Analysis)

**File:** `backend/services/parser/pipeline/stages/analysis.py`

1. **Multi-line caption accumulation for Word-to-PDF documents:**
   - Added `get_block_font_size()`: Extract average font size from block
   - Added `is_continuation_block()`: Detect caption continuation blocks by checking:
     - Vertical gap < 20pt from previous block
     - Similar font size (within 1pt)
     - No new caption pattern at start
   - Updated `detect_caption_in_block()`: Accumulates continuation blocks into single caption
   - Updated `detect_captions()`: Tracks consumed blocks to skip already-processed continuations

2. **Improved standalone vs inline caption detection:**
   - Simplified `is_standalone_caption()` logic:
     - Checks if block text STARTS with caption pattern (not embedded mid-sentence)
     - Rejects inline indicators: "as shown in", "see Figure", "(Figure X)", etc.
     - Rejects verb patterns: "Figure X shows/demonstrates/presents/indicates/suggests"
     - Fixed regex to handle letter suffixes (e.g., "10b", "2A"): `\d+[a-z]?`
   - Removed complex span-by-span analysis that was incorrectly rejecting valid captions

3. **Caption pattern matching:**
   - Supports: "Figure", "Fig", "Fig.", "Table", "Scheme"
   - Handles numbered figures with optional letter suffixes: "1", "2A", "10b", "S3"
   - Normalizes whitespace before pattern matching

#### Testing & Validation

**Created diagnostic scripts:**
- `find_all_figures_test.py`: Finds all caption patterns in test.pdf (found 13 total: 11 real + 2 false positives)
- `extract_captions.py`: Extracts and saves captions from all test PDFs to JSON/Markdown

**Test Results (7 PDFs, 52 total captions):**
- **test.pdf** (Word-to-PDF manuscript): 11 captions
  - Fixed: Multi-line captions now fully captured (was only getting first line)
  - Fixed: Rejected false positives "Figure 3 shows..." and "Fig 10b shows..."
  - Previously: 4/13 captions (missing 80%), 1 false positive
  - Now: 11/11 real captions (100%), 0 false positives ✓
- **test2.pdf** (journal article): 8 captions ✓
- **test3.pdf** (split-column edge case): 7 captions (partial captions accepted as designed) ✓
- **test4.pdf**: 7 captions ✓
- **test5.pdf**: 5 captions ✓
- **test6.pdf**: 6 captions ✓
- **test7.pdf** (dash-separated captions): 8 captions ✓

#### Bug Fixes:

1. **Multi-line caption truncation**: Word-generated PDFs split long captions across 6-20 blocks with ~6pt gaps. Now accumulates all continuation blocks.
   - Example: Figure 2 caption grew from 80 chars (first line only) → 1427 chars (full caption, 16 blocks)

2. **False positive inline references**: Rejected patterns like "Figure 3 shows the distribution..." which are body text, not captions.
   - Regex bug: `\d+` didn't match "10b" - fixed to `\d+[a-z]?`

3. **Missing 80% of captions**: Overly complex `is_standalone_caption()` logic was rejecting valid captions.
   - Simplified to block-level check instead of span-by-span analysis

### Files Modified:

- `backend/services/parser/pipeline/stages/analysis.py`: Caption detection logic (+200 lines)
- `backend/services/parser/pipeline/stages/figures.py`: Figure region detection (fixed unhashable FigureCaption bug)
- `backend/services/parser/pipeline/models.py`: Added FigureCaption and FigureRegion dataclasses
- `backend/services/parser/pipeline/PIPELINE_FLOW.md`: Updated Stage 2 documentation

### Output:

Captions saved to: `backend/docs/testPDFs/caption_extracts/captions_20251122_130637.json` and `.md`

### Strategy:

Progressive narrowing through systematic testing:
1. Test logic in isolation with minimal cases
2. Test on real data to find gaps
3. Identify which edge cases escaped
4. Debug at point of failure (test exact function)
5. Fix pattern and verify no regressions

---

## 2025-11-21: Pipeline Stage Debug Viewer

### Feature: Interactive Pipeline Stage Navigation

Added ability to view intermediate outputs of each pipeline stage in the frontend for debugging purposes.

### Changes Made:

#### Backend Changes:

1. **Modified `PipelineBuilder` class** (`backend/services/parser/pipeline/builder.py`):
   - Added `capture_stages` parameter to constructor (default: `False`)
   - Added `self.stage_outputs` dict to store intermediate stage outputs
   - Wrapped all stage output captures with `if self.capture_stages:` to make it toggleable
   - Captured outputs for stages 2-12:
     - Stage 2: Analyze Structure (metadata summary)
     - Stage 3: Geometric Cleaning (geometry info)
     - Stage 4: Extract Markdown (raw markdown)
     - Stage 5: Reflow Text (reflowed markdown)
     - Stage 6: Cleanup Artifacts (cleaned markdown)
     - Stage 7: Inject Section Labels (labeled markdown)
     - Stage 8: Split Sections (sections summary)
     - Stage 9: Validate Sections (validation results)
     - Stage 10: Index Sentences (sentence counts)
     - Stage 11: Extract Metadata (metadata counts)
     - Stage 12: Final Output (final markdown)

2. **Modified `main.py`**:
   - Added `builders_store` dict to store builder instances with stage outputs
   - Modified `/upload` endpoint to instantiate `DocumentBuilder(capture_stages=True)`
   - Store builder instance in `builders_store[doc_id]` for later retrieval
   - Added `/debug/pipeline-stages/{document_id}` endpoint:
     - Returns all captured stage outputs with labels
     - Only accessible when `settings.debug = True`
     - Returns 404 if document not found or stages not captured
   - Updated `/debug/clear` to also clear `builders_store`

#### Frontend Changes:

1. **Modified `DocumentViewer` component** (`frontend/components/document-viewer.tsx`):
   - Added `documentId` prop to receive document ID
   - Added state management for pipeline stages:
     - `stages`: Array of pipeline stage data
     - `currentStageIndex`: Index of currently displayed stage (-1 = final output)
     - `isLoadingStages`: Loading state
   - Added `useEffect` hook to fetch stages from `/debug/pipeline-stages/{documentId}`
   - Added navigation handlers:
     - `handlePrevStage()`: Navigate to previous stage
     - `handleNextStage()`: Navigate to next stage
     - `handleShowFinal()`: Jump back to final output
   - Modified display logic to show either stage content or final markdown
   - Added pipeline navigation UI:
     - Left/right arrow buttons for stage navigation
     - Current stage label and position indicator (e.g., "Stage 4: Extract Markdown (4 / 12)")
     - "Show Final" button to jump back to final output
     - Disabled state for arrows at boundaries
     - Only visible when stages are loaded

2. **Modified `page.tsx`** (`frontend/app/page.tsx`):
   - Added `documentId` prop when rendering `DocumentViewer`

### Usage:

1. Start backend with debug mode enabled
2. Upload a PDF document
3. View the document in the frontend
4. Use the arrow navigation controls at the top to step through pipeline stages:
   - Click left arrow to go to previous stage
   - Click right arrow to go to next stage
   - Click "Show Final" to return to the final output
5. The displayed markdown updates to show the output at each stage

### Purpose:

This feature enables debugging of the PDF parsing pipeline by allowing developers to:
- Identify at which stage parsing issues occur
- Compare outputs between stages to see transformations
- Validate that each stage is working correctly
- Diagnose problems with specific PDFs

### Configuration:

- **Toggleable**: Set `capture_stages=False` in `DocumentBuilder` constructor to disable (no performance impact)
- **Debug-only**: Frontend endpoint only works when backend `settings.debug = True`
- **In-memory**: Stage outputs stored in memory (cleared on server restart)

### Performance Considerations:

- Stage capture is toggleable via `capture_stages` parameter
- When disabled (`capture_stages=False`), no performance impact
- When enabled, minimal memory overhead (stores ~11 string outputs per document)
- Stage outputs cleared when calling `/debug/clear` endpoint
