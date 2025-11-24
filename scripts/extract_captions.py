"""Extract and save figure captions detected during pre-extraction stages.

This script runs the parser on PDFs and extracts the captions found in Stage 2 (analysis)
before extraction happens, saving them to JSON and Markdown files.
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

sys.path.insert(0, str(Path(__file__).parent.parent / 'backend'))
from services.parser.pipeline import PipelineBuilder, default_config


def extract_captions_from_pdf(pdf_path):
    """Extract captions from a PDF using the analysis stage.

    Args:
        pdf_path: Path to PDF file

    Returns:
        Dict with PDF info and detected captions
    """
    print(f"\n{'='*80}")
    print(f"Extracting captions from: {pdf_path.name}")
    print(f"{'='*80}")

    try:
        # Read PDF
        with open(pdf_path, 'rb') as f:
            pdf_bytes = f.read()

        # Build parser
        config = default_config()
        builder = PipelineBuilder(config)

        # Run just the analysis and geometry stages to get captions
        from services.parser.pipeline.stages import loader, analysis, geometry

        doc = loader.load_pdf(pdf_bytes)
        page_count = len(doc)  # Get page count before analysis
        structure_info = analysis.analyze_structure(doc, config.analysis)

        # Run geometry stage to get captions (they're detected AFTER cropping now)
        doc_cleaned, geom_info = geometry.apply_geometric_cleaning(doc, config.geometry, structure_info)

        # Extract caption data
        captions = []
        for cap in geom_info.figure_captions:
            captions.append({
                'text': cap.text,
                'type': cap.figure_type,
                'number': cap.figure_num,
                'page': cap.page,
                'bbox': {
                    'x0': cap.bbox[0],
                    'y0': cap.bbox[1],
                    'x1': cap.bbox[2],
                    'y1': cap.bbox[3]
                },
                'y_position': cap.y_position,
                'is_bold': cap.is_bold,
                'confidence': cap.confidence,
                'is_standalone': cap.is_standalone
            })

        print(f"\n✓ Found {len(captions)} captions:")
        for i, cap in enumerate(captions, 1):
            print(f"  {i}. [{cap['type']} {cap['number']}] Page {cap['page']}: {cap['text'][:80]}...")

        doc.close()

        return {
            'pdf': pdf_path.name,
            'page_count': page_count,
            'title': structure_info.title,
            'caption_count': len(captions),
            'captions': captions,
            'extracted_at': datetime.now().isoformat()
        }

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


def save_captions_json(results, output_path):
    """Save caption data to JSON file."""
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n📁 Saved JSON to: {output_path}")


def save_captions_markdown(results, output_path):
    """Save caption data to Markdown file."""
    lines = []
    lines.append("# Figure Captions Extracted from PDFs\n")
    lines.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
    lines.append(f"**Total PDFs processed:** {len(results)}\n")
    lines.append(f"**Total captions found:** {sum(r['caption_count'] for r in results)}\n\n")
    lines.append("---\n\n")

    for result in results:
        lines.append(f"## {result['pdf']}\n\n")
        lines.append(f"- **Title:** {result['title']}\n")
        lines.append(f"- **Pages:** {result['page_count']}\n")
        lines.append(f"- **Captions found:** {result['caption_count']}\n\n")

        if result['captions']:
            lines.append("### Detected Captions\n\n")

            # Group by page
            by_page = {}
            for cap in result['captions']:
                page = cap['page']
                if page not in by_page:
                    by_page[page] = []
                by_page[page].append(cap)

            for page in sorted(by_page.keys()):
                lines.append(f"**Page {page}:**\n\n")
                for cap in by_page[page]:
                    # Format caption with metadata
                    bold_indicator = "**BOLD**" if cap['is_bold'] else ""
                    confidence = f"(confidence: {cap['confidence']:.2f})"

                    lines.append(f"- **{cap['type']} {cap['number']}** {bold_indicator} {confidence}\n")
                    lines.append(f"  - Text: {cap['text']}\n")
                    lines.append(f"  - Position: y={cap['y_position']:.1f}\n")
                    lines.append(f"  - Bbox: ({cap['bbox']['x0']:.1f}, {cap['bbox']['y0']:.1f}, {cap['bbox']['x1']:.1f}, {cap['bbox']['y1']:.1f})\n\n")
        else:
            lines.append("*No captions detected*\n\n")

        lines.append("---\n\n")

    with open(output_path, 'w') as f:
        f.writelines(lines)

    print(f"📁 Saved Markdown to: {output_path}")


def main():
    """Extract captions from all test PDFs."""
    test_dir = Path(__file__).parent.parent / 'backend' / 'docs' / 'testPDFs'
    output_dir = test_dir / 'caption_extracts'
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get all PDFs (excluding minimal test file)
    pdf_files = [f for f in test_dir.glob('*.pdf') if f.name != 'test_no_abstract_header.pdf']

    print(f"\n{'#'*80}")
    print(f"# Caption Extraction")
    print(f"# Extracting from {len(pdf_files)} PDFs")
    print(f"{'#'*80}")

    results = []

    for pdf_path in sorted(pdf_files):
        result = extract_captions_from_pdf(pdf_path)
        if result:
            results.append(result)

    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    json_path = output_dir / f'captions_{timestamp}.json'
    md_path = output_dir / f'captions_{timestamp}.md'

    save_captions_json(results, json_path)
    save_captions_markdown(results, md_path)

    # Summary
    print(f"\n{'='*80}")
    print(f"SUMMARY")
    print(f"{'='*80}")
    print(f"\nProcessed {len(results)} PDFs")
    print(f"Total captions found: {sum(r['caption_count'] for r in results)}")
    print(f"\nBreakdown by PDF:")
    for r in results:
        print(f"  - {r['pdf']}: {r['caption_count']} captions")

    print(f"\n✓ Complete!")
    return 0


if __name__ == '__main__':
    sys.exit(main())
