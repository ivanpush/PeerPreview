"""Analyze Fig 7 block structure to find why it's truncating."""

import sys
from pathlib import Path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

import pymupdf
from services.parser.pipeline.stages.geometry import crop_margins, detect_footer_height
from services.parser.pipeline.config import GeometryConfig

doc = pymupdf.open(backend_dir / 'docs/testPDFs/test2.pdf')

print(f"BEFORE CROPPING:")
print(f"  Page 7 height: {doc[6].rect.height:.1f}pt\n")

# Apply cropping like the real pipeline
config = GeometryConfig()
bottom = detect_footer_height(doc)
print(f"Footer detection: {bottom}pt bottom margin\n")

doc = crop_margins(doc, top=60, bottom=bottom, left=0)

print(f"AFTER CROPPING:")
print(f"  Page 7 visible area: y0={doc[6].cropbox.y0:.1f} to y1={doc[6].cropbox.y1:.1f}")
print(f"  (cropbox height: {doc[6].cropbox.height:.1f}pt)\n")

page = doc[6]  # Page 7 AFTER cropping

blocks = page.get_text('dict')['blocks']
text_blocks = []
for b in blocks:
    if b.get('type') == 0:
        bbox = b['bbox']
        text = ''.join(span.get('text','') for line in b.get('lines',[]) for span in line.get('spans',[])).strip()
        text_blocks.append({
            'y0': bbox[1],
            'y1': bbox[3],
            'x0': bbox[0],
            'x1': bbox[2],
            'text': text,
            'lines': len(b.get('lines', []))
        })

text_blocks.sort(key=lambda x: x['y0'])

print("Searching for Fig 7 caption...\n")
fig7_start = None
for i, b in enumerate(text_blocks):
    # Search all blocks for Fig 7
    if 'Fig. 7' in b['text'] or 'Figure 7' in b['text']:
        print(f">>> FOUND FIG 7 at Block {i}: y={b['y0']:.1f}-{b['y1']:.1f}")
        print(f"    Text: {b['text'][:200]}...\n")
        fig7_start = i

print("\nNow showing blocks around Fig 7:\n")
if fig7_start is not None:
    for i in range(max(0, fig7_start - 1), min(len(text_blocks), fig7_start + 15)):
        b = text_blocks[i]

        if i == fig7_start:
            print(f"\n{'='*80}")
            print(f">>> FIG 7 CAPTION STARTS HERE (Block {i}) <<<")
            print(f"{'='*80}")

        print(f"\nBlock {i}: y={b['y0']:.1f}-{b['y1']:.1f}, x={b['x0']:.1f}-{b['x1']:.1f}")
        print(f"  Lines: {b['lines']}")
        print(f"  Text: {b['text'][:120]}...")

        # Check gap to next block
        if i < len(text_blocks) - 1:
            next_b = text_blocks[i+1]
            gap = next_b['y0'] - b['y1']
            h_overlap = (min(b['x1'], next_b['x1']) - max(b['x0'], next_b['x0'])) / max(b['x1'] - b['x0'], 1)
            print(f"  → Gap to next: {gap:.1f}pt, H-overlap: {h_overlap:.2f}")

            # Check continuation criteria
            if i >= fig7_start:
                if gap > 20:
                    print(f"  ⚠️  WOULD STOP: Gap too large ({gap:.1f}pt > 20pt)")
                elif h_overlap < 0.5:
                    print(f"  ⚠️  WOULD STOP: H-overlap too low ({h_overlap:.2f} < 0.5)")
                else:
                    print(f"  ✓ Would continue")
else:
    print("ERROR: Fig 7 not found!")

doc.close()
