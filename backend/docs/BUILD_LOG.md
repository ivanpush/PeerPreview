# Build Log

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
