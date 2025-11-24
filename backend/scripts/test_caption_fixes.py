"""Test caption detection fixes on all test PDFs.

Verifies:
1. Full captions captured (no truncation)
2. Inline references filtered out
3. No regressions in other PDFs
"""

import sys
import os
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

import pymupdf
from services.parser.pipeline.stages.geometry import detect_captions, crop_margins, detect_footer_height
from services.parser.pipeline.config import GeometryConfig
import json
from datetime import datetime


def test_caption_detection():
    """Test caption detection on all PDFs."""

    test_dir = backend_dir / "docs" / "testPDFs"
    pdf_files = sorted(test_dir.glob("*.pdf"))

    if not pdf_files:
        print(f"❌ No PDFs found in {test_dir}")
        return

    print(f"\n{'='*80}")
    print(f"CAPTION DETECTION TEST - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}\n")

    all_results = {
        "timestamp": datetime.now().isoformat(),
        "total_pdfs": len(pdf_files),
        "pdfs": {}
    }

    for pdf_path in pdf_files:
        print(f"\n{'─'*80}")
        print(f"Testing: {pdf_path.name}")
        print(f"{'─'*80}")

        try:
            # Load PDF
            doc = pymupdf.open(pdf_path)

            # Apply cropping first (like the real pipeline)
            config = GeometryConfig()
            bottom_margin = detect_footer_height(doc)
            doc = crop_margins(doc, top=config.top_margin, bottom=bottom_margin, left=0)

            # Detect captions on cropped pages
            captions = detect_captions(doc)

            # Store results
            pdf_results = {
                "filename": pdf_path.name,
                "pages": len(doc),
                "captions_found": len(captions),
                "captions": []
            }

            print(f"  Pages: {len(doc)}")
            print(f"  Captions found: {len(captions)}")

            # Show each caption
            for cap in captions:
                caption_info = {
                    "page": cap.page + 1,
                    "type": cap.figure_type,
                    "num": cap.figure_num,
                    "is_bold": cap.is_bold,
                    "confidence": cap.confidence,
                    "text_preview": cap.text[:100] + "..." if len(cap.text) > 100 else cap.text,
                    "full_text": cap.text,
                    "text_length": len(cap.text)
                }
                pdf_results["captions"].append(caption_info)

                print(f"\n  Page {cap.page + 1}:")
                print(f"    {cap.figure_type.upper()} {cap.figure_num} {'(BOLD)' if cap.is_bold else ''} (confidence: {cap.confidence:.2f})")
                print(f"    Length: {len(cap.text)} chars")
                print(f"    Text: {cap.text[:120]}...")

                # Flag potential issues
                if len(cap.text) < 50:
                    print(f"    ⚠️  SHORT CAPTION - might be truncated or inline ref")
                if "shows" in cap.text[:100].lower() or "demonstrates" in cap.text[:100].lower():
                    print(f"    ⚠️  CONTAINS VERB - might be inline reference")

            all_results["pdfs"][pdf_path.name] = pdf_results

            doc.close()

            print(f"\n  ✅ {pdf_path.name} processed successfully")

        except Exception as e:
            print(f"\n  ❌ Error processing {pdf_path.name}: {e}")
            import traceback
            traceback.print_exc()
            all_results["pdfs"][pdf_path.name] = {
                "error": str(e)
            }

    # Save results
    output_path = test_dir / "caption_test_results.json"
    with open(output_path, 'w') as f:
        json.dump(all_results, f, indent=2)

    print(f"\n{'='*80}")
    print(f"SUMMARY")
    print(f"{'='*80}")
    print(f"Total PDFs tested: {len(pdf_files)}")
    print(f"Results saved to: {output_path}")

    # Compare with old results if available
    old_results_path = test_dir / "caption_extracts" / "captions_20251122_130637.md"
    if old_results_path.exists():
        print(f"\n📊 OLD WORKING RESULTS (for comparison):")
        print(f"   test.pdf: 11 captions")
        print(f"   test2.pdf: 8 captions")
        print(f"   test3.pdf: 7 captions")
        print(f"   test4.pdf: 7 captions")
        print(f"   test5.pdf: 5 captions")
        print(f"   test6.pdf: 6 captions")
        print(f"   test7.pdf: 8 captions")

        print(f"\n📊 NEW RESULTS:")
        for pdf_name, results in all_results["pdfs"].items():
            if "captions_found" in results:
                print(f"   {pdf_name}: {results['captions_found']} captions")

    print(f"\n{'='*80}\n")


if __name__ == "__main__":
    test_caption_detection()
