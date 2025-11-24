"""Check footer detection on test2.pdf page 7."""

import sys
from pathlib import Path

backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

import pymupdf
import re


def check_footer():
    """Check what footer detection sees on test2.pdf page 7."""

    pdf_path = backend_dir / "docs" / "testPDFs" / "test2.pdf"
    doc = pymupdf.open(pdf_path)

    # Check page 7 (0-indexed: 6) BEFORE cropping
    page = doc[6]
    page_height = page.rect.height
    blocks = page.get_text("dict")["blocks"]

    print(f"Page 7 (index 6):")
    print(f"  Page height: {page_height}pt")
    print(f"  Total blocks: {len(blocks)}\n")

    # Extract text blocks
    text_blocks = []
    for b in blocks:
        if b["type"] == 0:
            bbox = b["bbox"]
            text = ""
            for line in b.get("lines", []):
                for span in line.get("spans", []):
                    text += span.get("text", "")
            text = text.strip()
            line_count = len(b.get("lines", []))
            text_blocks.append({
                'y0': bbox[1],
                'y1': bbox[3],
                'text': text,
                'lines': line_count,
                'height': bbox[3] - bbox[1],
                'width': bbox[2] - bbox[0]
            })

    text_blocks.sort(key=lambda x: x['y0'])

    # Find page number
    print("Looking for page number (bottom 15% of page):")
    for block in reversed(text_blocks):
        if (page_height - block['y1'] < page_height * 0.15 and
            len(block['text']) <= 4 and
            block['height'] < 20 and
            re.match(r'^\d+$', block['text'])):
            print(f"  Found: '{block['text']}' at y={block['y0']:.1f}")
            print(f"  Distance from bottom: {page_height - block['y0']:.1f}pt\n")
            break

    # Check bottom 100pt for all content
    print(f"All blocks in bottom 100pt (y > {page_height - 100:.1f}):")
    for block in text_blocks:
        if page_height - block['y0'] <= 100:
            preview = block['text'][:80].replace('\n', ' ')
            print(f"  y={block['y0']:.1f}: {preview}...")
            print(f"    Lines: {block['lines']}, Height: {block['height']:.1f}pt")

    doc.close()


if __name__ == "__main__":
    check_footer()
