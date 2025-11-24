"""
Check what REAL content is lost (not just reformatting).
"""

import sys
from pathlib import Path

if len(sys.argv) > 1:
    pdf_name = sys.argv[1]
else:
    pdf_name = "test2"

output_dir = Path(__file__).parent.parent / 'docs' / 'testPDFs' / 'test_outputs'

unfiltered_file = output_dir / f"{pdf_name}_unfiltered.md"
filtered_file = output_dir / f"{pdf_name}_filtered.md"

with open(unfiltered_file) as f:
    unfiltered = f.read()
with open(filtered_file) as f:
    filtered = f.read()

# Check for important content
checks = [
    ("Authors present", "Ivan Pushkarsky" in filtered),
    ("Abstract present", "cellular force-generation mechanisms are high" in filtered),
    ("Introduction present", "ell-generated mechanical forces" in filtered),
    ("Methods section", "Methods" in filtered or "methods" in filtered),
    ("Results section", "Results" in filtered or "results" in filtered),
    ("References", "References" in filtered or "references" in filtered),
]

print(f"\n{'='*60}")
print(f"CONTENT PRESERVATION CHECK: {pdf_name}.pdf")
print(f"{'='*60}\n")

all_good = True
for check_name, result in checks:
    status = "✓" if result else "✗"
    print(f"{status} {check_name}: {'PRESENT' if result else 'MISSING'}")
    if not result:
        all_good = False

print(f"\n{'='*60}")

# Find unique 10+ word phrases in unfiltered that are NOT in filtered
# This shows real content loss
import re

def extract_phrases(text, min_words=10):
    """Extract phrases of N+ consecutive words."""
    # Split into sentences
    sentences = re.split(r'[.!?]\s+', text)
    phrases = []
    for sent in sentences:
        words = sent.split()
        if len(words) >= min_words:
            # Take first 10 words as representative phrase
            phrase = ' '.join(words[:min_words])
            phrases.append(phrase)
    return set(phrases)

unfiltered_phrases = extract_phrases(unfiltered, min_words=10)
filtered_phrases = extract_phrases(filtered, min_words=10)

lost_phrases = unfiltered_phrases - filtered_phrases

print(f"\nUNIQUE PHRASES LOST (10+ words):")
print(f"{'='*60}\n")

if lost_phrases:
    print(f"Found {len(lost_phrases)} phrases in unfiltered but not in filtered:\n")
    for i, phrase in enumerate(sorted(lost_phrases)[:20], 1):
        print(f"{i}. {phrase[:80]}...")
else:
    print("✓ NO UNIQUE PHRASES LOST - All content preserved!")

print(f"\n{'='*60}")

if all_good and len(lost_phrases) < 10:
    print("✓ VERDICT: Content is well preserved!")
else:
    print(f"⚠ VERDICT: Some content may be lost ({len(lost_phrases)} unique phrases)")

print(f"{'='*60}\n")
