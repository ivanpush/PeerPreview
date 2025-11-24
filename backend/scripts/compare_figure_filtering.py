"""
Compare figure-filtered vs non-filtered extraction to see what's being removed.
"""

import sys
import os
from pathlib import Path
import difflib
import pymupdf

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.parser.pipeline import PipelineBuilder, default_config


def extract_unfiltered(pdf_path: Path) -> str:
    """Extract using pymupdf4llm directly - no figure filtering."""
    import pymupdf4llm

    doc = pymupdf.open(pdf_path)
    md = pymupdf4llm.to_markdown(doc)
    doc.close()
    return md


def extract_filtered(pdf_path: Path) -> str:
    """Extract using full pipeline WITH figure filtering."""
    with open(pdf_path, 'rb') as f:
        pdf_bytes = f.read()

    config = default_config()
    builder = PipelineBuilder(config)
    parsed_doc = builder.build(pdf_bytes, pdf_path.name)

    return parsed_doc.raw_markdown


def show_diff(unfiltered: str, filtered: str, pdf_name: str):
    """Show what was removed by filtering."""

    print(f"\n{'='*80}")
    print(f"DIFF ANALYSIS: {pdf_name}")
    print(f"{'='*80}\n")

    print(f"Unfiltered length: {len(unfiltered):,} chars")
    print(f"Filtered length: {len(filtered):,} chars")
    removed_chars = len(unfiltered) - len(filtered)
    pct = removed_chars/len(unfiltered)*100 if unfiltered else 0
    print(f"Removed: {removed_chars:,} chars ({pct:.1f}%)\n")

    # Split into lines for diff
    unfiltered_lines = unfiltered.split('\n')
    filtered_lines = filtered.split('\n')

    # Generate unified diff
    diff = list(difflib.unified_diff(
        unfiltered_lines,
        filtered_lines,
        fromfile='unfiltered',
        tofile='filtered',
        lineterm=''
    ))

    if not diff:
        print("✓ No differences (nothing filtered)")
        return

    # Show summary of removed lines
    removed_lines = [line[1:] for line in diff if line.startswith('-') and not line.startswith('---')]
    added_lines = [line[1:] for line in diff if line.startswith('+') and not line.startswith('+++')]

    print(f"Removed lines: {len(removed_lines)}")
    print(f"Added lines: {len(added_lines)}\n")

    # Analyze removed text
    removed_text = '\n'.join(removed_lines)
    removed_words = removed_text.split()

    print(f"Removed word count: {len(removed_words)}")
    print(f"Avg chars per removed line: {len(removed_text)/len(removed_lines) if removed_lines else 0:.1f}")

    # Show first 30 removed lines as examples
    if removed_lines:
        print(f"\n{'='*80}")
        print("EXAMPLES OF REMOVED TEXT (first 30 lines):")
        print(f"{'='*80}\n")

        for i, line in enumerate(removed_lines[:30]):
            truncated = line[:120]
            if len(line) > 120:
                truncated += "..."
            print(f"{i+1:3d}. {truncated}")


def main():
    """Run comparison on a test PDF."""

    if len(sys.argv) > 1:
        pdf_path = Path(sys.argv[1])
    else:
        # Default: test2.pdf
        pdf_path = Path(__file__).parent.parent / 'docs' / 'testPDFs' / 'test2.pdf'

    if not pdf_path.exists():
        print(f"Error: PDF not found: {pdf_path}")
        return

    print(f"Analyzing: {pdf_path.name}")
    print("Extracting unfiltered version...")
    unfiltered = extract_unfiltered(pdf_path)

    print("Extracting filtered version...")
    filtered = extract_filtered(pdf_path)

    show_diff(unfiltered, filtered, pdf_path.name)

    # Save outputs for manual inspection
    output_dir = pdf_path.parent / 'test_outputs'
    output_dir.mkdir(exist_ok=True)

    unfiltered_file = output_dir / f"{pdf_path.stem}_unfiltered.md"
    filtered_file = output_dir / f"{pdf_path.stem}_filtered.md"

    with open(unfiltered_file, 'w') as f:
        f.write(unfiltered)
    with open(filtered_file, 'w') as f:
        f.write(filtered)

    print(f"\n✓ Saved outputs:")
    print(f"  Unfiltered: {unfiltered_file}")
    print(f"  Filtered: {filtered_file}")


if __name__ == "__main__":
    main()
