#!/usr/bin/env python3
"""
Test section validation across all test PDFs
"""

import requests
import json
from pathlib import Path

API_URL = "http://localhost:8000"
TEST_PDF_DIR = Path("/Users/ivanforcytebio/Projects/PeerPreview/backend/docs/testPDFs")

def test_pdf(pdf_path):
    """Upload and test a PDF"""
    print(f"\n{'='*80}")
    print(f"Testing: {pdf_path.name}")
    print('='*80)

    with open(pdf_path, 'rb') as f:
        files = {'file': (pdf_path.name, f, 'application/pdf')}
        response = requests.post(f"{API_URL}/upload", files=files)

    if response.status_code != 200:
        print(f"❌ Upload failed: {response.status_code}")
        print(response.text)
        return

    data = response.json()

    print(f"\n📄 Title: {data['title'][:100]}")
    print(f"\n📑 Found Sections ({len(data['sections'])}):")
    for section in data['sections']:
        print(f"   • {section}")

    print(f"\n✅ Section Validation:")
    validation = data['section_validation']
    for key, value in validation.items():
        status = "✓" if value else "✗"
        color = "\033[92m" if value else "\033[91m"  # Green or Red
        reset = "\033[0m"
        print(f"   {color}{status}{reset} {key}: {value}")

    # Summary
    all_valid = all(validation.values())
    if all_valid:
        print(f"\n🎉 All required sections found!")
    else:
        missing = [k for k, v in validation.items() if not v]
        print(f"\n⚠️  Missing sections: {', '.join(missing)}")

def main():
    print("🧪 Testing Section Validation Across Test PDFs")
    print("="*80)

    # Get all test PDFs
    test_pdfs = sorted(TEST_PDF_DIR.glob("test*.pdf"))

    print(f"\nFound {len(test_pdfs)} test PDFs")

    for pdf_path in test_pdfs:
        try:
            test_pdf(pdf_path)
        except Exception as e:
            print(f"\n❌ Error testing {pdf_path.name}: {e}")

    print(f"\n{'='*80}")
    print("✅ Testing complete!")
    print('='*80)

if __name__ == "__main__":
    main()
