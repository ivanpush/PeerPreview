"""Detect gibberish and artifacts that escape cleanup stage."""

import re
from pathlib import Path
from services.parser.pipeline import PipelineBuilder, default_config

def analyze_gibberish(text: str, section_name: str):
    """Analyze text for various types of gibberish."""
    lines = text.split('\n')
    issues = []

    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue

        # Issue 1: Very short lines (1-3 chars) that aren't list markers
        if len(stripped) <= 3 and not re.match(r'^[a-z]\.$|^\d+\.$|^-$|^\*$', stripped):
            issues.append({
                'type': 'short_line',
                'line_num': i,
                'content': stripped,
                'severity': 'high'
            })

        # Issue 2: Lines with only symbols/punctuation
        if len(stripped) > 0 and re.match(r'^[^a-zA-Z0-9\s]+$', stripped):
            issues.append({
                'type': 'symbols_only',
                'line_num': i,
                'content': stripped,
                'severity': 'high'
            })

        # Issue 3: URLs that survived
        if re.search(r'https?://|www\.|\.com|\.org|\.edu|\.gov', stripped, re.IGNORECASE):
            issues.append({
                'type': 'url',
                'line_num': i,
                'content': stripped[:80],
                'severity': 'medium'
            })

        # Issue 4: Email addresses
        if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', stripped):
            issues.append({
                'type': 'email',
                'line_num': i,
                'content': stripped[:80],
                'severity': 'medium'
            })

        # Issue 5: Lines that are mostly numbers/symbols (gibberish coordinates, etc.)
        alpha_count = sum(c.isalpha() for c in stripped)
        if len(stripped) > 5 and alpha_count / len(stripped) < 0.3:
            issues.append({
                'type': 'mostly_numbers',
                'line_num': i,
                'content': stripped[:80],
                'severity': 'medium'
            })

        # Issue 6: Excessive capitalization (>50% caps, likely metadata)
        if len(stripped) > 10:
            upper_count = sum(c.isupper() for c in stripped if c.isalpha())
            alpha_total = sum(c.isalpha() for c in stripped)
            if alpha_total > 0 and upper_count / alpha_total > 0.5:
                issues.append({
                    'type': 'excessive_caps',
                    'line_num': i,
                    'content': stripped[:80],
                    'severity': 'low'
                })

        # Issue 7: Lines with weird unicode symbols (figure remnants)
        weird_chars = re.findall(r'[→←↑↓►◄▲▼■□●○★☐☑✓✗×±≈≠≤≥∞∫∑∏√∂∇∆Δ◊◇]', stripped)
        if weird_chars:
            issues.append({
                'type': 'unicode_symbols',
                'line_num': i,
                'content': stripped[:80],
                'symbols': set(weird_chars),
                'severity': 'high'
            })

        # Issue 8: Lines that are just single repeated characters
        if len(set(stripped.replace(' ', ''))) == 1 and len(stripped) > 3:
            issues.append({
                'type': 'repeated_char',
                'line_num': i,
                'content': stripped[:80],
                'severity': 'high'
            })

        # Issue 9: Lines with excessive spaces (likely table formatting residue)
        if '  ' in stripped and stripped.count('  ') > 3:
            issues.append({
                'type': 'excessive_spacing',
                'line_num': i,
                'content': stripped[:80],
                'severity': 'low'
            })

        # Issue 10: "Half-full" lines - text ending mid-sentence with no punctuation
        if len(stripped) > 20 and len(stripped) < 60:
            # Check if ends without proper terminator
            if not re.search(r'[.!?,;:\]\)"\']$', stripped):
                # Check if next line exists and starts with lowercase (broken line)
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if next_line and next_line[0].islower():
                        issues.append({
                            'type': 'half_full_line',
                            'line_num': i,
                            'content': stripped,
                            'severity': 'medium'
                        })

    return issues

def test_pdf(pdf_path: Path, pdf_num: int):
    """Test a single PDF for gibberish."""
    print(f"\n{'='*80}")
    print(f"PDF {pdf_num}: {pdf_path.name}")
    print(f"{'='*80}")

    with open(pdf_path, 'rb') as f:
        pdf_bytes = f.read()

    builder = PipelineBuilder(default_config())
    parsed_doc = builder.build(pdf_bytes, pdf_path.name)

    all_issues = []
    for section_name, section in parsed_doc.sections.items():
        issues = analyze_gibberish(section.text, section_name)
        for issue in issues:
            issue['section'] = section_name
        all_issues.extend(issues)

    # Group by type
    by_type = {}
    for issue in all_issues:
        issue_type = issue['type']
        if issue_type not in by_type:
            by_type[issue_type] = []
        by_type[issue_type].append(issue)

    # Print summary
    if by_type:
        print(f"\n⚠️  Found {len(all_issues)} issues across {len(by_type)} types:\n")
        for issue_type, items in sorted(by_type.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"  {issue_type}: {len(items)} occurrences")
            # Show first 3 examples
            for item in items[:3]:
                print(f"    - [{item['section']}:{item['line_num']}] {item['content']}")
            if len(items) > 3:
                print(f"    ... and {len(items)-3} more")
    else:
        print("✓ No gibberish detected")

    return all_issues

def main():
    test_dir = Path('/Users/ivanforcytebio/Projects/PeerPreview/backend/docs/testPDFs')
    pdf_files = sorted([f for f in test_dir.glob('*.pdf') if f.is_file() and f.stat().st_size > 10000])

    print(f"Testing {len(pdf_files)} PDFs for gibberish...")

    all_results = {}
    for i, pdf_path in enumerate(pdf_files, 1):
        try:
            issues = test_pdf(pdf_path, i)
            all_results[pdf_path.name] = issues
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            all_results[pdf_path.name] = []

    # Overall summary
    print(f"\n\n{'='*80}")
    print("OVERALL SUMMARY")
    print(f"{'='*80}")

    total_issues = sum(len(issues) for issues in all_results.values())
    print(f"Total issues found: {total_issues}")

    # Most common issue types
    all_types = {}
    for issues in all_results.values():
        for issue in issues:
            issue_type = issue['type']
            all_types[issue_type] = all_types.get(issue_type, 0) + 1

    if all_types:
        print("\nMost common issue types:")
        for issue_type, count in sorted(all_types.items(), key=lambda x: x[1], reverse=True):
            print(f"  {issue_type}: {count}")

if __name__ == '__main__':
    main()
