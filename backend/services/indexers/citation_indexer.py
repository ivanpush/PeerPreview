"""Citation indexer for mapping citations to bibliography."""

import re
from typing import Dict, List
from collections import defaultdict
from dataclasses import asdict
from core.models import ParsedDocument, CitationIndex
from core.models import CitationRef as CitationRefModel
from core.models import BibliographyEntry as BibliographyEntryModel


class CitationIndexer:
    """Builds CitationIndex from ParsedDocument."""

    def build(self, doc: ParsedDocument) -> CitationIndex:
        """Build citation index."""
        citation_to_bib = {}
        bib_to_citations = defaultdict(list)

        # Match citations to bibliography entries
        for citation in doc.citations:
            matching_bib = self._find_matching_bib(citation, doc.bibliography)
            if matching_bib:
                citation_to_bib[citation.id] = matching_bib
                bib_to_citations[matching_bib.id].append(citation)

        # Find unmatched items
        unmatched_citations = self._find_unmatched_citations(doc, citation_to_bib)
        unmatched_bib_entries = self._find_unmatched_bib(doc, bib_to_citations)

        # Convert dataclasses to Pydantic models
        citation_to_bib_models = {}
        for cit_id, bib in citation_to_bib.items():
            # Convert dataclass to dict if needed, then to Pydantic model
            bib_dict = asdict(bib) if hasattr(bib, '__dataclass_fields__') else bib
            citation_to_bib_models[cit_id] = BibliographyEntryModel(**bib_dict)

        bib_to_citations_models = {}
        for bib_id, citations in bib_to_citations.items():
            citations_models = []
            for cit in citations:
                cit_dict = asdict(cit) if hasattr(cit, '__dataclass_fields__') else cit
                citations_models.append(CitationRefModel(**cit_dict))
            bib_to_citations_models[bib_id] = citations_models

        return CitationIndex(
            citation_to_bib=citation_to_bib_models,
            bib_to_citations=bib_to_citations_models,
            unmatched_citations=unmatched_citations,
            unmatched_bib_entries=unmatched_bib_entries
        )

    def _find_matching_bib(self, citation, bibliography: List):
        """Find the bibliography entry matching a citation."""
        # For numbered citations [1], [2,3], etc.
        if citation.id.isdigit():
            # Direct match by number
            for bib in bibliography:
                if bib.id == citation.id:
                    return bib
                # Also check if the bibliography text starts with [n] or n.
                if (bib.raw_text.startswith(f"[{citation.id}]") or
                    bib.raw_text.startswith(f"{citation.id}.")):
                    return bib

        # For author-year citations (Smith, 2020)
        else:
            # Extract author and year from citation
            author_year_match = re.match(r'([A-Z][a-z]+)(?:\s+et\s+al\.)?,?\s*(\d{4})', citation.id)
            if author_year_match:
                author = author_year_match.group(1).lower()
                year = author_year_match.group(2)

                # Find in bibliography
                for bib in bibliography:
                    bib_lower = bib.raw_text.lower()
                    if author in bib_lower and year in bib.raw_text:
                        return bib

        return None

    def _find_unmatched_citations(self, doc: ParsedDocument, citation_to_bib: Dict) -> List[str]:
        """Find citations that don't have matching bibliography entries."""
        unmatched = []
        for citation in doc.citations:
            if citation.id not in citation_to_bib:
                # Check if it's already in the list (same citation ID)
                if citation.id not in unmatched:
                    unmatched.append(citation.id)
        return unmatched

    def _find_unmatched_bib(self, doc: ParsedDocument, bib_to_citations: Dict) -> List[str]:
        """Find bibliography entries that are never cited."""
        unmatched = []
        for bib in doc.bibliography:
            if bib.id not in bib_to_citations or not bib_to_citations[bib.id]:
                # Return first 100 chars of the bibliography entry
                unmatched.append(bib.raw_text[:100] + "..." if len(bib.raw_text) > 100 else bib.raw_text)
        return unmatched

    def check_citation_consistency(self, index: CitationIndex) -> Dict[str, List[str]]:
        """Check for various citation consistency issues."""
        issues = {
            "dangling_citations": [],
            "orphaned_bibliography": [],
            "duplicate_citations": []
        }

        # Dangling citations (citations without bib entry)
        issues["dangling_citations"] = index.unmatched_citations

        # Orphaned bibliography (bib entries never cited)
        issues["orphaned_bibliography"] = index.unmatched_bib_entries

        # Check for duplicate bibliography entries
        seen_dois = {}
        for bib_id, bib_entry in index.citation_to_bib.items():
            if bib_entry.doi:
                if bib_entry.doi in seen_dois:
                    issues["duplicate_citations"].append(
                        f"DOI {bib_entry.doi} appears in entries {seen_dois[bib_entry.doi]} and {bib_id}"
                    )
                else:
                    seen_dois[bib_entry.doi] = bib_id

        return issues