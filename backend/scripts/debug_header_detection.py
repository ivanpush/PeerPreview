"""Debug header detection on page 1."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pymupdf
from services.parser.pipeline.stages.geometry import detect_header_height

pdf_path = Path('/Users/ivanforcytebio/Projects/PeerPreview/backend/docs/testPDFs/test2.pdf')
doc = pymupdf.open(pdf_path)

page1 = doc[0]

# Get all text blocks
blocks = page1.get_text("dict")["blocks"]

print("TEXT BLOCKS ON PAGE 1 (top 10):")
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
        text_blocks.append((y0, y1, text))

text_blocks.sort()

for i, (y0, y1, text) in enumerate(text_blocks[:10]):
    print(f"{i+1}. Y={y0:.1f}-{y1:.1f} ({y1-y0:.1f}pt): {text[:60]}")

# Test header detection
detected_top = detect_header_height(page1, is_first_page=True)
print(f"\n{'='*80}")
print(f"DETECTED TOP MARGIN: {detected_top:.0f}pt")
print(f"{'='*80}")

# Show what would be cropped
print(f"\nWould crop from Y=0 to Y={detected_top:.0f}")
print(f"Blocks that would be REMOVED:")
for y0, y1, text in text_blocks:
    if y1 <= detected_top:
        print(f"  - Y={y0:.1f}-{y1:.1f}: {text[:60]}")
    else:
        break

print(f"\nFirst block that would REMAIN:")
for y0, y1, text in text_blocks:
    if y0 >= detected_top:
        print(f"  - Y={y0:.1f}-{y1:.1f}: {text[:60]}")
        break

doc.close()
