"""Debug script to visualize each parsing step."""

import sys
import os
import glob
import pymupdf
import pymupdf.layout
import re

def save_step(step_num, step_name, text, max_chars=2000):
    """Save and display a parsing step."""
    print(f"\n{'='*80}")
    print(f"STEP {step_num}: {step_name}")
    print(f"{'='*80}")
    print(f"Length: {len(text)} chars")
    print(f"\nFirst {max_chars} chars:")
    print(text[:max_chars])
    print(f"\n... (truncated)" if len(text) > max_chars else "")

    # Save to file
    safe_name = step_name.replace(' ', '_').replace('/', '_').replace('(', '').replace(')', '').lower()
    filename = f"step_{step_num}_{safe_name}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Saved to: {filename}")


def debug_parse(pdf_path):
    """Parse PDF and show each step."""

    # Delete old step files
    old_files = glob.glob("step_*.txt")
    if old_files:
        print(f"Deleting {len(old_files)} old step files...")
        for f in old_files:
            os.remove(f)

    # Read PDF
    with open(pdf_path, 'rb') as f:
        pdf_bytes = f.read()

    print(f"Processing: {pdf_path}")
    print(f"File size: {len(pdf_bytes)} bytes")

    # STEP 1: Basic text extraction with manual header/footer cropping
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    md_text = ""
    for page in doc:
        # Crop header/footer manually (top 10%, bottom 10%)
        rect = page.rect
        header_height = rect.height * 0.10
        footer_start = rect.height * 0.90
        crop_rect = pymupdf.Rect(0, header_height, rect.width, footer_start)

        # Extract text from cropped region
        page_text = page.get_text("text", clip=crop_rect)
        md_text += page_text + "\n\n"

    save_step(1, "Raw text with header/footer cropping", md_text)

    # STEP 2: Detect line numbers
    lines = md_text.split('\n')
    standalone_numbers = 0
    for line in lines:
        stripped = line.strip()
        if stripped.isdigit() and 1 <= len(stripped) <= 3:
            standalone_numbers += 1

    has_line_numbers = standalone_numbers >= 10

    print(f"\n{'='*80}")
    print(f"LINE NUMBER DETECTION: {standalone_numbers} standalone numbers found")
    print(f"Has line numbers: {has_line_numbers}")
    print(f"{'='*80}")

    # STEP 3: Remove line numbers and stitch (if detected)
    if has_line_numbers:
        result = []
        current_paragraph = []

        for line in lines:
            stripped = line.strip()

            # Empty line = paragraph boundary
            if not stripped:
                if current_paragraph:
                    result.append(' '.join(current_paragraph))
                    current_paragraph = []
                result.append('')
                continue

            # Skip standalone line numbers
            if stripped.isdigit() and 1 <= len(stripped) <= 3:
                continue

            current_paragraph.append(stripped)

        if current_paragraph:
            result.append(' '.join(current_paragraph))

        md_text = '\n'.join(result)
        save_step(2, "After removing line numbers and stitching", md_text)
    else:
        save_step(2, "No line numbers detected - text as-is", md_text)

    doc.close()

    # STEP 3: Remove figure/table blocks
    text = md_text
    text = re.sub(r'picture\s*\[\d+\s*x\s*\d+\]\s*intentionally omitted', '[Figure]', text, flags=re.IGNORECASE)
    text = re.sub(r'=+>\s*picture.*?intentionally omitted\s*<==+', '[Figure]', text, flags=re.IGNORECASE)
    text = re.sub(
        r'-{5,}\s*Start of picture text\s*-{5,}.*?-{5,}\s*End of picture text\s*-{5,}',
        '[Figure]',
        text,
        flags=re.DOTALL | re.IGNORECASE
    )
    text = re.sub(r'(?m)^\|.*\|$\n?', '', text)
    text = re.sub(r'(?m)^[\-\s\|]+$\n?', '', text)
    text = re.sub(r'(?m)^Fig\.\s+\d+[a-z]?\s*\|.*$\n?', '', text, flags=re.IGNORECASE)

    save_step(3, "After removing figure/table blocks", text)

    # STEP 4: Clean artifacts
    artifacts = [
        'Author Manuscript',
        'HHS Public Access',
        'NIH Public Access',
        'bioRxiv preprint',
        'which was not certified by peer review'
    ]
    for artifact in artifacts:
        text = text.replace(artifact, '')

    text = re.sub(r'^doi:\s*10\.\d+/[^\n]+\n', '', text, flags=re.MULTILINE)
    text = re.sub(r'(?:available under.*?license|copyright.*?holder)[^\n]*\n?', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip()

    save_step(4, "After cleaning artifacts", text)

    # STEP 5: Final cleanup
    text = re.sub(r'\[Figure\]', '\n\n[Figure]\n\n', text)
    text = re.sub(r'\n[a-d]\n', '\n', text)
    text = re.sub(r'(?m)^n\s*[=>]\s*[\d,]+\s*$', '', text)
    text = re.sub(r'(?m)^[Pp]\s*[<>]\s*[\d.]+\s*$', '', text)
    text = re.sub(r'Scale bars?,?\s*[\d.]+\s*[μµ]?m', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\b[A-Z]+[a-z]+[A-Z]+[a-z]*\s+[A-Z]+[a-z]+[A-Z]+[a-z]*\b', '', text)
    text = re.sub(r'\n{4,}', '\n\n', text)
    text = re.sub(r' {3,}', ' ', text)
    text = text.strip()

    save_step(5, "After final cleanup", text)

    # STEP 6: Format sections
    lines = text.split('\n')
    formatted_lines = []

    for line in lines:
        if not line.strip():
            formatted_lines.append("")
            continue

        stripped = line.strip()
        if len(stripped) > 80 or len(stripped) < 3:
            formatted_lines.append(line)
            continue

        exact_sections = [
            'abstract', 'introduction', 'background', 'methods',
            'materials and methods', 'results', 'discussion',
            'conclusion', 'conclusions', 'references', 'acknowledgments',
            'acknowledgements', 'bibliography', 'supplementary', 'appendix',
            'significance', 'keywords', 'author contributions', 'data availability'
        ]

        lower = stripped.lower()
        clean_line = re.sub(r'^\d+\.?\d*\.?\s*', '', lower)

        is_section = False
        if clean_line in exact_sections:
            is_section = True
        elif stripped.isupper() and lower in exact_sections:
            is_section = True
        elif stripped.startswith('**') and any(sec in lower for sec in exact_sections):
            is_section = True

        if is_section:
            section_name = line.strip().lstrip('0123456789. ').upper()
            formatted_lines.append(f"\n### **{section_name}**\n")
        else:
            formatted_lines.append(line)

    final_text = '\n'.join(formatted_lines)

    save_step(6, "Final formatted output", final_text)

    print(f"\n{'='*80}")
    print("DONE! All steps saved to files.")
    print(f"{'='*80}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python debug_parser_steps.py <path_to_pdf>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    debug_parse(pdf_path)
