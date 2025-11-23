"""Test script for figure detection enhancement.

Tests the enhanced parser pipeline on all PDFs in testPDFs/ folder.
Evaluates output quality and logs issues found.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline import PipelineBuilder, default_config


def evaluate_output(parsed_doc, pdf_name):
    """Evaluate parser output quality.

    Checks for:
    - Weird character residuals from figures
    - Jumbled sections
    - Lack of line breaks
    - Anything out of order
    - Figure garbage (axis labels, scattered text)

    Returns:
        Dict with evaluation results
    """
    issues = []
    markdown = parsed_doc.raw_markdown

    # Check for scattered single characters (figure axis labels)
    import re
    # Pattern: isolated single chars or short number sequences
    scattered_pattern = r'\b[a-z0-9]\s+[a-z0-9]\s+[a-z0-9]\s+[a-z0-9]\b'
    matches = re.findall(scattered_pattern, markdown, re.IGNORECASE)
    if matches:
        issues.append(f"Scattered characters found: {matches[:3]}... ({len(matches)} total)")

    # Check for number sequences (common in axis labels)
    number_seq_pattern = r'\b\d+\s+\d+\s+\d+\s+\d+\b'
    number_matches = re.findall(number_seq_pattern, markdown)
    if number_matches:
        issues.append(f"Number sequences found: {number_matches[:3]}... ({len(number_matches)} total)")

    # Check for missing line breaks (3+ sentences without newline)
    long_lines = [line for line in markdown.split('\n') if line.count('. ') > 3]
    if any(len(line) > 500 for line in long_lines):
        issues.append(f"Very long lines without breaks: {len([l for l in long_lines if len(l) > 500])} lines")

    # Check for unicode residuals (common figure artifacts)
    unicode_pattern = r'[▪�□■◆●○▲△▼▽]'
    unicode_matches = re.findall(unicode_pattern, markdown)
    if unicode_matches:
        issues.append(f"Unicode symbols found: {unicode_matches[:10]}... ({len(unicode_matches)} total)")

    # Check section ordering
    sections = list(parsed_doc.sections.keys())
    expected_order = ['abstract', 'introduction', 'methods', 'results', 'discussion', 'references']
    actual_order = [s for s in sections if s in expected_order]
    if actual_order != sorted(actual_order, key=lambda x: expected_order.index(x)):
        issues.append(f"Sections out of order: {actual_order}")

    # Check for captions preserved
    fig_pattern = r'(?i)(Figure|Fig\.?|Table)\s+\d+'
    captions_found = len(re.findall(fig_pattern, markdown))

    return {
        'issues': issues,
        'captions_found': captions_found,
        'word_count': len(markdown.split()),
        'char_count': len(markdown)
    }


def run_test(pdf_path, test_run_num=1):
    """Run parser on single PDF and evaluate.

    Args:
        pdf_path: Path to PDF file
        test_run_num: Test run number (for iterations)

    Returns:
        Test result dict
    """
    print(f"\n{'='*80}")
    print(f"Testing: {pdf_path.name} (Run {test_run_num})")
    print(f"{'='*80}")

    try:
        # Read PDF
        with open(pdf_path, 'rb') as f:
            pdf_bytes = f.read()

        # Build parser with debug output
        config = default_config()
        builder = PipelineBuilder(config, capture_stages=True)

        # Parse
        start = datetime.now()
        parsed_doc = builder.build(pdf_bytes, pdf_path.name)
        duration = (datetime.now() - start).total_seconds()

        # Evaluate
        evaluation = evaluate_output(parsed_doc, pdf_path.name)

        # Log captions detected
        caption_count = len([c for c in builder.stage_outputs.get('02_analyze_structure', '').split('\n') if 'Captions found:' in c])
        figure_regions = len([c for c in builder.stage_outputs.get('03_after_crop', '').split('\n') if 'Figure regions detected:' in c])

        result = {
            'pdf': pdf_path.name,
            'run': test_run_num,
            'duration_sec': round(duration, 2),
            'title': parsed_doc.title,
            'sections': list(parsed_doc.sections.keys()),
            'evaluation': evaluation,
            'status': 'PASS' if not evaluation['issues'] else 'FAIL',
            'timestamp': datetime.now().isoformat()
        }

        # Print summary
        print(f"\n✓ Parsed successfully in {duration:.2f}s")
        print(f"  Title: {parsed_doc.title}")
        print(f"  Sections: {len(parsed_doc.sections)}")
        print(f"  Captions found: {evaluation['captions_found']}")
        print(f"  Word count: {evaluation['word_count']}")

        if evaluation['issues']:
            print(f"\n⚠ Issues found:")
            for issue in evaluation['issues']:
                print(f"  - {issue}")
            result['status'] = 'FAIL'
        else:
            print(f"\n✓ No issues detected!")
            result['status'] = 'PASS'

        return result

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return {
            'pdf': pdf_path.name,
            'run': test_run_num,
            'status': 'ERROR',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }


def main():
    """Run tests on all PDFs in testPDFs folder."""
    test_dir = Path(__file__).parent.parent.parent / 'docs' / 'testPDFs'
    output_dir = test_dir / 'test_outputs'
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get all PDFs (excluding .DS_Store and test_no_abstract_header.pdf which is a minimal test)
    pdf_files = [f for f in test_dir.glob('*.pdf') if f.name != 'test_no_abstract_header.pdf']

    print(f"\n{'#'*80}")
    print(f"# Figure Detection Test Suite")
    print(f"# Testing {len(pdf_files)} PDFs")
    print(f"{'#'*80}")

    results = []

    for pdf_path in sorted(pdf_files):
        # Run test (single run for now, can add iterations if needed)
        result = run_test(pdf_path, test_run_num=1)
        results.append(result)

    # Summary
    print(f"\n{'='*80}")
    print(f"TEST SUMMARY")
    print(f"{'='*80}")

    passed = sum(1 for r in results if r['status'] == 'PASS')
    failed = sum(1 for r in results if r['status'] == 'FAIL')
    errors = sum(1 for r in results if r['status'] == 'ERROR')

    print(f"\nTotal: {len(results)}")
    print(f"✓ Passed: {passed}")
    print(f"⚠ Failed: {failed}")
    print(f"✗ Errors: {errors}")

    if failed > 0:
        print(f"\nFailed PDFs:")
        for r in results:
            if r['status'] == 'FAIL':
                print(f"  - {r['pdf']}: {len(r['evaluation']['issues'])} issues")
                for issue in r['evaluation']['issues'][:2]:  # Show first 2 issues
                    print(f"    • {issue}")

    # Save results to JSON
    results_file = output_dir / f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n📁 Results saved to: {results_file}")

    # Return exit code
    return 0 if failed == 0 and errors == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
