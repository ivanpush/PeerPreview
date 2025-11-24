
---

# PHASE 3 — TITLE DETECTION

If no keyword-based title is found:

### Candidate selection:
- Page 1 only
- Blocks in top 30% of page height
- Prefer bold_large; fallback to regular_large

### Multi-line assembly rules:
Blocks belong to the title if:
- font_size difference < 1.5 pt
- |x0 difference| < 15 px
- vertical gap < 1.5 × current block's font size
- block does NOT include affiliation-like content:
  - university, department, institute
  - city, country, email, commas separating names

Concatenate until a stopping condition is hit.

detection_method:
- "heuristic_bold" if bold
- "heuristic_location" if not bold

confidence:
- 1.0 if bold_large in top 20%
- 0.9 if large in top 30%
- 0.7 if based only on location

---

# PHASE 4 — AUTHORS DETECTION

If not detected via keywords:

Location heuristics:
- Immediately below the title
- Same page
- Vertical gap < 3× title font size

Content heuristics:
- Contains multiple commas separating tokens
- Contains superscripts 1,2,3 or a,b,c or *
- Tokens look like names: capitalized pairs: “First Last” or “F. Last”

Multi-line assembly:
- Same font size ±1 pt
- Same alignment ±15 px
- Stop when affiliations-like content appears

Confidence = base 0.8 × modifiers.

---

# PHASE 5 — AFFILIATIONS DETECTION

If no keyword match:

Look for:
- University, Department, Institute, Center
- geographic locations
- email addresses
- postal codes
- superscripts matching authors

Assemble multilines with same-size font.

Stopping conditions:
- Abstract header
- Two-column transition
- Large vertical gap

Confidence based on keyword strength & alignment.

---

# PHASE 6 — ABSTRACT DETECTION (Fallback)

If no keyword:

Find first full paragraph after (title → authors → affiliations).

Constraints:
- 100–350 words
- Contains multiple sentences
- Appears before first two-column split (if present)
- Does NOT contain institutional/author-like patterns

Ends when:
- next bold header appears
- "Keywords:" line appears
- next section begins

Confidence ~ 0.7–0.9.

---

# PHASE 7 — INTRODUCTION DETECTION (Fallback)

If no keyword:

Definition:
- The FIRST major body section after abstract & keywords.

Detection:
- First bold_medium or regular_large block after abstract
- OR first block with header-like typography

detection_method = "heuristic_location"
confidence ~ 0.6–0.85.

---

# PHASE 8 — NON-BOLD HEADERS

If <3 sections identified, scan for:
- ALL CAPS headers
- Numbered headers (“1. INTRODUCTION”)
- Larger font blocks with header-like format

Normalize via same algorithm as in Phase 2.

---

# PHASE 9 — SECTION CONTENT EXTRACTION

For each detected header:
- Sort all headers by (page, y)
- Section content begins immediately after header bbox
- Ends immediately before next header
- Include blocks that overlap >50% vertically with section region

Exclude:
- figure captions starting with “Figure X”
- table captions
- footnotes
- page numbers
- headers/footers

Apply column-aware reading order:
- On 2-column pages: read left column fully, then right

Apply de-hyphenation and paragraph reconstruction.

---

# PHASE 10 — FIGURES AND TABLES

Identify captions:
- Text starting with: “Figure X”, “Fig. X”, “Table X”

Store:
{
  "id": "Figure 3",
  "caption": "...",
  "page": <page>,
  "bounding_box": [...]
}

Confidence:
- 1.0 if bold and matched keyword
- 0.8 otherwise

---

# PHASE 11 — EDGE CASE HANDLING

Combined sections:
- “Results and Discussion” → fill both OR treat as one; note it in parsing_notes.

References end detection:
Scan from back of document upward until:
- Text no longer matches reference patterns (Author, year, journal)

Ambiguous blocks:
- Move to other_sections with notes

---

# PHASE 12 — UNPARSED CONTENT

Any block not:
- inside a section
- a figure/table caption
- a header
Goes to unparsed_content with location info.

---

# END OF PROMPT
