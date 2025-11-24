#!/usr/bin/env python3
"""Visualize how well figure regions cover actual figures."""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.parser.pdf_parser import PdfParser
import logging

logging.basicConfig(level=logging.DEBUG)


def visualize_pdf(pdf_path):
    """Parse PDF and show figure region coverage."""
    print(f"\n{'='*80}")
    print(f"Analyzing: {os.path.basename(pdf_path)}")
    print(f"{'='*80}\n")

    with open(pdf_path, 'rb') as f:
        pdf_bytes = f.read()

    parser = PdfParser()
    result = parser.parse(pdf_bytes, os.path.basename(pdf_path))

    # Access internal builder to get stage info
    builder = parser._last_builder  # Hack to get last builder used

    if hasattr(builder, 'geom_info') and builder.geom_info:
        geom_info = builder.geom_info

        print(f"📊 Figure Detection Summary:")
        print(f"   Total captions: {len(geom_info.figure_captions)}")
        print(f"   Total regions: {len(geom_info.figure_regions)}")
        print(f"   - With actual figures: {sum(1 for r in geom_info.figure_regions if r.has_actual_figure)}")
        print(f"   - Synthetic zones: {sum(1 for r in geom_info.figure_regions if not r.has_actual_figure)}")

        # Group by page
        pages_with_figures = set(r.page for r in geom_info.figure_regions)

        for page_num in sorted(pages_with_figures):
            page_captions = [c for c in geom_info.figure_captions if c.page == page_num]
            page_regions = [r for r in geom_info.figure_regions if r.page == page_num]

            print(f"\n{'─'*80}")
            print(f"PAGE {page_num}: {len(page_captions)} captions, {len(page_regions)} regions")
            print(f"{'─'*80}")

            for i, region in enumerate(page_regions):
                x0, y0, x1, y1 = region.bbox
                width = x1 - x0
                height = y1 - y0
                area = width * height

                print(f"\n  Region {i+1}: {region.detection_method}")
                print(f"    Size: {width:.0f} x {height:.0f} pt (area: {area:.0f})")
                print(f"    Bbox: ({x0:.0f}, {y0:.0f}, {x1:.0f}, {y1:.0f})")
                print(f"    Has figure: {region.has_actual_figure}")
                if region.associated_caption:
                    print(f"    Caption: {region.associated_caption.text[:70]}...")

    else:
        print("⚠️  No geometry info available")

    # Show markdown excerpt around first figure reference
    markdown = result.markdown
    if "Figure" in markdown or "Fig." in markdown:
        idx = markdown.find("Figure")
        if idx == -1:
            idx = markdown.find("Fig.")

        start = max(0, idx - 200)
        end = min(len(markdown), idx + 400)

        print(f"\n{'='*80}")
        print(f"MARKDOWN EXCERPT (around first figure reference):")
        print(f"{'='*80}")
        print(markdown[start:end])
        print(f"{'='*80}")


if __name__ == '__main__':
    test_pdf = 'docs/testPDFs/test2.pdf'
    if os.path.exists(test_pdf):
        visualize_pdf(test_pdf)
    else:
        print(f"Error: {test_pdf} not found")
