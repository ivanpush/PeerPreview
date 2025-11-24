"""Debug Fig 7 truncation in test2.pdf."""

import sys
from pathlib import Path

backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

import pymupdf
from services.parser.pipeline.stages.geometry import detect_footer_height, crop_margins, _extract_block_text
from services.parser.pipeline.config import GeometryConfig


def debug_fig7():
    """Debug Fig 7 truncation on page 7 of test2.pdf."""

    pdf_path = backend_dir / "docs" / "testPDFs" / "test2.pdf"
    doc = pymupdf.open(pdf_path)

    # Apply cropping
    config = GeometryConfig()
    bottom_margin = detect_footer_height(doc)
    print(f"Bottom margin detected: {bottom_margin}pt\n")

    doc = crop_margins(doc, top=config.top_margin, bottom=bottom_margin, left=0)

    # Check page 7 (0-indexed: 6)
    page = doc[6]
    text_dict = page.get_text("dict")
    blocks = text_dict.get("blocks", [])

    print(f"Page 7 has {len(blocks)} blocks\n")
    print(f"{'='*80}")
    print("Blocks starting from y=600 (near Fig 7):")
    print(f"{'='*80}\n")

    for i, block in enumerate(blocks):
        if block.get("type") != 0:
            continue

        bbox = block["bbox"]
        if bbox[1] < 600:  # Only show blocks starting from y=600
            continue

        text = _extract_block_text(block)
        print(f"Block {i}:")
        print(f"  Bbox: {bbox}")
        print(f"  Y-position: {bbox[1]:.1f}")
        print(f"  Height: {bbox[3] - bbox[1]:.1f}pt")
        print(f"  Lines: {len(block.get('lines', []))}")
        print(f"  Text preview: {text[:100]}...")
        print(f"  Ends with: ...{text[-50:]}")
        print()

    doc.close()


if __name__ == "__main__":
    debug_fig7()
