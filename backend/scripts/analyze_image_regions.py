#!/usr/bin/env python3
"""Analyze how many image rects exist per figure in test PDFs."""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pymupdf
from collections import defaultdict

def analyze_pdf(pdf_path):
    """Analyze image distribution in a PDF."""
    doc = pymupdf.open(pdf_path)
    print(f"\n{'='*60}")
    print(f"Analyzing: {os.path.basename(pdf_path)}")
    print(f"{'='*60}")

    total_images = 0
    total_rects = 0
    multi_rect_images = 0

    for page_num, page in enumerate(doc):
        images = page.get_images(full=True)
        if not images:
            continue

        print(f"\nPage {page_num}: {len(images)} images")

        for idx, img in enumerate(images):
            xref = img[0]
            rects = page.get_image_rects(xref)
            total_images += 1
            total_rects += len(rects)

            if len(rects) > 1:
                multi_rect_images += 1
                print(f"  ⚠️  Image {idx} (xref={xref}): {len(rects)} RECTS")
                for rect_idx, rect in enumerate(rects):
                    width = rect.width
                    height = rect.height
                    area = width * height
                    print(f"      Rect {rect_idx}: {rect} (w={width:.1f}, h={height:.1f}, area={area:.0f})")
            else:
                rect = rects[0]
                width = rect.width
                height = rect.height
                area = width * height
                print(f"  ✓ Image {idx} (xref={xref}): 1 rect (w={width:.1f}, h={height:.1f}, area={area:.0f})")

    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Total images: {total_images}")
    print(f"  Total rects: {total_rects}")
    print(f"  Images with multiple rects: {multi_rect_images}")
    print(f"  Average rects per image: {total_rects/total_images if total_images > 0 else 0:.2f}")
    print(f"{'='*60}")

    doc.close()

if __name__ == '__main__':
    test_dir = os.path.join(os.path.dirname(__file__), '..', 'docs', 'testPDFs')

    # Analyze all test PDFs
    for filename in sorted(os.listdir(test_dir)):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(test_dir, filename)
            analyze_pdf(pdf_path)
