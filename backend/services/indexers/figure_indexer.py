"""Figure indexer for mapping figures to references."""

import re
from typing import Dict, List
from collections import defaultdict
from dataclasses import asdict
from core.models import ParsedDocument, FigureIndex
from core.models import FigureBlock as FigureBlockModel
from core.models import FigureRef as FigureRefModel


class FigureIndexer:
    """Builds FigureIndex from ParsedDocument."""

    def build(self, doc: ParsedDocument) -> FigureIndex:
        """Build figure index."""
        label_to_figure = {self._normalize(f.label): f for f in doc.figures}
        label_to_refs = defaultdict(list)

        for ref in doc.figure_refs:
            normalized_label = self._normalize(ref.label)
            label_to_refs[normalized_label].append(ref)

        # Find dangling refs (ref to figure that doesn't exist)
        dangling = []
        for ref in doc.figure_refs:
            if self._normalize(ref.label) not in label_to_figure:
                if not any(d.label == ref.label for d in dangling):  # Avoid duplicates
                    dangling.append(ref)

        # Find orphaned figures (figure never referenced)
        orphaned = []
        for fig in doc.figures:
            if self._normalize(fig.label) not in label_to_refs:
                orphaned.append(fig)

        # Convert dataclasses to Pydantic models
        label_to_figure_models = {}
        for label, fig in label_to_figure.items():
            fig_dict = asdict(fig) if hasattr(fig, '__dataclass_fields__') else fig
            label_to_figure_models[label] = FigureBlockModel(**fig_dict)

        label_to_refs_models = {}
        for label, refs in label_to_refs.items():
            refs_models = []
            for ref in refs:
                ref_dict = asdict(ref) if hasattr(ref, '__dataclass_fields__') else ref
                refs_models.append(FigureRefModel(**ref_dict))
            label_to_refs_models[label] = refs_models

        # Convert dangling and orphaned
        dangling_models = []
        for ref in dangling:
            ref_dict = asdict(ref) if hasattr(ref, '__dataclass_fields__') else ref
            dangling_models.append(FigureRefModel(**ref_dict))

        orphaned_models = []
        for fig in orphaned:
            fig_dict = asdict(fig) if hasattr(fig, '__dataclass_fields__') else fig
            orphaned_models.append(FigureBlockModel(**fig_dict))

        return FigureIndex(
            label_to_figure=label_to_figure_models,
            label_to_refs=label_to_refs_models,
            dangling_refs=dangling_models,
            orphaned_figures=orphaned_models
        )

    def _normalize(self, label: str) -> str:
        """Normalize 'Figure 1', 'Fig. 1', 'FIGURE 1' → 'figure_1'"""
        # Remove all variations of "Figure" or "Fig"
        normalized = re.sub(r'(?i)fig(?:ure)?\.?\s*', '', label)
        # Keep only alphanumeric and replace spaces with underscore
        normalized = re.sub(r'[^a-z0-9]+', '_', normalized.lower())
        return normalized.strip('_')

    def check_figure_consistency(self, index: FigureIndex) -> Dict[str, List]:
        """Check for various figure consistency issues."""
        issues = {
            "dangling_refs": [],
            "orphaned_figures": [],
            "duplicate_numbers": [],
            "numbering_gaps": [],
            "wrong_order": []
        }

        # Dangling references
        for ref in index.dangling_refs:
            issues["dangling_refs"].append({
                "label": ref.label,
                "section": ref.section,
                "sentence": ref.sentence_text[:100]
            })

        # Orphaned figures
        for fig in index.orphaned_figures:
            issues["orphaned_figures"].append({
                "label": fig.label,
                "caption": fig.caption[:100]
            })

        # Check for duplicate figure numbers
        figure_numbers = []
        for label in index.label_to_figure.keys():
            # Extract number from normalized label
            num_match = re.search(r'\d+', label)
            if num_match:
                num = int(num_match.group())
                if num in figure_numbers:
                    issues["duplicate_numbers"].append(f"Figure {num} appears multiple times")
                else:
                    figure_numbers.append(num)

        # Check for gaps in numbering
        if figure_numbers:
            figure_numbers.sort()
            expected = list(range(1, max(figure_numbers) + 1))
            missing = set(expected) - set(figure_numbers)
            for m in missing:
                issues["numbering_gaps"].append(f"Figure {m} is missing")

        # Check if figures are referenced in order
        ref_order = []
        for refs_list in index.label_to_refs.values():
            for ref in refs_list:
                num_match = re.search(r'\d+', ref.label)
                if num_match:
                    num = int(num_match.group())
                    if num not in ref_order:
                        ref_order.append(num)

        # Check if order is sequential
        for i in range(1, len(ref_order)):
            if ref_order[i] < ref_order[i-1]:
                issues["wrong_order"].append(
                    f"Figure {ref_order[i]} referenced before Figure {ref_order[i-1]}"
                )

        return issues

    def get_figure_stats(self, index: FigureIndex) -> Dict[str, int]:
        """Get summary statistics about figures."""
        return {
            "total_figures": len(index.label_to_figure),
            "total_references": sum(len(refs) for refs in index.label_to_refs.values()),
            "dangling_refs": len(index.dangling_refs),
            "orphaned_figures": len(index.orphaned_figures),
            "avg_refs_per_figure": (
                sum(len(refs) for refs in index.label_to_refs.values()) / len(index.label_to_figure)
                if index.label_to_figure else 0
            )
        }