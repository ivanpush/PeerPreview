# Caption Detection Refactor Plan: Two-Pass Approach

## Problem Statement
Caption detection currently happens in Stage 2 (analysis.py) BEFORE geometry cropping in Stage 3. This causes footer/header text to be incorrectly merged with captions when they appear at page boundaries.

Example: A figure caption at the bottom of a page picks up "bioRxiv preprint" footer text.

## Root Cause
Order of operations issue:
1. Stage 2 detects captions on UNCROPPED pages (with headers/footers)
2. Stage 3 crops margins/footers (too late)
3. Caption list already contaminated with footer text

## Solution: Two-Pass Caption Detection

### Overview
Split caption detection into two passes:
- **Pass 1:** Detect bold spans only (Stage 2)
- **Pass 2:** Detect captions on cropped pages (Stage 3)

### Detailed Flow

#### Stage 2: Analysis (MODIFIED)
```python
analyze_structure() returns StructureInfo:
  - bold_spans: List[BoldSpan] ✓ (keep as-is)
  - title: str ✓ (keep as-is)
  - abstract: str ✓ (keep as-is)
  - section_headers: List[SectionHeader] ✓ (keep as-is)
  - figure_captions: List[FigureCaption] ✗ (REMOVE - move to Stage 3)
```

#### Stage 3: Geometry + Figures (MODIFIED)
```python
apply_geometric_cleaning() now does:
  1. Crop margins/headers/footers (existing)
  2. Detect line numbers (existing)
  3. NEW: Detect captions on CROPPED pages
  4. Detect figure regions using captions (existing)
  5. Return GeometryInfo with both captions AND regions
```

### Implementation Steps

#### Phase 1: Refactor Stage 2 (analysis.py)
1. Remove `_detect_figure_captions()` method
2. Remove `figure_captions` from StructureInfo initialization
3. Keep all other analysis logic unchanged
4. Update tests to not expect captions from Stage 2

#### Phase 2: Refactor Stage 3 (geometry.py)
1. Add caption detection after cropping:
   ```python
   def apply_geometric_cleaning(doc, config, structure_info):
       # Step 1: Existing geometry analysis
       geom_info = _analyze_geometry(doc, config)

       # Step 2: Apply crops
       _apply_crops(doc, geom_info)

       # Step 3: NEW - Detect captions on cropped pages
       figure_captions = _detect_figure_captions(doc, structure_info.bold_spans)

       # Step 4: Existing figure detection
       figure_regions = detect_figures(doc, figure_captions, config)

       # Step 5: Store both in GeometryInfo
       geom_info.figure_captions = figure_captions
       geom_info.figure_regions = figure_regions

       return doc, geom_info
   ```

2. Move `_detect_figure_captions()` from analysis.py to geometry.py
3. Update method to work with cropped pages:
   - Use cropped page dimensions
   - Adjust bbox coordinates if needed

#### Phase 3: Update Data Flow
1. Modify `models.py`:
   - Remove `figure_captions` from StructureInfo
   - Add `figure_captions` to GeometryInfo

2. Update `extraction.py`:
   - Get captions from `geom_info.figure_captions` instead of `structure_info.figure_captions`
   - No logic changes needed

3. Update `builder.py`:
   - Pass captions from geom_info to extraction stage
   - Update stage capture for debugging

#### Phase 4: Update Tests
1. Create test case with problematic PDF (caption at page bottom)
2. Verify footer text no longer appears in captions
3. Update existing tests for new data flow
4. Add regression test for this specific issue

### Benefits of This Approach

1. **Minimal Disruption:** Only moves caption detection, everything else stays the same
2. **Clean Separation:** Analysis stays focused on structure, geometry handles spatial elements
3. **Accurate Captions:** No more footer/header contamination
4. **Maintains Performance:** Still single pass through document

### Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Bold spans might have different coordinates after cropping | Recalculate bbox relative to crop margins |
| Caption detection might miss captions split by crop | Unlikely - captions are inside margins |
| Breaking existing code that expects captions in StructureInfo | Update all references (extraction.py mainly) |

### Testing Strategy

1. **Unit Tests:**
   - Test caption detection on cropped pages
   - Test caption-figure pairing still works
   - Test extraction gets correct captions

2. **Integration Tests:**
   - Run all test PDFs through pipeline
   - Check for footer text in captions
   - Verify caption count unchanged
   - Check figure filtering still works

3. **Specific Test Case:**
   - Create PDF with caption at very bottom of page
   - Add footer text that would previously merge
   - Verify clean caption extraction

### Rollback Plan
If issues arise:
1. Keep both caption detection methods temporarily
2. Add config flag: `use_cropped_caption_detection: true/false`
3. Default to new method, allow fallback to old

### Implementation Order
1. Create feature branch: `fix/caption-footer-contamination`
2. Implement Phase 1 (remove from analysis.py)
3. Implement Phase 2 (add to geometry.py)
4. Update data flow (Phase 3)
5. Run test suite
6. Test on all PDFs in testPDFs/
7. Update PIPELINE_FLOW.md
8. Merge to main

### Estimated Time
- Refactoring: 2-3 hours
- Testing: 1-2 hours
- Documentation: 30 minutes
- Total: ~4-5 hours

### Success Criteria
- [ ] No footer/header text in captions
- [ ] Caption count remains same or improves
- [ ] All existing tests pass
- [ ] Figure filtering still works correctly
- [ ] No performance regression

### Notes
- Consider caching cropped page dimensions for coordinate transformation
- May want to add debug logging for caption bbox adjustments
- Could extend to detect table captions simultaneously

---

## Decision Record
**Date:** 2024-11-22
**Decision:** Use Option A (Two-Pass Caption Detection)
**Rationale:** Minimal refactoring while solving the core issue
**Approver:** [TBD]