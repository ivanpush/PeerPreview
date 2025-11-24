#!/usr/bin/env python3
"""Debug why Fig 5 artifacts are getting through."""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pymupdf
from services.parser.pdf_parser import PdfParser
import logging

logging.basicConfig(level=logging.INFO)

pdf_path = 'docs/testPDFs/test2.pdf'

# Parse the PDF
with open(pdf_path, 'rb') as f:
    pdf_bytes = f.read()

parser = PdfParser()
doc = pymupdf.open(pdf_path)

# Find which page has "Fig. 5"
for page_num, page in enumerate(doc):
    text = page.get_text()
    if "Fig. 5" in text or "Figure 5" in text:
        print(f"\n{'='*80}")
        print(f"Fig 5 found on page {page_num}")
        print(f"{'='*80}\n")

        # Get images on this page
        images = page.get_images(full=True)
        print(f"Images on page: {len(images)}")

        for idx, img in enumerate(images):
            xref = img[0]
            rects = page.get_image_rects(xref)
            print(f"\nImage {idx}: {len(rects)} rects")
            for rect_idx, rect in enumerate(rects):
                print(f"  Rect {rect_idx}: {rect}")

        # Get text blocks
        blocks = page.get_text("dict")["blocks"]
        text_blocks = [b for b in blocks if b.get("type") == 0]

        print(f"\nText blocks on page: {len(text_blocks)}")

        # Find problematic text
        problem_patterns = ["_n_", "_R_", "_P_", "Histamine", "Serum", "Bradykinin"]

        for block in text_blocks:
            text = ""
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text += span.get("text", "")

            if any(p in text for p in problem_patterns):
                print(f"\n⚠️ Problem text found:")
                print(f"   Text: {text[:100]}")
                print(f"   Bbox: {block['bbox']}")

doc.close()
