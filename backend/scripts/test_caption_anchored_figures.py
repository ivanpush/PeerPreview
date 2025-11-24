"""
Test script for Caption-Anchored Ray-Casting Figure Detection.

This script validates the new algorithm by:
1. Processing all test PDFs
2. Analyzing output for common issues (artifacts, merged paragraphs)
3. Comparing against baseline metrics
4. Generating detailed test report
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime
import re

# Add parent directories to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.parser.pipeline import PipelineBuilder, default_config


def analyze_markdown_quality(markdown: str) -> dict:
    """
    Analyze parsed markdown for common quality issues.

    Returns dict with metrics:
    - scattered_chars: Count of scattered character groups (figure artifacts)
    - merged_paragraphs: Count of abnormally long lines (>500 chars, likely merged)
    - total_lines: Total line count
    - avg_line_length: Average line length
    - caption_count: Count of figure captions
    """
    lines = markdown.split('\n')

    # Filter out empty lines
    non_empty_lines = [line for line in lines if line.strip()]

    # Detect scattered characters (common artifact pattern)
    # e.g., "a b c d", "0 5 10 15 20", "p < 0.05"
    scattered_pattern = re.compile(r'^[\w\s\.\<\>\=\-]{1,30}$')
    scattered_chars = []

    for line in non_empty_lines:
        stripped = line.strip()
        # Short lines with scattered appearance
        if len(stripped) < 30 and ' ' in stripped:
            word_count = len(stripped.split())
            char_count = len(stripped.replace(' ', ''))
            # High ratio of spaces to characters = scattered
            if word_count >= 3 and char_count / len(stripped) < 0.6:
                scattered_chars.append(stripped)

    # Detect merged paragraphs (very long lines without breaks)
    # Normal academic text wraps at ~80-100 chars
    # Lines >500 chars suggest missing line breaks (text was deleted mid-paragraph)
    very_long_lines = [line for line in non_empty_lines if len(line) > 500]

    # Calculate average line length
    if non_empty_lines:
        avg_line_length = sum(len(line) for line in non_empty_lines) / len(non_empty_lines)
    else:
        avg_line_length = 0

    # Count captions
    caption_pattern = re.compile(r'\b(Figure|Fig\.|Table|Scheme)\s+\d+', re.IGNORECASE)
    caption_count = len(caption_pattern.findall(markdown))

    return {
        'scattered_chars': scattered_chars,
        'scattered_char_count': len(scattered_chars),
        'merged_paragraphs': len(very_long_lines),
        'total_lines': len(non_empty_lines),
        'avg_line_length': round(avg_line_length, 1),
        'caption_count': caption_count
    }


def test_single_pdf(pdf_path: Path, config) -> dict:
    """
    Test caption-anchored algorithm on a single PDF.

    Returns dict with test results.
    """
    print(f"\n{'='*60}")
    print(f"Testing: {pdf_path.name}")
    print(f"{'='*60}")

    try:
        # Read PDF
        with open(pdf_path, 'rb') as f:
            pdf_bytes = f.read()

        # Build pipeline
        builder = PipelineBuilder(config)

        # Parse PDF
        parsed_doc = builder.build(pdf_bytes, pdf_path.name)

        # Analyze output quality
        markdown = parsed_doc.raw_markdown
        quality = analyze_markdown_quality(markdown)

        # Extract figure detection info from sections
        figure_count = 0
        if hasattr(parsed_doc, 'figures'):
            figure_count = len(parsed_doc.figures)
        elif hasattr(parsed_doc, 'sections'):
            # Count from sections if available
            figure_count = sum(len(getattr(section, 'figures', [])) for section in parsed_doc.sections.values())

        # Generate summary
        print(f"✓ Parsed successfully")
        print(f"  Captions detected: {quality['caption_count']}")
        print(f"  Figure regions: {figure_count}")
        print(f"  Total lines: {quality['total_lines']}")
        print(f"  Avg line length: {quality['avg_line_length']} chars")
        print(f"  Merged paragraphs: {quality['merged_paragraphs']}")
        print(f"  Scattered artifacts: {quality['scattered_char_count']}")

        if quality['scattered_char_count'] > 0:
            print(f"  Example artifacts: {quality['scattered_chars'][:3]}")

        # Determine pass/fail
        issues = []
        if quality['merged_paragraphs'] > 10:
            issues.append(f"Too many merged paragraphs ({quality['merged_paragraphs']})")
        if quality['scattered_char_count'] > 5:
            issues.append(f"Too many scattered artifacts ({quality['scattered_char_count']})")

        passed = len(issues) == 0

        return {
            'pdf': pdf_path.name,
            'status': 'PASS' if passed else 'FAIL',
            'issues': issues,
            'quality': quality,
            'figure_count': figure_count
        }

    except Exception as e:
        print(f"✗ Error: {e}")
        return {
            'pdf': pdf_path.name,
            'status': 'ERROR',
            'error': str(e),
            'issues': [f"Parse error: {str(e)}"]
        }


def run_full_test_suite():
    """
    Run caption-anchored algorithm on all test PDFs.

    Generates detailed test report with metrics.
    """
    print("\n" + "="*60)
    print("CAPTION-ANCHORED RAY-CASTING FIGURE DETECTION TEST")
    print("="*60)

    # Find test PDFs
    test_pdf_dir = Path(__file__).parent.parent / 'docs' / 'testPDFs'

    if not test_pdf_dir.exists():
        print(f"Error: Test PDF directory not found: {test_pdf_dir}")
        return

    test_pdfs = sorted(test_pdf_dir.glob('test*.pdf'))

    if not test_pdfs:
        print(f"Error: No test PDFs found in {test_pdf_dir}")
        return

    print(f"\nFound {len(test_pdfs)} test PDFs")

    # Configure pipeline
    config = default_config()

    # Run tests
    results = []
    for pdf_path in test_pdfs:
        result = test_single_pdf(pdf_path, config)
        results.append(result)

    # Generate summary report
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = [r for r in results if r['status'] == 'PASS']
    failed = [r for r in results if r['status'] == 'FAIL']
    errors = [r for r in results if r['status'] == 'ERROR']

    print(f"\nResults:")
    print(f"  PASS: {len(passed)}/{len(results)}")
    print(f"  FAIL: {len(failed)}/{len(results)}")
    print(f"  ERROR: {len(errors)}/{len(results)}")

    # Aggregate metrics
    total_merged = sum(r.get('quality', {}).get('merged_paragraphs', 0) for r in results if 'quality' in r)
    total_artifacts = sum(r.get('quality', {}).get('scattered_char_count', 0) for r in results if 'quality' in r)
    total_captions = sum(r.get('quality', {}).get('caption_count', 0) for r in results if 'quality' in r)

    print(f"\nAggregate Metrics:")
    print(f"  Total merged paragraphs: {total_merged}")
    print(f"  Total scattered artifacts: {total_artifacts}")
    print(f"  Total captions detected: {total_captions}")

    # Performance vs baseline
    print(f"\nPerformance vs Baseline (old algorithm):")
    print(f"  Baseline merged paragraphs: 98")
    print(f"  Current merged paragraphs: {total_merged}")
    if total_merged < 98:
        improvement = round((98 - total_merged) / 98 * 100, 1)
        print(f"  ✓ IMPROVEMENT: {improvement}% reduction")
    else:
        regression = round((total_merged - 98) / 98 * 100, 1)
        print(f"  ✗ REGRESSION: {regression}% increase")

    print(f"\n  Baseline scattered artifacts: 5")
    print(f"  Current scattered artifacts: {total_artifacts}")
    if total_artifacts <= 5:
        print(f"  ✓ MAINTAINED: Artifact removal still effective")
    else:
        increase = total_artifacts - 5
        print(f"  ⚠ INCREASE: {increase} more artifacts than baseline")

    # Detail failed tests
    if failed:
        print(f"\nFailed Tests:")
        for r in failed:
            print(f"\n  {r['pdf']}:")
            for issue in r['issues']:
                print(f"    - {issue}")

    # Save detailed report
    output_dir = test_pdf_dir / 'test_outputs'
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = output_dir / f"caption_anchored_test_{timestamp}.json"

    with open(report_file, 'w') as f:
        json.dump({
            'timestamp': timestamp,
            'test_count': len(results),
            'passed': len(passed),
            'failed': len(failed),
            'errors': len(errors),
            'aggregate_metrics': {
                'total_merged_paragraphs': total_merged,
                'total_scattered_artifacts': total_artifacts,
                'total_captions': total_captions
            },
            'results': results
        }, f, indent=2)

    print(f"\n✓ Detailed report saved to: {report_file}")

    # Overall result
    print("\n" + "="*60)
    if len(passed) == len(results):
        print("✓ ALL TESTS PASSED")
    elif len(errors) > 0:
        print("✗ SOME TESTS HAD ERRORS")
    else:
        print("⚠ SOME TESTS FAILED")
    print("="*60 + "\n")

    return results


if __name__ == "__main__":
    run_full_test_suite()
