"""Debug extraction to see what's happening with footer and figure text."""

import sys
from pathlib import Path
import pymupdf

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.parser.pipeline import PipelineBuilder, default_config

def debug_extraction():
    pdf_path = Path('/Users/ivanforcytebio/Projects/PeerPreview/backend/docs/testPDFs/test2.pdf')

    with open(pdf_path, 'rb') as f:
        pdf_bytes = f.read()

    # Build with stage capture
    builder = PipelineBuilder(default_config(), capture_stages=True)
    parsed_doc = builder.build(pdf_bytes, "test2.pdf")

    # Check stage outputs
    print("="*80)
    print("STAGE 3: After Geometric Cleaning")
    print("="*80)
    stage3 = builder.stage_outputs.get('03_geometric_cleaning', '')
    print(stage3[-500:])  # Last 500 chars

    print("\n" + "="*80)
    print("STAGE 4: After Extract Markdown")
    print("="*80)
    stage4 = builder.stage_outputs.get('04_extract_markdown', '')

    # Search for footer in stage 4
    if 'nature' in stage4.lower() and 'biomedical' in stage4.lower():
        print("❌ FOOTER FOUND IN STAGE 4!")
        # Find context
        idx = stage4.lower().find('nature biomedical')
        print(f"\nContext around footer:")
        print(stage4[max(0, idx-200):idx+200])
    else:
        print("✅ No footer detected in stage 4")

    # Search for figure garbage
    print("\n" + "="*80)
    print("CHECKING FOR FIGURE GARBAGE (scattered a b d numbers)")
    print("="*80)

    # Look for pattern like "a\n\nb\n\nd\n\n16"
    import re
    scattered_pattern = r'[a-d]\s+[a-d]\s+[a-d]\s+\d+\s+\d+\s+\d+'
    matches = re.findall(scattered_pattern, stage4[:10000])  # First 10k chars

    if matches:
        print(f"❌ FOUND {len(matches)} instances of scattered text")
        for m in matches[:3]:
            print(f"  '{m}'")
    else:
        print("✅ No scattered garbage detected")

    # Check around Figure 6
    fig6_idx = stage4.lower().find('fig. 6')
    if fig6_idx > 0:
        print("\n" + "="*80)
        print("TEXT AROUND FIGURE 6:")
        print("="*80)
        print(stage4[max(0, fig6_idx-300):fig6_idx+500])

if __name__ == '__main__':
    debug_extraction()
