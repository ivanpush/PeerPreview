"""Test reflow stage with all test PDFs."""

import os
from pathlib import Path
from services.parser.pipeline import PipelineBuilder, default_config

def test_pdf(pdf_path: Path, pdf_num: int):
    """Test a single PDF and check for reflow issues."""
    print(f"\n{'='*80}")
    print(f"Testing PDF {pdf_num}: {pdf_path.name}")
    print(f"{'='*80}")

    with open(pdf_path, 'rb') as f:
        pdf_bytes = f.read()

    builder = PipelineBuilder(default_config())
    parsed_doc = builder.build(pdf_bytes, pdf_path.name)

    # Check for common reflow issues
    issues = []

    # Check each section
    for section_name, section in parsed_doc.sections.items():
        text = section.text

        # Issue 1: Lines ending mid-word without hyphen
        lines = text.split('\n')
        for i, line in enumerate(lines[:-1]):
            if line and not line[-1] in '.!?,;: ])"\'':
                # Line doesn't end with punctuation - might be broken
                if lines[i+1] and lines[i+1][0].islower():
                    issues.append(f"Section '{section_name}': Possible broken line:\n  '{line}'\n  '{lines[i+1]}'")

        # Issue 2: Missing line breaks between sentences
        import re
        # Check for sentence endings followed immediately by capitals
        bad_breaks = re.findall(r'\. [A-Z][a-z]+ [A-Z][a-z]+', text)
        if bad_breaks:
            issues.append(f"Section '{section_name}': Possible missing line breaks: {bad_breaks[:3]}")

        # Issue 3: Weird characters from figures
        weird_chars = re.findall(r'[→←↑↓►◄▲▼■□●○★☐☑✓✗×±≈≠≤≥∞∫∑∏√∂∇]', text)
        if weird_chars:
            issues.append(f"Section '{section_name}': Figure residual characters: {set(weird_chars)}")

        # Issue 4: Very long lines (> 500 chars without newline)
        long_lines = [line for line in lines if len(line) > 500]
        if long_lines:
            issues.append(f"Section '{section_name}': {len(long_lines)} very long lines (>500 chars)")

    # Print results
    if issues:
        print(f"\n⚠️  ISSUES FOUND ({len(issues)}):")
        for issue in issues[:10]:  # Show first 10
            print(f"  - {issue}")
        if len(issues) > 10:
            print(f"  ... and {len(issues)-10} more issues")
    else:
        print(f"\n✓ No obvious reflow issues detected")

    # Show sample from first section
    first_section = list(parsed_doc.sections.values())[0] if parsed_doc.sections else None
    if first_section:
        print(f"\nSample from '{first_section.name}' (first 300 chars):")
        print(f"  {first_section.text[:300]}...")

    return issues

def main():
    test_dir = Path('/Users/ivanforcytebio/Projects/PeerPreview/backend/docs/testPDFs')
    pdf_files = sorted([f for f in test_dir.glob('*.pdf') if f.is_file()])

    print(f"Found {len(pdf_files)} test PDFs")

    all_issues = {}
    for i, pdf_path in enumerate(pdf_files, 1):
        try:
            issues = test_pdf(pdf_path, i)
            all_issues[pdf_path.name] = issues
        except Exception as e:
            print(f"\n❌ ERROR processing {pdf_path.name}: {e}")
            all_issues[pdf_path.name] = [f"FATAL ERROR: {e}"]

    # Summary
    print(f"\n\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    for pdf_name, issues in all_issues.items():
        status = "✓" if not issues else f"⚠️  ({len(issues)} issues)"
        print(f"{status} {pdf_name}")

if __name__ == '__main__':
    main()
