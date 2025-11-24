import json
import re
import uuid
import os
import glob

class ManuscriptIndexer:
    def __init__(self, raw_text, title, authors, working_dir="."):
        self.working_dir = working_dir
        
        # --- Counters for clean IDs ---
        self.counts = {
            "p": 0,
            "sec": 0,
            "fig": 0
        }
        
        # --- 1. Define Patterns & Maps FIRST ---
        self.canonical_map = {
            "ABSTRACT": "sec_abs",
            "INTRODUCTION": "sec_intro",
            "RESULTS": "sec_res",
            "DISCUSSION": "sec_disc",
            "METHODS": "sec_meth",
            "REFERENCES": "sec_ref",
            "ACKNOWLEDGEMENTS": "sec_ack"
        }
        
        # Regex for subheadings (2.1, 2.3)
        self.subheader_pattern = re.compile(r"^\d+\.\d+\s+.*")
        # Regex for figure mentions
        self.figure_mention_pattern = re.compile(r"(?:Figure|Fig)\.?\s+(\d+)", re.IGNORECASE)

        # --- 2. Now safe to clean text ---
        self.raw_text = self.clean_and_normalize_text(raw_text)
        
        self.data = {
            "manuscript_id": "man_001", # Simple ID
            "title": title,
            "authors_block": authors,
            "sections": [],
            "paragraphs": [],
            "figures": []
        }

    def get_next_id(self, prefix):
        """Generates sequential IDs like p_1, p_2 instead of random UUIDs."""
        self.counts[prefix] = self.counts.get(prefix, 0) + 1
        return f"{prefix}_{self.counts[prefix]}"

    def clean_and_normalize_text(self, text):
        """
        Heavy-duty cleaner to strip RTF artifacts and fix broken lines.
        """
        # --- Step 1: RTF Hex Decoding ---
        def replace_hex(match):
            try: return chr(int(match.group(1), 16))
            except: return match.group(0)
        
        replacements = {
            r"\\'91": "'", r"\\'92": "'", r"\\'93": '"', r"\\'94": '"',
            r"\\'96": "-", r"\\'97": "—", r"\\'a0": " ",  r"\\'b0": "°",
            r"\\'b2": "²", r"\\'b5": "µ", r"\\": ""
        }
        for pattern, char in replacements.items():
            text = text.replace(pattern, char)
        text = re.sub(r"\\'[0-9a-fA-F]{2}", "", text) 

        # --- Step 2: Strip RTF Control Words ---
        text = re.sub(r"\\[a-z]+\d*", " ", text) 
        text = re.sub(r"[{}]", "", text)

        # --- Step 3: Merge Broken Lines ---
        lines = text.splitlines()
        merged_lines = []
        buffer_line = ""

        for line in lines:
            line = line.strip()
            if not line:
                if buffer_line:
                    merged_lines.append(buffer_line)
                    buffer_line = ""
                continue
            
            # Filter garbage
            if len(line) < 3 and not line[0].isalnum(): continue
            if any(x in line.lower() for x in ["eftab720", "tightenfactor0", "pard", "plain"]): continue

            if buffer_line:
                # Heuristic 1: Buffer ends in hyphen -> join directly
                if buffer_line.endswith("-"):
                    buffer_line = buffer_line[:-1] + line
                
                # Heuristic 2: Next line starts lower -> it belongs to previous sentence
                elif line[0].islower() and not self.is_subheading(line):
                    # Drop Cap Fix: "C" + "ellular" -> "Cellular"
                    if len(buffer_line) == 1 and buffer_line.isupper() and buffer_line not in ["A", "I"]:
                        buffer_line += line
                    else:
                        buffer_line += " " + line
                else:
                    merged_lines.append(buffer_line)
                    buffer_line = line
            else:
                buffer_line = line
        
        if buffer_line:
            merged_lines.append(buffer_line)

        return "\n\n".join(merged_lines)

    def identify_canonical_section(self, text_block):
        clean_line = text_block.strip()
        upper_line = clean_line.upper()
        for key, sec_id in self.canonical_map.items():
            pattern = rf"^(?:\d+\.?\s*)?{key}\b"
            if re.match(pattern, upper_line) and len(clean_line) < 60:
                return sec_id, clean_line
        return None, None

    def is_subheading(self, text_block):
        clean = text_block.strip()
        
        # 1. Check for explicit numbering "2.1 Results"
        if self.subheader_pattern.match(clean):
            return True
            
        # 2. Heuristic Check
        if len(clean) < 80 and clean[0].isupper() and not clean.endswith(('.', ':', ';')):
            # A. Exclusion: Can't end with connector words (the fix for "In particular, the")
            bad_endings = [' the', ' a', ' an', ' and', ' or', ' but', ' of', ' in', ' with', ' for', ' to']
            if any(clean.lower().endswith(end) for end in bad_endings):
                return False
            
            # B. Exclusion: Can't contain "Figure" or "Table" (captions)
            if "Table" in clean or "Figure" in clean: 
                return False
                
            return True
        return False

    def scan_figures(self):
        found_nums = set(self.figure_mention_pattern.findall(self.raw_text))
        for num in sorted(found_nums, key=int):
            fig_id = f"fig_{num}"
            img_path = None
            search_patterns = [f"fig{num}.*", f"fig_{num}.*", f"figure{num}.*", f"figure_{num}.*"]
            
            for pattern in search_patterns:
                matches = glob.glob(os.path.join(self.working_dir, pattern)) + \
                          glob.glob(os.path.join(self.working_dir, pattern.upper()))
                if matches:
                    img_path = matches[0]
                    break
            
            self.data["figures"].append({
                "figure_id": fig_id,
                "caption": f"Figure {num}",
                "mentions": [],
                "img_path": img_path,
                "metadata": {"detected_number": int(num)}
            })

    def parse(self):
        self.scan_figures()
        blocks = self.raw_text.split('\n\n')
        current_sec_id = "sec_front_matter"
        
        # Ensure front matter section exists
        self.data["sections"].append({
            "section_id": "sec_front_matter",
            "section_title": "Front Matter",
            "paragraph_ids": []
        })

        for block in blocks:
            clean_block = block.strip()
            if not clean_block: continue

            # Final safety check for RTF fragments
            if len(clean_block) < 2 and not clean_block[0].isalnum(): 
                continue

            # Canonical Section Check
            can_id, can_title = self.identify_canonical_section(clean_block)
            if can_id:
                current_sec_id = can_id
                # Only add section if not already present
                if not any(s["section_id"] == current_sec_id for s in self.data["sections"]):
                    self.data["sections"].append({
                        "section_id": current_sec_id,
                        "section_title": clean_block,
                        "paragraph_ids": []
                    })
                continue

            # Paragraph Parsing
            role = "subheading" if self.is_subheading(clean_block) else "body"
            
            # Use sequential ID instead of UUID
            p_id = self.get_next_id("p")

            # Add to current section
            for sec in self.data["sections"]:
                if sec["section_id"] == current_sec_id:
                    sec["paragraph_ids"].append(p_id)
                    break
            
            fig_refs = [f"fig_{n}" for n in self.figure_mention_pattern.findall(clean_block)]

            self.data["paragraphs"].append({
                "paragraph_id": p_id,
                "section_id": current_sec_id,
                "role": role,
                "text": clean_block,
                "sentences": [],
                "metadata": {"fig_refs": fig_refs}
            })

    def to_json(self):
        return json.dumps(self.data, indent=2)

if __name__ == "__main__":
    input_filename = "manuscript.txt.rtf" 
    output_filename = "parsed_manuscript2.json"

    if os.path.exists(input_filename):
        print(f"Processing {input_filename}...")
        with open(input_filename, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
        indexer = ManuscriptIndexer(
            raw_text=content, 
            title="Auto-Detected Title", 
            authors="Auto-Detected Authors",
            working_dir=os.path.dirname(os.path.abspath(input_filename))
        )
        indexer.parse()

        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(indexer.to_json())
        print(f"Done. Saved to {output_filename}")
    else:
        print("File not found.")