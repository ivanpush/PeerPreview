"""Test parser on all PDFs and evaluate output quality."""

import os
import sys
from pathlib import Path
from services.parser.pdf_parser import PdfParser
import logging

# Enable debug logging for column detection
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_output_quality(markdown: str, pdf_name: str) -> dict:
    """Analyze markdown output for common issues."""
    issues = []

    # Check for weird character residuals
    weird_chars = ['□', '■', '●', '○', '▪', '▫', '▬', '►', '◄', '↑', '↓', '←', '→']
    found_weird = [c for c in weird_chars if c in markdown]
    if found_weird:
        issues.append(f"Weird characters found: {found_weird}")

    # Check for jumbled sections (crude heuristic: very short paragraphs)
    lines = markdown.split('\n')
    non_empty_lines = [l for l in lines if l.strip()]
    if len(non_empty_lines) > 10:
        avg_line_length = sum(len(l) for l in non_empty_lines) / len(non_empty_lines)
        if avg_line_length < 30:
            issues.append(f"Possibly jumbled: avg line length {avg_line_length:.1f} chars")

    # Check for lack of line breaks (very long continuous text)
    paragraphs = markdown.split('\n\n')
    long_paragraphs = [p for p in paragraphs if len(p) > 2000]
    if long_paragraphs:
        issues.append(f"Found {len(long_paragraphs)} very long paragraphs (>2000 chars)")

    # Check for figure placeholders
    figure_count = markdown.count('[FIGURE:')

    # Check for section markers
    section_count = markdown.count('###')

    return {
        'pdf': pdf_name,
        'length': len(markdown),
        'figures': figure_count,
        'sections': section_count,
        'issues': issues
    }


def test_pdf(pdf_path: Path, parser: PdfParser, test_num: int) -> dict:
    """Test a single PDF and return results."""
    logger.info(f"\n{'='*80}")
    logger.info(f"TEST {test_num}: {pdf_path.name}")
    logger.info(f"{'='*80}")

    try:
        with open(pdf_path, 'rb') as f:
            pdf_bytes = f.read()

        markdown = parser.parse(pdf_bytes)

        # Analyze quality
        analysis = analyze_output_quality(markdown, pdf_path.name)

        # Print preview
        logger.info(f"\nFirst 500 characters:")
        logger.info("-" * 80)
        print(markdown[:500])
        logger.info("-" * 80)

        logger.info(f"\nLast 500 characters:")
        logger.info("-" * 80)
        print(markdown[-500:])
        logger.info("-" * 80)

        # Print analysis
        logger.info(f"\nANALYSIS:")
        logger.info(f"  Length: {analysis['length']} characters")
        logger.info(f"  Figures detected: {analysis['figures']}")
        logger.info(f"  Section headers: {analysis['sections']}")

        if analysis['issues']:
            logger.warning(f"  ISSUES FOUND:")
            for issue in analysis['issues']:
                logger.warning(f"    - {issue}")
        else:
            logger.info(f"  ✓ No obvious issues detected")

        return {
            'status': 'success',
            'analysis': analysis,
            'markdown': markdown
        }

    except Exception as e:
        logger.error(f"ERROR processing {pdf_path.name}: {e}")
        import traceback
        traceback.print_exc()
        return {
            'status': 'error',
            'error': str(e),
            'analysis': {'pdf': pdf_path.name, 'issues': [f'Parse error: {e}']}
        }


def main():
    test_dir = Path('/Users/ivanforcytebio/Projects/PeerPreview/backend/docs/testPDFs')

    # Get all PDF files
    pdf_files = sorted([f for f in test_dir.glob('*.pdf') if not f.name.startswith('.')])

    logger.info(f"Found {len(pdf_files)} PDF files to test")

    parser = PdfParser()

    results = []
    for i, pdf_path in enumerate(pdf_files, 1):
        result = test_pdf(pdf_path, parser, i)
        results.append(result)

    # Summary
    logger.info(f"\n\n{'='*80}")
    logger.info("SUMMARY")
    logger.info(f"{'='*80}")

    for i, result in enumerate(results, 1):
        analysis = result['analysis']
        status = "✓" if result['status'] == 'success' else "✗"
        logger.info(f"\n{i}. {status} {analysis['pdf']}")
        logger.info(f"   Length: {analysis.get('length', 'N/A')} chars, "
                   f"Figures: {analysis.get('figures', 'N/A')}, "
                   f"Sections: {analysis.get('sections', 'N/A')}")

        if analysis['issues']:
            for issue in analysis['issues']:
                logger.info(f"   ⚠ {issue}")

    # Write outputs to files for inspection
    output_dir = test_dir / 'test_outputs'
    output_dir.mkdir(exist_ok=True)

    for result in results:
        if result['status'] == 'success':
            pdf_name = result['analysis']['pdf']
            output_file = output_dir / f"{pdf_name}.md"
            with open(output_file, 'w') as f:
                f.write(result['markdown'])
            logger.info(f"Wrote output to {output_file}")


if __name__ == '__main__':
    main()
