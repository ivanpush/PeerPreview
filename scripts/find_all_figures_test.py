"""Find all figure references in test.pdf to understand what we're missing."""

import sys
import pymupdf
from pathlib import Path

sys.path.insert(0, '..')

pdf_path = Path('../../docs/testPDFs/test.pdf')
doc = pymupdf.open(pdf_path)

print('Searching all pages for Figure/Table captions:')
print('='*80)

for page_num, page in enumerate(doc):
    blocks = page.get_text('dict')['blocks']

    for i, block in enumerate(blocks):
        if block.get('type') != 0:
            continue

        text = ''
        for line in block.get('lines', []):
            for span in line.get('spans', []):
                text += span.get('text', '')

        text = text.strip()

        # Look for caption patterns at start of text
        import re
        if re.match(r'^(Figure|Fig\.?|Table)\s+\d+', text, re.IGNORECASE):
            bbox = block['bbox']

            # Check if bold
            is_bold = False
            for line in block.get('lines', []):
                for span in line.get('spans', []):
                    font = span.get('font', '').lower()
                    flags = span.get('flags', 0)
                    if (flags & 16) or 'bold' in font:
                        is_bold = True
                        break

            print(f'Page {page_num + 1}, Block {i}:')
            print(f'  Pattern: {text[:80]}...')
            print(f'  Bold: {is_bold}')
            print(f'  BBox height: {bbox[3] - bbox[1]:.1f}pt')
            print(f'  Full text length: {len(text)} chars')
            print()

doc.close()
