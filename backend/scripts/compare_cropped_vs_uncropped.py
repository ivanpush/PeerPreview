"""Compare caption detection on cropped vs uncropped pages."""

import sys
from pathlib import Path
import pymupdf

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.parser.pipeline.stages.analysis import detect_captions

def compare_detection():
    """Compare captions detected before and after cropping."""

    pdf_path = Path('/Users/ivanforcytebio/Projects/PeerPreview/backend/docs/testPDFs/test2.pdf')

    print("=" * 80)
    print("Caption Detection: UNCROPPED vs CROPPED Pages")
    print("=" * 80)

    doc_uncropped = pymupdf.open(pdf_path)
    doc_cropped = pymupdf.open(pdf_path)

    # Manually crop the second doc (simulate geometry stage)
    for page in doc_cropped:
        rect = page.rect
        # Typical crop: top 60pt, bottom 60pt
        new_rect = pymupdf.Rect(
            rect.x0,
            rect.y0 + 60,
            rect.x1,
            rect.y1 - 60
        )
        page.set_cropbox(new_rect)

    # Detect on both
    captions_uncropped = detect_captions(doc_uncropped)
    captions_cropped = detect_captions(doc_cropped)

    print(f"\nUNCROPPED: {len(captions_uncropped)} captions")
    print(f"CROPPED: {len(captions_cropped)} captions")

    # Find Figure 7
    print("\n" + "=" * 80)
    print("Figure 7 Comparison:")
    print("=" * 80)

    fig7_uncropped = [c for c in captions_uncropped if '7' in c.figure_num]
    fig7_cropped = [c for c in captions_cropped if '7' in c.figure_num]

    print(f"\nUNCROPPED (Stage 2 - OLD WAY):")
    print(f"Found {len(fig7_uncropped)} instances")
    for c in fig7_uncropped:
        print(f"\n  {c.figure_type} {c.figure_num} (Page {c.page})")
        print(f"  Length: {len(c.text)} chars")
        print(f"  Last 200 chars:")
        print(f"  ...{c.text[-200:]}")

        # Check for footer
        footer_kw = ['nature', 'biomedical engineering', 'biorxiv', 'preprint', 'doi:', 'springer']
        found = [kw for kw in footer_kw if kw in c.text.lower()]
        if found:
            print(f"  ❌ FOOTER DETECTED: {found}")
        else:
            print(f"  ✅ Clean")

    print(f"\n{'='*80}")
    print(f"CROPPED (Stage 3 - NEW WAY):")
    print(f"Found {len(fig7_cropped)} instances")
    for c in fig7_cropped:
        print(f"\n  {c.figure_type} {c.figure_num} (Page {c.page})")
        print(f"  Length: {len(c.text)} chars")
        print(f"  Last 200 chars:")
        print(f"  ...{c.text[-200:]}")

        # Check for footer
        footer_kw = ['nature', 'biomedical engineering', 'biorxiv', 'preprint', 'doi:', 'springer']
        found = [kw for kw in footer_kw if kw in c.text.lower()]
        if found:
            print(f"  ❌ FOOTER DETECTED: {found}")
        else:
            print(f"  ✅ Clean")

    doc_uncropped.close()
    doc_cropped.close()

if __name__ == '__main__':
    compare_detection()
