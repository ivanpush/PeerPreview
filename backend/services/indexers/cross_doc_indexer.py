"""Cross-document indexer for consistency checking."""

import re
from typing import Dict, List, Set
from collections import defaultdict
from core.models import ParsedDocument, CrossDocIndex, Sentence


class CrossDocIndexer:
    """Builds CrossDocIndex from ParsedDocument."""

    N_PATTERNS = [
        r'[Nn]\s*=\s*(\d+)',
        r'(\d+)\s+participants?',
        r'(\d+)\s+subjects?',
        r'(\d+)\s+patients?',
        r'sample\s+(?:size|of)\s+(\d+)',
        r'total\s+of\s+(\d+)',
        r'recruited\s+(\d+)',
    ]

    P_VALUE_PATTERN = r'[pP]\s*[<>=]\s*(0\.\d+)'
    PERCENTAGE_PATTERN = r'(\d+(?:\.\d+)?)\s*%'
    MEAN_SD_PATTERN = r'(\d+(?:\.\d+)?)\s*±\s*(\d+(?:\.\d+)?)'

    def build(self, doc: ParsedDocument) -> CrossDocIndex:
        """Build cross-document index."""
        ns_by_section = {}
        key_numbers = defaultdict(list)
        term_to_sentence_ids = defaultdict(list)
        notation_map = {}

        # Process each section
        for section_name, section in doc.sections.items():
            # Extract N values
            ns_by_section[section_name] = self._extract_ns(section.text)

            # Extract key numbers
            for p_val in self._extract_p_values(section.text):
                key_numbers["p_values"].append(p_val)

            for pct in self._extract_percentages(section.text):
                key_numbers["percentages"].append(pct)

            for mean, sd in self._extract_means_sds(section.text):
                key_numbers["means"].append(mean)
                key_numbers["sds"].append(sd)

            # Build term index
            for sentence in section.sentences:
                terms = self._extract_key_terms(sentence.text)
                for term in terms:
                    term_to_sentence_ids[term.lower()].append(sentence.id)

        # Extract notation (simplified for now)
        notation_map = self._extract_notation(doc.raw_markdown)

        return CrossDocIndex(
            ns_by_section=ns_by_section,
            key_numbers=dict(key_numbers),
            term_to_sentence_ids=dict(term_to_sentence_ids),
            notation_map=notation_map
        )

    def _extract_ns(self, text: str) -> List[int]:
        """Extract sample sizes from text."""
        ns = []
        for pattern in self.N_PATTERNS:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    n = int(match.group(1))
                    if 1 <= n <= 100000:  # Reasonable range
                        ns.append(n)
                except (ValueError, IndexError):
                    pass
        return list(set(ns))  # Remove duplicates

    def _extract_p_values(self, text: str) -> List[float]:
        """Extract p-values from text."""
        p_values = []
        matches = re.finditer(self.P_VALUE_PATTERN, text)
        for match in matches:
            try:
                p = float(match.group(1))
                if 0 <= p <= 1:
                    p_values.append(p)
            except (ValueError, IndexError):
                pass
        return p_values

    def _extract_percentages(self, text: str) -> List[float]:
        """Extract percentages from text."""
        percentages = []
        matches = re.finditer(self.PERCENTAGE_PATTERN, text)
        for match in matches:
            try:
                pct = float(match.group(1))
                if 0 <= pct <= 100:
                    percentages.append(pct)
            except (ValueError, IndexError):
                pass
        return percentages

    def _extract_means_sds(self, text: str) -> List[tuple]:
        """Extract mean ± SD values."""
        results = []
        matches = re.finditer(self.MEAN_SD_PATTERN, text)
        for match in matches:
            try:
                mean = float(match.group(1))
                sd = float(match.group(2))
                results.append((mean, sd))
            except (ValueError, IndexError):
                pass
        return results

    def _extract_key_terms(self, text: str) -> Set[str]:
        """Extract important terms from sentence."""
        # Statistical terms
        stat_terms = {'ANOVA', 'regression', 't-test', 'chi-square', 'Mann-Whitney',
                      'Wilcoxon', 'Kruskal-Wallis', 'correlation', 'linear model'}

        # Medical/scientific terms (can be expanded)
        sci_terms = {'treatment', 'control', 'placebo', 'intervention', 'outcome',
                     'baseline', 'follow-up', 'primary', 'secondary', 'endpoint'}

        found_terms = set()
        text_lower = text.lower()

        for term in stat_terms | sci_terms:
            if term.lower() in text_lower:
                found_terms.add(term)

        return found_terms

    def _extract_notation(self, markdown: str) -> Dict[str, str]:
        """Extract mathematical notation definitions."""
        notation = {}

        # Look for patterns like "α = 0.05" or "N = sample size"
        patterns = [
            r'([α-ωΑ-Ω])\s*[=:]\s*([^,\n]+)',  # Greek letters
            r'([A-Z])\s*[=:]\s*(?:the\s+)?([^,\n]+)',  # Capital letters
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, markdown)
            for match in matches:
                symbol = match.group(1)
                definition = match.group(2).strip()
                if len(definition) < 100:  # Reasonable length
                    notation[symbol] = definition

        # Add common defaults
        if 'α' not in notation:
            notation['α'] = 'significance level'
        if 'N' not in notation:
            notation['N'] = 'sample size'
        if 'p' not in notation:
            notation['p'] = 'p-value'

        return notation

    def find_sentences_by_term(self, doc: ParsedDocument, term: str) -> List[Sentence]:
        """Helper to find all sentences containing a term."""
        sentences = []
        term_lower = term.lower()

        for section in doc.sections.values():
            for sentence in section.sentences:
                if term_lower in sentence.text.lower():
                    sentences.append(sentence)

        return sentences

    def find_n_contradictions(self, index: CrossDocIndex) -> List[tuple]:
        """Find contradictory N values across sections."""
        contradictions = []

        sections = list(index.ns_by_section.keys())
        for i, sec1 in enumerate(sections):
            for sec2 in sections[i+1:]:
                ns1 = set(index.ns_by_section[sec1])
                ns2 = set(index.ns_by_section[sec2])

                # If sections have N values and they don't match
                if ns1 and ns2 and not ns1.intersection(ns2):
                    # Check if values are close (might be subsample)
                    for n1 in ns1:
                        for n2 in ns2:
                            if abs(n1 - n2) <= 2:  # Allow small differences
                                continue
                            elif n1 > n2 * 1.5 or n2 > n1 * 1.5:  # Significant difference
                                contradictions.append((
                                    sec1, n1, sec2, n2
                                ))

        return contradictions