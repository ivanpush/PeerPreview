"""Inspect actual caption text to verify footer removal."""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.parser.pipeline import PipelineBuilder, default_config
import pymupdf

def inspect_test2_captions():
    """Check test2.pdf Figure 7 caption for footer text."""

    pdf_path = Path('/Users/ivanforcytebio/Projects/PeerPreview/backend/docs/testPDFs/test2.pdf')

    print("=" * 80)
    print("Inspecting test2.pdf Figure Captions (AFTER REFACTOR)")
    print("=" * 80)

    builder = PipelineBuilder(default_config())

    with open(pdf_path, 'rb') as f:
        pdf_bytes = f.read()

    # Parse with new refactored code
    parsed_doc = builder.build(pdf_bytes, "test2.pdf")

    print(f"\nFound {len(parsed_doc.figures)} figures\n")

    # Look for Figure 7
    for fig in parsed_doc.figures:
        if '7' in fig.label:
            print(f"Label: {fig.label}")
            print(f"Page: {fig.page}")
            print(f"Caption text ({len(fig.caption)} chars):")
            print("-" * 80)
            print(fig.caption)
            print("-" * 80)

            # Check for footer artifacts
            footer_keywords = [
                'biorxiv', 'preprint', 'doi:', 'copyright',
                'license', 'peer review', 'manuscript',
                'nature', 'biomedical engineering'
            ]

            found_footer = []
            for keyword in footer_keywords:
                if keyword in fig.caption.lower():
                    found_footer.append(keyword)

            if found_footer:
                print(f"\n❌ FOOTER CONTAMINATION DETECTED: {found_footer}")
            else:
                print(f"\n✅ No footer text detected in caption")

            print("\n")

    print("\n" + "=" * 80)
    print("All Figure Captions:")
    print("=" * 80)
    for i, fig in enumerate(parsed_doc.figures, 1):
        print(f"\n{i}. {fig.label} (Page {fig.page})")
        print(f"   First 100 chars: {fig.caption[:100]}...")
        print(f"   Last 100 chars: ...{fig.caption[-100:]}")

        # Check each for footer
        footer_keywords = ['biorxiv', 'preprint', 'doi:', 'nature', 'biomedical engineering']
        contaminated = any(kw in fig.caption.lower() for kw in footer_keywords)
        if contaminated:
            print(f"   ⚠️ POSSIBLE FOOTER TEXT DETECTED")

if __name__ == '__main__':
    inspect_test2_captions()
