"""Debug test3.pdf caption detection to find missing captions."""

import sys
from pathlib import Path

backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

import pymupdf
from services.parser.pipeline.stages.geometry import detect_footer_height, crop_margins, _extract_block_text
from services.parser.pipeline.config import GeometryConfig
import re


def debug_test3():
    """Debug test3.pdf to find missing Fig 5 and Fig 7."""

    pdf_path = backend_dir / "docs" / "testPDFs" / "test3.pdf"
    doc = pymupdf.open(pdf_path)

    # Apply cropping
    config = GeometryConfig()
    bottom_margin = detect_footer_height(doc)
    doc = crop_margins(doc, top=config.top_margin, bottom=bottom_margin, left=0)

    caption_pattern = re.compile(
        r'^\s*(Figure|Fig\.?|Table|Scheme)\s*'
        r'(S)?'
        r'(\d+)',
        re.IGNORECASE
    )

    # Check pages 5-10 for figure captions
    print("Scanning pages 5-10 for figure/table patterns:\n")
    for page_num in range(4, 11):  # Pages 5-11 (0-indexed: 4-10)
        if page_num >= len(doc):
            break

        page = doc[page_num]
        text_dict = page.get_text("dict")
        blocks = text_dict.get("blocks", [])

        print(f"{'='*80}")
        print(f"PAGE {page_num + 1}")
        print(f"{'='*80}")

        for i, block in enumerate(blocks):
            if block.get("type") != 0:
                continue

            text = _extract_block_text(block)
            if not text:
                continue

            # Check if it matches figure pattern
            match = caption_pattern.match(text)
            if match:
                print(f"\nBlock {i}:")
                print(f"  Type: {match.group(1)}")
                print(f"  Number: {match.group(3)}")
                print(f"  Text (first 100 chars): {text[:100]}...")
                print(f"  Full length: {len(text)} chars")
                print(f"  Bbox: {block['bbox']}")

    doc.close()


if __name__ == "__main__":
    debug_test3()
