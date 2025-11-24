"""Check raw caption detection from geometry stage."""

import sys
from pathlib import Path
import pymupdf

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.parser.pipeline.stages.geometry import apply_geometric_cleaning
from services.parser.pipeline.stages.analysis import analyze_structure
from services.parser.pipeline.config import default_config

def check_raw_captions():
    """Inspect raw caption detection for test2.pdf."""

    pdf_path = Path('/Users/ivanforcytebio/Projects/PeerPreview/backend/docs/testPDFs/test2.pdf')

    print("=" * 80)
    print("RAW Caption Detection (Stage 3 - After Cropping)")
    print("=" * 80)

    doc = pymupdf.open(pdf_path)
    config = default_config()

    # Stage 2: Structure analysis
    structure_info = analyze_structure(doc, config.analysis)

    # Stage 3: Geometric cleaning + caption detection
    doc, geom_info = apply_geometric_cleaning(doc, config.geometry, structure_info)

    print(f"\nDetected {len(geom_info.figure_captions)} captions\n")

    for i, caption in enumerate(geom_info.figure_captions, 1):
        print(f"\n{i}. {caption.figure_type} {caption.figure_num} (Page {caption.page})")
        print(f"   Confidence: {caption.confidence:.2f}, Standalone: {caption.is_standalone}, Bold: {caption.is_bold}")
        print(f"   Text ({len(caption.text)} chars):")
        print(f"   " + "-" * 76)

        # Show first 200 chars and last 200 chars
        if len(caption.text) <= 400:
            print(f"   {caption.text}")
        else:
            print(f"   {caption.text[:200]}")
            print(f"   [...{len(caption.text) - 400} chars omitted...]")
            print(f"   {caption.text[-200:]}")

        print(f"   " + "-" * 76)

        # Check for footer keywords
        footer_keywords = ['nature', 'biomedical engineering', 'biorxiv', 'preprint', 'doi:', 'springer']
        found = [kw for kw in footer_keywords if kw in caption.text.lower()]

        if found:
            print(f"   ⚠️ FOOTER CONTAMINATION: {found}")
        else:
            print(f"   ✅ Clean (no footer text)")

    doc.close()

if __name__ == '__main__':
    check_raw_captions()
