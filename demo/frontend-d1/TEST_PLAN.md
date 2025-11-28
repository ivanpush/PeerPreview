# Test Plan for Review Screen Updates

## Summary of Changes
All requested features have been successfully implemented in the demo/frontend-d1 review screen:

### 1. User Edits Tracking
- ✅ Added `userEdits` Map to ManuscriptContext to track all manual edits and deletions
- ✅ Created `UserEditCard` component with diff view functionality
- ✅ Added "User Edits" section to IssuesPanel between Accepted and Dismissed sections
- ✅ User edits are automatically tracked when paragraphs are edited or deleted
- ✅ Edits can be reverted to original text from the User Edits section

### 2. Issue State Management
- ✅ Accepted and dismissed issues no longer appear as inline flags in the manuscript
- ✅ Only active issues (not accepted/dismissed) show as inline annotations
- ✅ Recalled issues maintain their original position in the list (not moved to top)

### 3. UI Improvements
- ✅ Suggested rewrite display is now expandable with "See more/See less" toggle
- ✅ Long rewrites (>180 chars) show truncated with expansion option
- ✅ User Edits section is collapsible with chevron indicator

### 4. Export Functionality
- ✅ Export button now functional - downloads JSON with complete review data
- ✅ Export includes:
  - All accepted issues (marked if rewrite was applied)
  - All dismissed issue IDs
  - Complete user edits history with diffs
  - Updated manuscript with edit status for each paragraph
  - Statistics (total/edited/rewritten/deleted paragraphs)

## Testing Instructions

### Test 1: User Edits Tracking
1. Navigate to http://localhost:5176/review
2. Click "Edit" button on any paragraph
3. Make changes and save
4. Verify edit appears in "User Edits" section
5. Expand the edit card to see diff view
6. Click "Revert to Original" and verify paragraph is restored

### Test 2: Delete Tracking
1. Edit a paragraph and click "Delete"
2. Verify deleted paragraph shows strikethrough
3. Check "User Edits" section shows DELETED tag
4. Click "Restore" on deleted paragraph
5. Verify it's removed from User Edits

### Test 3: Issue Filtering
1. Click "Accept" on any issue
2. Verify the inline flag disappears from manuscript
3. Check issue appears in "Accepted" section
4. Click "Recall" to bring it back
5. Verify issue returns to original position (not top)

### Test 4: Dismiss Filtering
1. Click "Dismiss" (X) on any issue
2. Verify inline flag disappears
3. Check issue appears in "Dismissed" section
4. Click "Undo" to restore
5. Verify issue returns to main list at original position

### Test 5: Suggested Rewrite Expansion
1. Find an issue with a long suggested rewrite
2. Expand the issue card
3. Look for "See more" link next to "Suggested Rewrite"
4. Click to expand full text
5. Click "See less" to collapse

### Test 6: Export Function
1. Make some edits, accept issues, dismiss others
2. Click "Export" button in header
3. Verify JSON file downloads
4. Open file and verify it contains:
   - acceptedIssues array
   - dismissedIssues array
   - userEdits array with all manual changes
   - manuscript with paragraph statuses
   - metadata with counts

### Test 7: Combined Workflow
1. Accept an issue with rewrite
2. Manually edit another paragraph
3. Delete a third paragraph
4. Dismiss an issue
5. Export the review
6. Verify all changes are captured in export

## Browser Console
Check for any errors in browser console (F12 > Console tab)

## Known Working State
- Development server running on http://localhost:5176/
- All components compile without errors
- No TypeScript/JavaScript errors in console
- Export generates valid JSON

## Files Modified
1. `/src/context/ManuscriptContext.jsx` - Added userEdits tracking and export function
2. `/src/components/UserEditCard.jsx` - New component for displaying edits
3. `/src/components/IssuesPanel.jsx` - Added User Edits section, fixed rewrite display
4. `/src/components/ManuscriptView.jsx` - Filter accepted/dismissed from inline flags
5. `/src/pages/ReviewScreen.jsx` - Connected Export button to function

## Success Criteria
✅ All user edits are tracked and displayed
✅ Accepted/dismissed issues don't show inline
✅ Recalled issues maintain position
✅ Suggested rewrites are expandable
✅ Export includes all review data
✅ No console errors or warnings