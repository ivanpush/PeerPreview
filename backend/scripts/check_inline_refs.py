"""Check for inline figure references that shouldn't be captured as captions."""

import sys
from pathlib import Path

backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

import pymupdf
from services.parser.pipeline.stages.geometry import detect_footer_height, crop_margins, _extract_block_text
from services.parser.pipeline.config import GeometryConfig
import re


def check_inline_refs():
    """Check pages 7-8 and 22 of test.pdf for inline references."""

    pdf_path = backend_dir / "docs" / "testPDFs" / "test.pdf"
    doc = pymupdf.open(pdf_path)

    # Apply cropping
    config = GeometryConfig()
    bottom_margin = detect_footer_height(doc)
    doc = crop_margins(doc, top=config.top_margin, bottom=bottom_margin, left=0)

    # Check specific pages mentioned in old results
    pages_to_check = [6, 7, 21]  # Pages 7, 8, 22 (0-indexed)

    for page_num in pages_to_check:
        if page_num >= len(doc):
            continue

        page = doc[page_num]
        text_dict = page.get_text("dict")
        blocks = text_dict.get("blocks", [])

        print(f"\n{'='*80}")
        print(f"PAGE {page_num + 1} (0-indexed: {page_num})")
        print(f"{'='*80}")

        for i, block in enumerate(blocks):
            if block.get("type") != 0:
                continue

            text = _extract_block_text(block)
            if not text:
                continue

            # Look for "Figure 3" or "Fig 10b" patterns
            if re.search(r'\bfigure\s+\d+|fig\.?\s*\d+', text, re.IGNORECASE):
                # Show first 200 chars
                preview = text[:200].replace('\n', ' ')
                print(f"\nBlock {i}:")
                print(f"  Bbox: {block['bbox']}")
                print(f"  Text: {preview}...")

                # Check if it's an inline reference (has verb after)
                if re.search(r'figure\s+\d+[a-z]?\s+(shows?|demonstrates?|illustrates?)', text, re.IGNORECASE):
                    print(f"  ⚠️  INLINE REFERENCE - should be FILTERED")
                else:
                    print(f"  ✓ Likely a caption")

    doc.close()


if __name__ == "__main__":
    check_inline_refs()
