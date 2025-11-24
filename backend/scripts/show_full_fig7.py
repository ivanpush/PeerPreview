"""Show full Fig 7 caption text comparison."""

import sys
from pathlib import Path
import pymupdf

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.parser.pipeline.stages.analysis import detect_captions

def show_full():
    pdf_path = Path('/Users/ivanforcytebio/Projects/PeerPreview/backend/docs/testPDFs/test2.pdf')

    doc_uncropped = pymupdf.open(pdf_path)
    doc_cropped = pymupdf.open(pdf_path)

    # Crop
    for page in doc_cropped:
        rect = page.rect
        new_rect = pymupdf.Rect(rect.x0, rect.y0 + 60, rect.x1, rect.y1 - 60)
        page.set_cropbox(new_rect)

    captions_uncropped = detect_captions(doc_uncropped)
    captions_cropped = detect_captions(doc_cropped)

    fig7_uncropped = [c for c in captions_uncropped if '7' in c.figure_num][0]
    fig7_cropped = [c for c in captions_cropped if '7' in c.figure_num][0]

    print("UNCROPPED (OLD - with footer):")
    print("="*80)
    print(fig7_uncropped.text)
    print("="*80)
    print(f"Length: {len(fig7_uncropped.text)} chars\n")

    print("\nCROPPED (NEW - after footer removal):")
    print("="*80)
    print(fig7_cropped.text)
    print("="*80)
    print(f"Length: {len(fig7_cropped.text)} chars\n")

    # Find the difference
    print("\nDIFFERENCE (what was removed):")
    print("="*80)
    if fig7_uncropped.text.startswith(fig7_cropped.text):
        removed = fig7_uncropped.text[len(fig7_cropped.text):]
        print(f"REMOVED FROM END: '{removed}'")
    else:
        print("Captions don't match as expected - manual inspection needed")

    doc_uncropped.close()
    doc_cropped.close()

if __name__ == '__main__':
    show_full()
