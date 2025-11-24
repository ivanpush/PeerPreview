"""Check if page 1 is being cropped properly."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pymupdf

pdf_path = Path('/Users/ivanforcytebio/Projects/PeerPreview/backend/docs/testPDFs/test2.pdf')
doc = pymupdf.open(pdf_path)

page1 = doc[0]

print("BEFORE CROP:")
print(f"Page 1 rect: {page1.rect}")
print(f"Height: {page1.rect.height}")

# Get text from top 100pt
top_text = ""
for block in page1.get_text("dict")["blocks"]:
    if block.get("type") == 0:
        bbox = block["bbox"]
        if bbox[1] < 100:  # Top 100pt
            text = "".join(
                span.get("text", "")
                for line in block.get("lines", [])
                for span in line.get("spans", [])
            ).strip()
            top_text += text + " "

print(f"\nText in top 100pt:")
print(top_text[:200])

# Now crop
from services.parser.pipeline.stages.geometry import crop_margins, detect_footer_height

# Apply crop
cropped_doc = pymupdf.open(pdf_path)
from services.parser.pipeline.config import default_config
config = default_config()

bottom = detect_footer_height(cropped_doc)
print(f"\nDetected bottom margin: {bottom}pt")

cropped_doc = crop_margins(cropped_doc, top=60, bottom=bottom, left=0)

page1_cropped = cropped_doc[0]
print(f"\nAFTER CROP:")
print(f"Page 1 cropbox: {page1_cropped.cropbox}")
print(f"Cropped height: {page1_cropped.cropbox.height}")

# Get text from cropped page
cropped_text = page1_cropped.get_text()[:300]
print(f"\nFirst 300 chars of cropped text:")
print(cropped_text)

if 'doi.org' in cropped_text.lower() or 'nature biomedical' in cropped_text.lower():
    print("\n❌ HEADER/FOOTER STILL IN CROPPED TEXT!")
else:
    print("\n✅ Header/footer removed")

doc.close()
cropped_doc.close()
