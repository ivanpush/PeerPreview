"""Example usage of FigureExtractor."""

import pymupdf
import json
from extractor import FigureExtractor


def example_basic_extraction(pdf_path: str):
    """Basic figure extraction example."""
    print(f"\n=== Basic Figure Extraction ===")
    print(f"PDF: {pdf_path}\n")

    # Open PDF
    doc = pymupdf.open(pdf_path)

    # Extract markdown (simple version)
    raw_markdown = ""
    for page in doc:
        raw_markdown += page.get_text("text")

    # Create extractor
    extractor = FigureExtractor(preserve_positions=True)

    # Extract figures
    cleaned_md, figures = extractor.extract(
        doc=doc,
        raw_markdown=raw_markdown,
        section_headers=[]  # Could use BoldTextAnalyzer here
    )

    # Print results
    print(f"Found {len(figures)} figures\n")

    for i, fig in enumerate(figures, 1):
        print(f"Figure {i}:")
        print(f"  ID: {fig.id}")
        print(f"  Number: {fig.figure_number}")
        print(f"  Caption: {fig.caption_text[:80]}...")
        print(f"  Page: {fig.page_number}")
        print(f"  Placement: {fig.placement_type}")
        print(f"  Action: {fig.suggested_action}")
        if fig.move_reason:
            print(f"  Reason: {fig.move_reason}")
        print()

    # Show cleaned markdown (first 500 chars)
    print("Cleaned markdown (first 500 chars):")
    print(cleaned_md[:500])
    print()

    doc.close()

    return cleaned_md, figures


def example_with_section_headers(pdf_path: str):
    """Example with section header detection."""
    print(f"\n=== Extraction with Section Headers ===")
    print(f"PDF: {pdf_path}\n")

    # Open PDF
    doc = pymupdf.open(pdf_path)

    # Simple section header detection (mock)
    # In real usage, use BoldTextAnalyzer from pdf_parser.py
    section_headers = [
        {'text': 'Introduction', 'page_num': 0},
        {'text': 'Methods', 'page_num': 2},
        {'text': 'Results', 'page_num': 4},
        {'text': 'Discussion', 'page_num': 8},
    ]

    # Extract markdown
    raw_markdown = ""
    for page in doc:
        raw_markdown += page.get_text("text")

    # Create extractor
    extractor = FigureExtractor(preserve_positions=True)

    # Extract figures with section context
    cleaned_md, figures = extractor.extract(
        doc=doc,
        raw_markdown=raw_markdown,
        section_headers=section_headers
    )

    # Print figures grouped by section
    print(f"Found {len(figures)} figures\n")

    sections = {}
    for fig in figures:
        section = fig.section_id or 'unknown'
        if section not in sections:
            sections[section] = []
        sections[section].append(fig)

    for section, figs in sections.items():
        print(f"\n[{section.upper()}] - {len(figs)} figures")
        for fig in figs:
            print(f"  • Figure {fig.figure_number or '?'}: {fig.caption_text[:60]}...")

    doc.close()

    return cleaned_md, figures


def example_export_json(pdf_path: str, output_path: str):
    """Export figures to JSON."""
    print(f"\n=== Export to JSON ===")
    print(f"PDF: {pdf_path}")
    print(f"Output: {output_path}\n")

    # Open PDF
    doc = pymupdf.open(pdf_path)

    # Extract markdown
    raw_markdown = ""
    for page in doc:
        raw_markdown += page.get_text("text")

    # Extract figures
    extractor = FigureExtractor(preserve_positions=False)
    cleaned_md, figures = extractor.extract(doc, raw_markdown)

    # Convert to JSON
    output = {
        'main_text_md': cleaned_md,
        'figures': [fig.to_dict() for fig in figures],
        'metadata': {
            'total_figures': len(figures),
            'total_pages': len(doc)
        }
    }

    # Save
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"Saved {len(figures)} figures to {output_path}")

    doc.close()


def example_analyze_placement(pdf_path: str):
    """Analyze figure placement patterns."""
    print(f"\n=== Placement Analysis ===")
    print(f"PDF: {pdf_path}\n")

    # Open PDF
    doc = pymupdf.open(pdf_path)

    # Extract markdown
    raw_markdown = ""
    for page in doc:
        raw_markdown += page.get_text("text")

    # Extract figures
    extractor = FigureExtractor()
    cleaned_md, figures = extractor.extract(doc, raw_markdown)

    # Analyze placement
    placement_stats = {
        'inline': 0,
        'end_of_section': 0,
        'appendix': 0
    }

    action_stats = {
        'keep_inline': 0,
        'move_to_end': 0,
        'group_with_figures': 0
    }

    for fig in figures:
        placement_stats[fig.placement_type] = placement_stats.get(fig.placement_type, 0) + 1
        action_stats[fig.suggested_action] = action_stats.get(fig.suggested_action, 0) + 1

    print("Placement Distribution:")
    for ptype, count in placement_stats.items():
        print(f"  {ptype}: {count}")

    print("\nRecommended Actions:")
    for action, count in action_stats.items():
        print(f"  {action}: {count}")

    # Show figures needing movement
    print("\nFigures suggested to move:")
    for fig in figures:
        if fig.suggested_action == 'move_to_end':
            print(f"  • Figure {fig.figure_number} (page {fig.page_number}): {fig.move_reason}")

    doc.close()


if __name__ == "__main__":
    # Example usage
    pdf_path = "sample_paper.pdf"  # Replace with actual path

    # Run examples
    try:
        example_basic_extraction(pdf_path)
        example_with_section_headers(pdf_path)
        example_export_json(pdf_path, "figures_output.json")
        example_analyze_placement(pdf_path)
    except FileNotFoundError:
        print(f"Error: PDF file '{pdf_path}' not found")
        print("\nTo use this example:")
        print("1. Replace 'sample_paper.pdf' with path to your PDF")
        print("2. Run: python example_usage.py")
