#!/usr/bin/env python3
"""Check for figure artifacts (scattered text, labels) in parsed markdown."""

import sys
import os
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def check_artifacts(md_text, filename):
    """Check for various figure artifact patterns."""

    issues = []
    lines = md_text.split('\n')

    # Pattern 1: Scattered single chars/numbers (likely axis labels)
    # e.g., "a b c d" or "0 5 10 15 20"
    scattered_pattern = re.compile(r'^[a-zA-Z0-9]{1,3}(\s+[a-zA-Z0-9]{1,3}){3,}$')

    # Pattern 2: Mixed alpha-numeric soup (figure legends)
    # e.g., "A B C 1 2 3"
    soup_pattern = re.compile(r'^([A-Z]\s+){3,}|^(\d+\s+){3,}')

    # Pattern 3: Very short isolated lines that aren't section markers
    # e.g., single word on a line between paragraphs

    scattered_lines = []
    soup_lines = []

    for i, line in enumerate(lines):
        stripped = line.strip()

        if not stripped or stripped.startswith('#') or stripped.startswith('**'):
            continue

        # Check for scattered chars
        if scattered_pattern.match(stripped):
            scattered_lines.append((i+1, stripped))

        # Check for soup
        if soup_pattern.match(stripped):
            soup_lines.append((i+1, stripped))

    if scattered_lines:
        issues.append(f"Found {len(scattered_lines)} scattered character lines")
        for line_num, content in scattered_lines[:5]:  # Show first 5
            issues.append(f"  Line {line_num}: {content[:80]}")

    if soup_lines:
        issues.append(f"Found {len(soup_lines)} alpha-numeric soup lines")
        for line_num, content in soup_lines[:5]:
            issues.append(f"  Line {line_num}: {content[:80]}")

    # Summary stats
    total_chars = len(md_text)
    total_lines = len(lines)
    avg_line_length = total_chars / total_lines if total_lines > 0 else 0

    print(f"\n{'='*60}")
    print(f"File: {filename}")
    print(f"{'='*60}")
    print(f"Total characters: {total_chars}")
    print(f"Total lines: {total_lines}")
    print(f"Avg line length: {avg_line_length:.1f}")

    if issues:
        print(f"\n⚠️  ISSUES FOUND:")
        for issue in issues:
            print(f"  {issue}")
    else:
        print(f"\n✓ No obvious figure artifacts detected")

    return len(scattered_lines) + len(soup_lines)


def main():
    test_dir = 'docs/testPDFs/test_outputs'

    if not os.path.exists(test_dir):
        print(f"Error: {test_dir} not found")
        return

    total_artifacts = 0

    for filename in sorted(os.listdir(test_dir)):
        if filename.endswith('.pdf.md'):
            filepath = os.path.join(test_dir, filename)

            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            artifacts = check_artifacts(content, filename)
            total_artifacts += artifacts

    print(f"\n{'='*60}")
    print(f"TOTAL ARTIFACTS ACROSS ALL FILES: {total_artifacts}")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
