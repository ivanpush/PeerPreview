"""Examine test.pdf caption structure to understand multi-line issue."""

import sys
import pymupdf
from pathlib import Path

sys.path.insert(0, '..')

pdf_path = Path('../../docs/testPDFs/test.pdf')
doc = pymupdf.open(pdf_path)

# Look at page 4 (index 4) where we know Figure 2 is
page = doc[4]
blocks = page.get_text('dict')['blocks']

print('Page 4 text blocks (looking for Figure 2):')
print('='*80)

found_figure = False
for i, block in enumerate(blocks):
    if block.get('type') != 0:  # Skip non-text
        continue

    # Get text
    text = ''
    for line in block.get('lines', []):
        for span in line.get('spans', []):
            text += span.get('text', '')

    text = text.strip()

    # Show Figure 2 and next 5 blocks
    if 'Figure 2' in text:
        found_figure = True

    if found_figure and i < 100:  # Show next blocks
        bbox = block['bbox']

        # Check font info
        font_info = []
        for line in block.get('lines', []):
            for span in line.get('spans', []):
                font_info.append(f"{span.get('font', 'unknown')} {span.get('size', 0):.1f}pt")

        print(f'Block {i}:')
        print(f'  Text: {text[:150]}{"..." if len(text) > 150 else ""}')
        print(f'  BBox: y0={bbox[1]:.1f}, y1={bbox[3]:.1f}, height={bbox[3]-bbox[1]:.1f}pt')
        print(f'  Fonts: {", ".join(set(font_info))}')

        # Calculate gap to next block
        if i + 1 < len(blocks) and blocks[i+1].get('type') == 0:
            next_bbox = blocks[i+1]['bbox']
            gap = next_bbox[1] - bbox[3]
            print(f'  Gap to next: {gap:.1f}pt')
        print()

        # Stop after showing 10 blocks
        if found_figure and (i - [j for j, b in enumerate(blocks) if 'Figure 2' in str(b)][ 0]) > 8:
            break

doc.close()
