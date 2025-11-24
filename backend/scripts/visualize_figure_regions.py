#!/usr/bin/env python3
"""Visualize figure detection regions overlaid on PDF pages.

Creates annotated PDFs showing:
- Detected image boxes (blue)
- Merged regions (green)
- Expanded regions with margins (red)
- Captions (yellow)
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pymupdf
from services.parser.pdf_parser import PdfParser


def visualize_page_regions(pdf_path: str, output_path: str, page_nums: list = None):
    """Create annotated PDF showing figure detection regions.

    Args:
        pdf_path: Input PDF path
        output_path: Output PDF path with annotations
        page_nums: List of page numbers to visualize (0-indexed), or None for all
    """
    # Parse the PDF to get figure regions
    with open(pdf_path, 'rb') as f:
        pdf_bytes = f.read()

    parser = PdfParser()

    # Access internal builder to get geometry info
    import logging
    logging.basicConfig(level=logging.INFO)

    from services.parser.pipeline import PipelineBuilder
    from services.parser.pipeline.config import default_config

    builder = PipelineBuilder(default_config())
    parsed = builder.build(pdf_bytes, os.path.basename(pdf_path))

    geom_info = builder.geom_info

    # Open PDFs for annotation
    doc = pymupdf.open(pdf_path)
    output_doc = pymupdf.open(pdf_path)

    # Process each page
    for page_num in range(len(doc)):
        if page_nums and page_num not in page_nums:
            continue

        page = cleaned_doc[page_num]
        output_page = output_doc[page_num]

        # Get captions for this page
        page_captions = [c for c in geom_info.figure_captions if c.page == page_num]

        if not page_captions:
            continue

        print(f"\n{'='*80}")
        print(f"PAGE {page_num}")
        print(f"{'='*80}")

        # 1. Draw original image rects (BLUE)
        images = page.get_images(full=True)
        all_rects = []
        for img in images:
            try:
                xref = img[0]
                rects = page.get_image_rects(xref)
                for rect in rects:
                    width = rect.width
                    height = rect.height
                    area = width * height
                    if width >= 150 and height >= 100 and area >= 20000:
                        all_rects.append(tuple(rect))
                        # Draw on output
                        output_page.draw_rect(rect, color=(0, 0, 1), width=1)  # Blue
            except Exception as e:
                continue

        print(f"Original image rects: {len(all_rects)}")

        # 2. Draw merged regions (GREEN)
        if all_rects:
            merged = merge_overlapping_rects(all_rects, proximity_threshold=150)
            print(f"Merged regions: {len(merged)}")

            for bbox in merged:
                rect = pymupdf.Rect(bbox)
                output_page.draw_rect(rect, color=(0, 1, 0), width=2)  # Green

                # 3. Draw expanded regions (RED - this is what filters text!)
                expanded = expand_bbox_with_margin(bbox)
                exp_rect = pymupdf.Rect(expanded)
                output_page.draw_rect(exp_rect, color=(1, 0, 0), width=3)  # RED

                w_orig = bbox[2] - bbox[0]
                h_orig = bbox[3] - bbox[1]
                w_exp = expanded[2] - expanded[0]
                h_exp = expanded[3] - expanded[1]

                print(f"  Merged: {w_orig:.0f}x{h_orig:.0f}")
                print(f"  Expanded: {w_exp:.0f}x{h_exp:.0f}")

        # 4. Draw captions (YELLOW)
        for caption in page_captions:
            rect = pymupdf.Rect(caption.bbox)
            output_page.draw_rect(rect, color=(1, 1, 0), width=2)  # Yellow
            print(f"Caption: {caption.text[:60]}...")

        # 5. Draw text blocks that would be filtered (PINK border)
        from services.parser.pipeline.stages.extraction import should_filter_text
        page_figure_regions = [r for r in geom_info.figure_regions if r.page == page_num]

        blocks = page.get_text("dict")["blocks"]
        filtered_count = 0
        for block in blocks:
            if block.get("type") != 0:
                continue

            if should_filter_text(block, page_figure_regions, page_captions):
                rect = pymupdf.Rect(block["bbox"])
                output_page.draw_rect(rect, color=(1, 0, 1), width=1)  # Pink
                filtered_count += 1

        print(f"Text blocks filtered: {filtered_count}")

        # Add legend
        legend_y = 20
        output_page.insert_text((20, legend_y), "LEGEND:", fontsize=10)
        output_page.insert_text((20, legend_y+15), "BLUE = Original images", fontsize=8, color=(0, 0, 1))
        output_page.insert_text((20, legend_y+30), "GREEN = Merged regions", fontsize=8, color=(0, 1, 0))
        output_page.insert_text((20, legend_y+45), "RED = Expanded (w/ margins)", fontsize=8, color=(1, 0, 0))
        output_page.insert_text((20, legend_y+60), "YELLOW = Captions", fontsize=8, color=(1, 1, 0))
        output_page.insert_text((20, legend_y+75), "PINK = Filtered text", fontsize=8, color=(1, 0, 1))

    # Save annotated PDF
    output_doc.save(output_path)
    output_doc.close()
    doc.close()
    cleaned_doc.close()

    print(f"\n{'='*80}")
    print(f"Saved annotated PDF to: {output_path}")
    print(f"{'='*80}")
    print("\nOpen the PDF to see:")
    print("  - RED boxes = what we're using to filter text")
    print("  - PINK borders = text that gets deleted")
    print("  - YELLOW = captions (never deleted)")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python visualize_figure_regions.py <pdf_path> [page_numbers...]")
        print("Example: python visualize_figure_regions.py test2.pdf 5 7")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_path = pdf_path.replace('.pdf', '_annotated.pdf')

    # Parse page numbers if provided
    page_nums = None
    if len(sys.argv) > 2:
        page_nums = [int(p) for p in sys.argv[2:]]

    visualize_page_regions(pdf_path, output_path, page_nums)
