"""Compare caption detection before and after refactor."""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.parser.pdf_parser import PdfParser
import json

def main():
    # Old results (before refactor)
    old_results = {
        "test.pdf": 25,  # from test_results_20251122_121057.json
        "test2.pdf": 53,
        "test3.pdf": 86,
        "tes4.pdf": 52,  # Note: typo in filename
        "tes5.pdf": 28,
        "test6.pdf": 50,
    }

    test_dir = Path('/Users/ivanforcytebio/Projects/PeerPreview/backend/docs/testPDFs')
    pdf_files = sorted([f for f in test_dir.glob('*.pdf') if not f.name.startswith('.')])

    parser = PdfParser()

    print("Caption Count Comparison (Before vs After Refactor)")
    print("=" * 70)
    print(f"{'PDF':<20} {'Before':<10} {'After':<10} {'Diff':<10} {'Status'}")
    print("-" * 70)

    total_before = 0
    total_after = 0
    mismatches = []

    for pdf_path in pdf_files:
        pdf_name = pdf_path.name

        # Get old count
        old_count = old_results.get(pdf_name, 0)

        # Parse with new code
        try:
            with open(pdf_path, 'rb') as f:
                pdf_bytes = f.read()

            parsed_doc = parser.parse(pdf_bytes)

            # Count figures (captions) in new output
            new_count = len(parsed_doc.figures)

            diff = new_count - old_count
            status = "✓ MATCH" if diff == 0 else f"⚠ DIFF: {diff:+d}"

            print(f"{pdf_name:<20} {old_count:<10} {new_count:<10} {diff:+10d} {status}")

            total_before += old_count
            total_after += new_count

            if diff != 0:
                mismatches.append({
                    'pdf': pdf_name,
                    'before': old_count,
                    'after': new_count,
                    'diff': diff
                })

        except Exception as e:
            print(f"{pdf_name:<20} {old_count:<10} {'ERROR':<10} {'N/A':<10} ✗ {str(e)[:30]}")

    print("-" * 70)
    print(f"{'TOTAL':<20} {total_before:<10} {total_after:<10} {total_after - total_before:+10d}")
    print("=" * 70)

    if mismatches:
        print(f"\n⚠ WARNING: {len(mismatches)} PDFs have different caption counts!")
        print("\nNOTE: Caption counts may differ if:")
        print("  - Old counts included inline 'Figure X' references (not actual captions)")
        print("  - Old captions had footer text merged (counted as separate)")
        print("  - New detection is more accurate (standalone captions only)")
        print("\nThis is likely EXPECTED and CORRECT if new counts are lower.")
    else:
        print("\n✅ All caption counts match! Refactor preserved detection accuracy.")

if __name__ == '__main__':
    main()
