"""Inspect page 7 structure to understand caption+footer layout."""

import pymupdf
from pathlib import Path

pdf_path = Path('/Users/ivanforcytebio/Projects/PeerPreview/backend/docs/testPDFs/test2.pdf')
doc = pymupdf.open(pdf_path)

page = doc[7]  # Page 7 (0-indexed)
blocks = page.get_text("dict")["blocks"]

print("="*80)
print("Page 7 Text Blocks (bottom 5):")
print("="*80)

text_blocks = []
for b in blocks:
    if b["type"] == 0:
        y0, y1 = b["bbox"][1], b["bbox"][3]
        text = "".join(
            span.get("text", "")
            for line in b.get("lines", [])
            for span in line.get("spans", [])
        ).strip()
        line_count = len(b.get("lines", []))
        text_blocks.append({
            'y0': y0,
            'y1': y1,
            'text': text,
            'lines': line_count,
            'height': y1 - y0
        })

# Sort and show bottom 5
text_blocks.sort(key=lambda x: x['y0'])
print(f"\nTotal text blocks: {len(text_blocks)}")
print(f"Page height: {page.rect.height}")
print("\nBottom 5 blocks:\n")

for i, block in enumerate(text_blocks[-5:], 1):
    print(f"{i}. Y-position: {block['y0']:.1f} - {block['y1']:.1f}")
    print(f"   Lines: {block['lines']}, Height: {block['height']:.1f}pt")
    print(f"   Text ({len(block['text'])} chars):")
    if len(block['text']) > 200:
        print(f"   START: {block['text'][:100]}")
        print(f"   END: ...{block['text'][-100:]}")
    else:
        print(f"   {block['text']}")
    print()

doc.close()
