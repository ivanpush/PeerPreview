"""Check header detection for test3.pdf pages with missing captions."""

import sys
from pathlib import Path

backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

import pymupdf
from services.parser.pipeline.stages.geometry import detect_header_height


def check_headers():
    """Check header heights for pages 6 and 9 (0-indexed) of test3.pdf."""

    pdf_path = backend_dir / "docs" / "testPDFs" / "test3.pdf"
    doc = pymupdf.open(pdf_path)

    print("Checking header heights for test3.pdf pages with missing captions:\n")

    for page_num in [6, 9]:  # Pages 7 and 10 (1-indexed)
        if page_num >= len(doc):
            continue

        page = doc[page_num]
        is_first = (page_num == 0)
        header_height = detect_header_height(page, is_first_page=is_first)

        print(f"Page {page_num + 1} (0-indexed: {page_num}):")
        print(f"  Detected header height: {header_height}pt")
        print(f"  Caption position (from old data): y=49.3pt")
        print(f"  Caption will be cropped: {'YES ❌' if 49.3 < header_height else 'NO ✅'}")
        print()

        # Get text blocks to understand page structure
        text_dict = page.get_text("dict")
        blocks = text_dict.get("blocks", [])
        text_blocks = [b for b in blocks if b.get("type") == 0]

        if text_blocks:
            text_blocks.sort(key=lambda b: b["bbox"][1])
            print(f"  Top 5 text blocks:")
            for i, block in enumerate(text_blocks[:5]):
                bbox = block["bbox"]
                text = ""
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        text += span.get("text", "")[:50]
                        break
                    break
                print(f"    Block {i+1}: y={bbox[1]:.1f}pt, text='{text}...'")
        print()

    doc.close()


if __name__ == "__main__":
    check_headers()
