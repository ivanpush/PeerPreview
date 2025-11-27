"""
Aggregator Agent - Combines and deduplicates issues from all tracks
"""

import logging
from typing import Dict, List
from models.review import Issue

logger = logging.getLogger(__name__)

class AggregatorAgent:
    """
    Aggregates results from all tracks, deduplicates issues,
    and ensures global consistency
    """

    async def aggregate(self, track_results: Dict, global_map: Dict) -> Dict:
        """
        Aggregate and reconcile all track results
        """
        logger.info("Aggregating results from all tracks")

        # Collect all issues
        all_issues = []
        all_issues.extend(track_results["track_a"]["issues"])
        all_issues.extend(track_results["track_b"]["issues"])
        all_issues.extend(track_results["track_c"]["issues"])

        # Deduplicate similar issues
        deduped_issues = self._deduplicate_issues(all_issues)

        # Check global consistency
        consistent_issues = await self._ensure_consistency(deduped_issues, global_map)

        # Prioritize issues
        prioritized_issues = self._prioritize_issues(consistent_issues)

        # Generate summary
        summary = self._generate_summary(prioritized_issues, track_results)

        return {
            "issues": prioritized_issues,
            "summary": summary,
            "track_statistics": {
                "track_a_count": len(track_results["track_a"]["issues"]),
                "track_b_count": len(track_results["track_b"]["issues"]),
                "track_c_count": len(track_results["track_c"]["issues"]),
                "total_before_dedup": len(all_issues),
                "total_after_dedup": len(deduped_issues),
                "final_count": len(prioritized_issues)
            }
        }

    def _deduplicate_issues(self, issues: List[Issue]) -> List[Issue]:
        """Remove duplicate or highly similar issues"""
        # Would use embedding similarity or heuristics
        # For now, simple dedup by paragraph_id and rubric_code
        seen = set()
        unique_issues = []

        for issue in issues:
            key = (issue.paragraph_id, issue.rubric_code)
            if key not in seen:
                seen.add(key)
                unique_issues.append(issue)

        return unique_issues

    async def _ensure_consistency(self, issues: List[Issue], global_map: Dict) -> List[Issue]:
        """Ensure issues are consistent with global document understanding"""
        # Would cross-check against global map
        return issues

    def _prioritize_issues(self, issues: List[Issue]) -> List[Issue]:
        """Sort issues by importance and severity"""
        # Priority: severity (high > medium > low), then by rubric code
        return sorted(issues, key=lambda x: (
            {"high": 0, "medium": 1, "low": 2}.get(x.severity, 3),
            x.rubric_code
        ))

    def _generate_summary(self, issues: List[Issue], track_results: Dict) -> str:
        """Generate review summary"""
        high_count = len([i for i in issues if i.severity == "high"])
        medium_count = len([i for i in issues if i.severity == "medium"])
        low_count = len([i for i in issues if i.severity == "low"])

        return (
            f"Review complete. Found {len(issues)} issues: "
            f"{high_count} high, {medium_count} medium, {low_count} low severity. "
            f"Track A identified rigor concerns, Track B highlighted clarity issues, "
            f"Track C provided skeptical perspective."
        )