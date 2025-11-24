import json
import re
import uuid
import os
import glob
import hashlib

class ManuscriptIndexer:
    def __init__(self, raw_text, working_dir="."):
        # Initialize patterns and maps first (before cleaning text)
        self.subsection_pattern = re.compile(r"^(\d+\.\d+(?:\.\d+)?)\s+(.+)$")
        self.figure_mention_pattern = re.compile(r"(?:Figure|Fig)\.?\s+(\d+)", re.IGNORECASE)
        self.table_mention_pattern = re.compile(r"Table\s+(\d+)", re.IGNORECASE)

        self.canonical_map = {
            "ABSTRACT": "abstract",
            "INTRODUCTION": "sec_intro",
            "RESULTS": "sec_results",
            "DISCUSSION": "sec_disc",
            "METHODS": "sec_methods",
            "MATERIALS AND METHODS": "sec_methods",
            "REFERENCES": "sec_refs",
            "ACKNOWLEDGEMENTS": "sec_ack"
        }

        # Clean the text and extract metadata (after patterns are initialized)
        self.raw_text, self.title, self.authors_block = self.clean_and_extract_metadata(raw_text)
        self.working_dir = working_dir
        # Split authors_block into authors and affiliations
        authors, affiliations = self.split_authors_and_affiliations(self.authors_block)

        self.data = {
            "manuscript_id": f"man_{str(uuid.uuid4())[:8]}",
            "title": self.title,
            "authors": authors,
            "affiliations": affiliations,
            "sections": [],
            "paragraphs": [],
            "figures": [],
            "tables": [],
            "issues": []
        }

        # Track counters
        self.subsection_counters = {}
        self.para_counters = {}

    def clean_and_extract_metadata(self, text):
        """
        Heavy-duty cleaner to strip RTF artifacts, extract title/authors, and fix broken lines.
        Returns: (cleaned_text, title, authors_block)
        """
        # --- Step 1: RTF Hex Decoding (e.g., \'92 -> ') ---
        def replace_hex(match):
            try:
                return chr(int(match.group(1), 16))
            except:
                return match.group(0)

        # Common Windows-1252/RTF mappings (use single backslash in raw strings)
        replacements = {
            r"\'91": "'", r"\'92": "'", r"\'93": '"', r"\'94": '"',
            r"\'96": "-", r"\'97": "—", r"\'a0": " ",  r"\'b0": "°",
            r"\'b2": "²", r"\'b5": "µ", r"\\": ""
        }
        for pattern, char in replacements.items():
            text = text.replace(pattern, char)

        # Generic hex replacement for anything else left (e.g. \'e9)
        text = re.sub(r"\'[0-9a-fA-F]{2}", "", text)

        # --- Step 2: Convert RTF Superscript Citations to Bracketed Format ---
        # Handle affiliation markers (letters) - keep as superscript letters
        text = re.sub(r'\\super\s+([a-z])\s*\\nosupersub', r'\1', text)

        # Pattern: \super NUMBER \nosupersub -> [NUMBER]
        # Handles: \super 4,5 \nosupersub and \super 9-11 \nosupersub (dashes already converted)
        def convert_citation(match):
            citation = match.group(1)
            # Remove spaces and normalize em-dashes to regular dashes
            citation = citation.replace(' ', '').replace('—', '-')
            return f" [{citation}]"

        text = re.sub(r'\\super\s+([\d,\s—-]+)\s*\\nosupersub', convert_citation, text)

        # --- Step 3: Strip RTF Control Words ---
        # Remove font declarations and other RTF garbage
        text = re.sub(r"\\f\d+", "", text)  # Font references
        text = re.sub(r"\\fs\d+", "", text)  # Font sizes
        text = re.sub(r"\\[a-z]+\d*", " ", text)  # Other control words
        text = re.sub(r"[{}]", "", text)  # Remove curly braces

        # Remove font name declarations (Arial-BoldMT, etc.)
        text = re.sub(r"^.*[A-Za-z-]+MT;.*$", "", text, flags=re.MULTILINE)
        text = re.sub(r"^.*Helvetica.*$", "", text, flags=re.MULTILINE)
        text = re.sub(r"^.*Arial.*$", "", text, flags=re.MULTILINE)
        text = re.sub(r"^.*Times.*$", "", text, flags=re.MULTILINE)
        text = re.sub(r"^[A-Za-z-]+;.*$", "", text, flags=re.MULTILINE)
        text = re.sub(r"^;\s*;.*$", "", text, flags=re.MULTILINE)
        text = re.sub(r"^\s*\*\s*;.*$", "", text, flags=re.MULTILINE)

        # --- Step 3: Extract Title and Authors ---
        lines = text.splitlines()
        cleaned_lines = []
        title = None
        authors_block = None
        in_authors_section = False

        for i, line in enumerate(lines):
            line = line.strip()

            # Skip empty lines and garbage (but allow single uppercase letters for drop caps)
            if not line:
                continue
            if len(line) < 3 and not (len(line) == 1 and line.isupper()):
                continue

            # Skip RTF artifacts
            if line.lower() in ["eftab720", "tightenfactor0", "pard", "plain"]:
                continue

            # Skip lines that are just punctuation/symbols
            if all(c in ";*\\/ " for c in line):
                continue

            # First substantial line is likely the title
            if not title and len(line) > 20 and not line.startswith("\\") and not self.is_section_header(line):
                title = line
                in_authors_section = True
                continue

            # Look for authors/affiliations after title (before Abstract)
            if in_authors_section:
                # Skip "Authors & Affiliations" heading if present
                if "Authors" in line and "Affiliations" in line:
                    continue

                # Once we hit Abstract or another section, stop collecting authors
                if self.is_section_header(line):
                    in_authors_section = False
                    authors_block = authors_block or "Authors not detected"
                    cleaned_lines.append(line)
                    continue

                # Collect all text before Abstract as authors/affiliations
                if not authors_block:
                    authors_block = line
                else:
                    authors_block += "\n" + line
                continue

            # Regular content (after authors section)
            cleaned_lines.append(line)

        # --- Step 4: Merge Broken Lines ---
        merged_lines = []
        buffer_line = ""

        for line in cleaned_lines:
            line = line.strip()
            if not line:
                if buffer_line:
                    merged_lines.append(buffer_line)
                    buffer_line = ""
                merged_lines.append("")
                continue

            if buffer_line:
                # NEVER merge if buffer is a section header
                if self.is_section_header(buffer_line):
                    merged_lines.append(buffer_line)
                    buffer_line = line
                # Priority 1: If buffer ends with opening parenthesis/bracket, always merge
                elif buffer_line.endswith(("(", "[")):
                    # Add space only if buffer doesn't already end with space
                    if not buffer_line.endswith(" "):
                        buffer_line += " " + line
                    else:
                        buffer_line += line
                # Priority 2: If buffer ends in hyphen, merge without space
                elif buffer_line.endswith("-"):
                    buffer_line = buffer_line[:-1] + line
                # Priority 3: If next line starts lowercase, merge with space
                elif line and line[0].islower() and not self.is_subheading(line):
                    # Special case: if buffer is single uppercase letter (drop cap), merge without space
                    if len(buffer_line) == 1 and buffer_line.isupper():
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

        cleaned_text = "\n\n".join(merged_lines)

        # Use defaults if not found
        if not title:
            title = "Untitled Manuscript"
        if not authors_block:
            authors_block = "Authors not detected"

        return cleaned_text, title, authors_block

    def is_section_header(self, text):
        """Check if text is a section header"""
        if not text:
            return False
        clean = text.strip().upper()
        for key in self.canonical_map.keys():
            if clean.startswith(key) or re.match(rf"^\d+\.?\s*{key}", clean):
                return True
        return False

    def split_authors_and_affiliations(self, authors_block):
        """
        Split the authors_block into separate authors and affiliations strings.
        Heuristic: Lines with institutional keywords are affiliations, rest are authors.
        """
        if not authors_block or authors_block == "Authors not detected":
            return "Authors not detected", "Affiliations not detected"

        lines = authors_block.split('\n')
        authors_lines = []
        affiliation_lines = []

        affiliation_keywords = ["University", "Institute", "Department", "School",
                                "College", "Hospital", "Center", "Centre", "Laboratory",
                                "USA", "UK", "Canada", "@", ".edu", ".org", ".gov"]

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check if line contains institutional keywords
            if any(kw in line for kw in affiliation_keywords):
                affiliation_lines.append(line)
            else:
                authors_lines.append(line)

        authors = "\n".join(authors_lines) if authors_lines else "Authors not detected"
        affiliations = "\n".join(affiliation_lines) if affiliation_lines else "Affiliations not detected"

        return authors, affiliations

    def generate_id(self, prefix):
        return f"{prefix}_{str(uuid.uuid4())[:8]}"

    def generate_sentence_id(self, text):
        """Generate deterministic sentence ID from text hash"""
        hash_obj = hashlib.md5(text.encode('utf-8'))
        return f"s_{hash_obj.hexdigest()[:8]}"

    def identify_canonical_section(self, text_block):
        clean_line = text_block.strip()
        upper_line = clean_line.upper()
        for key, sec_id in self.canonical_map.items():
            # Strict match: "1. INTRODUCTION" or just "INTRODUCTION"
            pattern = rf"^(?:\d+\.?\s*)?{re.escape(key)}\b"
            if re.match(pattern, upper_line) and len(clean_line) < 80:
                return sec_id, clean_line
        return None, None

    def is_subsection_header(self, text_block):
        """Check if text matches subsection pattern like '2.1 Title'"""
        return self.subsection_pattern.match(text_block.strip()) is not None

    def is_subheading(self, text_block):
        clean = text_block.strip()

        # Exclude lines starting with "Fig" or "Figure" (figure references)
        if clean.startswith(("Fig", "Figure")):
            return False

        # Exclude lines ending with closing parenthesis (likely citations or references)
        if clean.endswith(")"):
            return False

        # Must start with a number pattern like "2.1"
        if self.subsection_pattern.match(clean):
            return True
        # Or be very short, capitalized, and NOT end in punctuation
        if len(clean) < 80 and clean[0].isupper() and not clean.endswith(('.', ':', ';')):
            # Avoid false positives like "Table 1."
            if "Table" in clean:
                return False
            # Must have multiple words
            if len(clean.split()) > 1:
                return True
        return False

    def normalize_citations(self, text):
        """
        Convert citations to bracketed format [1], [2,3], [4-6]
        Citations are already converted from RTF \super format during text cleaning.
        This function is a placeholder for any additional normalization if needed.
        """
        # Citations are already handled during RTF cleaning in clean_and_extract_metadata
        # No additional normalization needed here
        return text

    def split_sentences(self, text):
        """Split text into sentences with better handling of abbreviations"""
        # Protect common abbreviations
        text = re.sub(r'\b(Dr|Mr|Mrs|Ms|Prof|Sr|Jr|Fig|et al|vs|etc|i\.e|e\.g)\.\s*', r'\1<DOT> ', text)

        # Split on sentence endings
        sentence_pattern = re.compile(r'([.!?]+)\s+(?=[A-Z])')
        parts = sentence_pattern.split(text)

        sentences = []
        current = ""
        for i, part in enumerate(parts):
            current += part
            if re.match(r'^[.!?]+$', part):  # End of sentence marker
                if current.strip():
                    # Restore protected dots
                    current = current.replace('<DOT>', '.')
                    sentences.append(current.strip())
                current = ""

        # Add remaining text as last sentence
        if current.strip():
            current = current.replace('<DOT>', '.')
            sentences.append(current.strip())

        return sentences if sentences else [text]

    def extract_figure_captions(self):
        """Extract actual figure captions from the text"""
        # Pattern to match "Figure X." or "Figure X:" followed by caption text
        caption_pattern = re.compile(
            r'(?:Figure|Fig\.?)\s+(\d+)[.:]\s*([^\n]+(?:\n(?![A-Z][a-z]+\s+\d+)[^\n]+)*)',
            re.IGNORECASE
        )

        captions = {}
        for match in caption_pattern.finditer(self.raw_text):
            fig_num = match.group(1)
            caption_text = match.group(2).strip()
            # Clean up the caption (remove extra whitespace)
            caption_text = re.sub(r'\s+', ' ', caption_text)
            captions[fig_num] = caption_text

        return captions

    def scan_figures(self):
        # First extract captions
        captions = self.extract_figure_captions()

        # Then find all figure mentions
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

            # Use extracted caption if available, otherwise use placeholder
            caption = captions.get(num, f"Figure {num}")

            self.data["figures"].append({
                "figure_id": fig_id,
                "caption": caption,
                "mentions": [],
                "img_path": img_path,
                "metadata": {"detected_number": int(num)}
            })

    def extract_table_captions(self):
        """Extract actual table captions from the text"""
        caption_pattern = re.compile(
            r'Table\s+(\d+)[.:]\s*([^\n]+(?:\n(?![A-Z][a-z]+\s+\d+)[^\n]+)*)',
            re.IGNORECASE
        )

        captions = {}
        for match in caption_pattern.finditer(self.raw_text):
            table_num = match.group(1)
            caption_text = match.group(2).strip()
            caption_text = re.sub(r'\s+', ' ', caption_text)
            captions[table_num] = caption_text

        return captions

    def scan_tables(self):
        """Scan for table mentions in text"""
        # First extract captions
        captions = self.extract_table_captions()

        found_nums = set(self.table_mention_pattern.findall(self.raw_text))
        for num in sorted(found_nums, key=int):
            caption = captions.get(num, f"Table {num}")

            self.data["tables"].append({
                "table_id": f"table_{num}",
                "caption": caption,
                "mentions": [],
                "metadata": {"detected_number": int(num)}
            })

    def parse(self):
        self.scan_figures()
        self.scan_tables()

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

            # Skip if block looks like an RTF artifact that survived cleaning
            if clean_block in ["\\", "eftab720", "tightenfactor0"]:
                continue

            # Canonical Section Check
            can_id, can_title = self.identify_canonical_section(clean_block)
            if can_id:
                # If we were in references, save the accumulated references block
                if current_sec_id == "sec_refs" and hasattr(self, 'references_text'):
                    self.save_references_block()

                current_sec_id = can_id
                # Initialize counters for this section
                if current_sec_id not in self.para_counters:
                    self.para_counters[current_sec_id] = 0
                    self.subsection_counters[current_sec_id] = 0

                # Only add section if not already present
                if not any(s["section_id"] == current_sec_id for s in self.data["sections"]):
                    self.data["sections"].append({
                        "section_id": current_sec_id,
                        "section_title": clean_block,
                        "paragraph_ids": []
                    })

                # Initialize references accumulator if this is references section
                if current_sec_id == "sec_refs":
                    self.references_text = []

                continue

            # Special handling for references section - accumulate all text
            if current_sec_id == "sec_refs":
                self.references_text.append(clean_block)
                continue

            # Determine paragraph type and generate appropriate ID
            if self.is_subsection_header(clean_block):
                para_type = "subsection_header"
                # Generate semantic ID for subsection headers
                if current_sec_id not in self.subsection_counters:
                    self.subsection_counters[current_sec_id] = 0
                self.subsection_counters[current_sec_id] += 1

                # Extract section prefix (e.g., "res" from "sec_results")
                sec_prefix = current_sec_id.replace("sec_", "")[:3]
                # Extract subsection number from text (e.g., "2_1" from "2.1 Title")
                match = self.subsection_pattern.match(clean_block)
                if match:
                    subsec_num = match.group(1).replace('.', '_')
                    p_id = f"p_{sec_prefix}_sub_{subsec_num}"
                else:
                    p_id = f"p_{sec_prefix}_sub_{self.subsection_counters[current_sec_id]}"
            elif self.is_subheading(clean_block):
                para_type = "subheading"
                # Generate semantic ID for subheadings too
                if current_sec_id not in self.para_counters:
                    self.para_counters[current_sec_id] = 0
                self.para_counters[current_sec_id] += 1

                sec_prefix = current_sec_id.replace("sec_", "")
                if sec_prefix == "abstract":
                    sec_prefix = "abs"
                else:
                    sec_prefix = sec_prefix[:3]

                p_id = f"p_{sec_prefix}_{self.para_counters[current_sec_id]}"
            else:
                para_type = "text"
                # Generate semantic ID for text paragraphs
                if current_sec_id not in self.para_counters:
                    self.para_counters[current_sec_id] = 0
                self.para_counters[current_sec_id] += 1

                sec_prefix = current_sec_id.replace("sec_", "")[:3]
                if sec_prefix == "abs":  # Special case for abstract
                    sec_prefix = "abs"
                p_id = f"p_{sec_prefix}_{self.para_counters[current_sec_id]}"

            # Add paragraph ID to section
            for sec in self.data["sections"]:
                if sec["section_id"] == current_sec_id:
                    sec["paragraph_ids"].append(p_id)
                    break

            # Extract references
            fig_refs = [f"fig_{n}" for n in self.figure_mention_pattern.findall(clean_block)]
            table_refs = [f"table_{n}" for n in self.table_mention_pattern.findall(clean_block)]

            # Update figure/table mentions
            for fig_ref in fig_refs:
                for fig in self.data["figures"]:
                    if fig["figure_id"] == fig_ref:
                        fig["mentions"].append(p_id)
                        break

            for table_ref in table_refs:
                for tbl in self.data["tables"]:
                    if tbl["table_id"] == table_ref:
                        tbl["mentions"].append(p_id)
                        break

            # Split into sentences for text paragraphs
            sentences = []
            if para_type == "text":
                # Normalize citations before splitting into sentences
                normalized_block = self.normalize_citations(clean_block)
                sent_texts = self.split_sentences(normalized_block)
                for idx, sent_text in enumerate(sent_texts):
                    # Generate semantic sentence ID: s_{section_prefix}_{para_num}_{sentence_num}
                    sec_prefix = current_sec_id.replace("sec_", "")
                    if sec_prefix == "abstract":
                        sec_prefix = "abs"
                    else:
                        sec_prefix = sec_prefix[:3]

                    # Extract paragraph number from p_id (e.g., "p_int_3" -> "3")
                    para_num = p_id.split('_')[-1]
                    sent_id = f"s_{sec_prefix}_{para_num}_{idx + 1}"

                    sentences.append({
                        "sentence_id": sent_id,
                        "text": sent_text,
                        "position": idx
                    })

            # Normalize citations in the text
            normalized_text = self.normalize_citations(clean_block)

            para_obj = {
                "paragraph_id": p_id,
                "section_id": current_sec_id,
                "para_type": para_type,
                "text": normalized_text,
                "sentences": sentences,
                "metadata": {
                    "fig_refs": fig_refs,
                    "table_refs": table_refs
                }
            }

            self.data["paragraphs"].append(para_obj)

        # Save references if we ended in the references section
        if current_sec_id == "sec_refs" and hasattr(self, 'references_text'):
            self.save_references_block()

    def save_references_block(self):
        """Save accumulated references as a single text block"""
        if not self.references_text:
            return

        # Join all references into one block
        references_content = "\n\n".join(self.references_text)

        p_id = "p_refs_1"

        # Add paragraph ID to references section
        for sec in self.data["sections"]:
            if sec["section_id"] == "sec_refs":
                sec["paragraph_ids"].append(p_id)
                break

        # Create a single paragraph for all references
        para_obj = {
            "paragraph_id": p_id,
            "section_id": "sec_refs",
            "para_type": "references_block",
            "text": references_content,
            "sentences": [],
            "metadata": {
                "fig_refs": [],
                "table_refs": []
            }
        }

        self.data["paragraphs"].append(para_obj)

    def to_json(self):
        return json.dumps(self.data, indent=2)

if __name__ == "__main__":
    input_filename = "manuscript.txt.rtf"  # Default to RTF file
    output_filename = "parsed_manuscript.json"

    if os.path.exists(input_filename):
        print(f"Processing {input_filename}...")
        with open(input_filename, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        indexer = ManuscriptIndexer(
            raw_text=content,
            working_dir=os.path.dirname(os.path.abspath(input_filename)) or "."
        )
        indexer.parse()

        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(indexer.to_json())

        print(f"\nExtracted Metadata:")
        print(f"Title: {indexer.title[:80]}...")
        print(f"Authors: {indexer.authors_block[:100] if indexer.authors_block else 'Not detected'}...")

        print(f"\nSuccess! JSON saved to: {output_filename}")
        print(f"Sections: {len(indexer.data['sections'])}")
        print(f"Paragraphs: {len(indexer.data['paragraphs'])}")
        print(f"  - Text paragraphs: {len([p for p in indexer.data['paragraphs'] if p['para_type'] == 'text'])}")
        print(f"  - Subsection headers: {len([p for p in indexer.data['paragraphs'] if p['para_type'] == 'subsection_header'])}")
        print(f"Figures: {len(indexer.data['figures'])}")
        print(f"Tables: {len(indexer.data['tables'])}")
        print(f"Issues: {len(indexer.data['issues'])}")
    else:
        print(f"File '{input_filename}' not found.")