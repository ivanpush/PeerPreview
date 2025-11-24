#!/usr/bin/env python3
"""Debug figure region detection - show what's being filtered."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pymupdf
from services.parser.pipeline.stages.geometry import apply_geometric_cleaning
from services.parser.pipeline.stages.analysis import detect_captions
from services.parser.pipeline.stages.figures import detect_figure_regions
from services.parser.pipeline.config import default_config


def debug_pdf(pdf_path):
    """Debug figure detection for a PDF."""
    print(f"\n{'='*80}")
    print(f"Debugging: {os.path.basename(pdf_path)}")
    print(f"{'='*80}\n")

    doc = pymupdf.open(pdf_path)
    config = default_config()

    # Apply geometric cleaning (crops margins)
    cleaned_doc, geom_info = apply_geometric_cleaning(doc, config, None)

    print(f"Total captions detected: {len(geom_info.figure_captions)}")
    print(f"Total figure regions: {len(geom_info.figure_regions)}\n")

    # Show details for each page with figures
    for page_num in range(len(cleaned_doc)):
        page_captions = [c for c in geom_info.figure_captions if c.page == page_num]
        page_regions = [r for r in geom_info.figure_regions if r.page == page_num]

        if not page_regions:
            continue

        print(f"\n{'='*80}")
        print(f"PAGE {page_num}")
        print(f"{'='*80}")

        print(f"\nCaptions on this page: {len(page_captions)}")
        for cap in page_captions:
            print(f"  - {cap.figure_type} {cap.figure_number}: {cap.text[:60]}...")
            print(f"    bbox: {cap.bbox}")

        print(f"\nFigure regions on this page: {len(page_regions)}")
        for i, region in enumerate(page_regions):
            x0, y0, x1, y1 = region.bbox
            width = x1 - x0
            height = y1 - y0
            area = width * height

            print(f"\n  Region {i+1}:")
            print(f"    Method: {region.detection_method}")
            print(f"    Has actual figure: {region.has_actual_figure}")
            print(f"    Bbox: ({x0:.1f}, {y0:.1f}, {x1:.1f}, {y1:.1f})")
            print(f"    Size: {width:.1f} x {height:.1f} pt (area: {area:.0f})")
            if region.associated_caption:
                print(f"    Caption: {region.associated_caption.text[:60]}...")

        # Get text blocks on this page and show which would be filtered
        page = cleaned_doc[page_num]
        text_blocks = page.get_text("dict")["blocks"]

        print(f"\nText blocks on page: {len(text_blocks)}")

        filtered_count = 0
        preserved_count = 0

        for block in text_blocks:
            if block.get("type") != 0:  # Not a text block
                continue

            bbox = block["bbox"]
            x0, y0, x1, y1 = bbox
            block_height = y1 - y0

            # Get text content
            text_content = ""
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text_content += span.get("text", "")

            if not text_content.strip():
                continue

            # Check if this block overlaps any figure region
            overlaps_figure = False
            for region in page_regions:
                rx0, ry0, rx1, ry1 = region.bbox

                # Calculate overlap
                overlap_x = max(0, min(x1, rx1) - max(x0, rx0))
                overlap_y = max(0, min(y1, ry1) - max(y0, ry0))
                overlap_area = overlap_x * overlap_y

                block_area = (x1 - x0) * (y1 - y0)
                if block_area > 0:
                    overlap_pct = (overlap_area / block_area) * 100

                    # Apply filtering thresholds
                    threshold = 50 if block_height < 20 else 30

                    if overlap_pct > threshold:
                        overlaps_figure = True
                        filtered_count += 1
                        print(f"\n  ❌ FILTERED ({overlap_pct:.0f}% overlap, height={block_height:.1f}):")
                        print(f"     Text: {text_content[:80]}")
                        print(f"     Block bbox: {bbox}")
                        print(f"     Figure bbox: {(rx0, ry0, rx1, ry1)}")
                        break

            if not overlaps_figure:
                preserved_count += 1

        print(f"\n📊 Summary: {filtered_count} blocks filtered, {preserved_count} blocks preserved")

    doc.close()


if __name__ == '__main__':
    # Debug test2.pdf (the problematic one)
    test_pdf = 'docs/testPDFs/test2.pdf'
    if os.path.exists(test_pdf):
        debug_pdf(test_pdf)
    else:
        print(f"Error: {test_pdf} not found")
