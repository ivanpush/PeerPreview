"""Test the PDF parser directly."""

import sys
from services.parser.pdf_parser import PdfParser

if len(sys.argv) < 2:
    print("Usage: python test_parser.py <pdf_file>")
    sys.exit(1)

pdf_path = sys.argv[1]

with open(pdf_path, 'rb') as f:
    pdf_bytes = f.read()

parser = PdfParser()
markdown = parser.parse(pdf_bytes)

# Print first 2000 characters
print("=" * 80)
print("PARSED OUTPUT:")
print("=" * 80)
print(markdown[:2000])
print("=" * 80)
print(f"\nTotal length: {len(markdown)} characters")
