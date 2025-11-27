"""
Planning Agent - Creates review strategy based on document type and user requirements
"""

import logging
from typing import Dict, Optional
from models.document import DocumentObject

logger = logging.getLogger(__name__)

class PlanningAgent:
    """
    Analyzes document structure and creates a tailored review plan.
    Determines which sections need most attention based on document type.
    """

    async def analyze(
        self,
        document: DocumentObject,
        depth: str,
        user_prompt: Optional[str] = None
    ) -> Dict:
        """
        Create review plan based on document analysis
        """
        logger.info(f"Planning review for {document.document_type}")

        # Analyze document structure
        section_priorities = self._prioritize_sections(document, document.document_type)

        # Determine review focus areas
        focus_areas = self._determine_focus(document.document_type, user_prompt)

        # Create depth-specific strategy
        strategy = self._create_strategy(depth, focus_areas)

        return {
            "document_type": document.document_type,
            "section_priorities": section_priorities,
            "focus_areas": focus_areas,
            "strategy": strategy,
            "custom_instructions": user_prompt
        }

    def _prioritize_sections(self, document: DocumentObject, doc_type: str) -> Dict:
        """Determine which sections need most scrutiny"""
        priorities = {}

        if doc_type == "academic_manuscript":
            priorities = {
                "methods": "high",
                "results": "high",
                "discussion": "medium",
                "introduction": "low"
            }
        elif doc_type == "grant_proposal":
            priorities = {
                "specific_aims": "high",
                "approach": "high",
                "significance": "medium",
                "innovation": "medium"
            }
        elif doc_type == "policy_brief":
            priorities = {
                "recommendations": "high",
                "analysis": "high",
                "background": "low"
            }

        return priorities

    def _determine_focus(self, doc_type: str, user_prompt: Optional[str]) -> List[str]:
        """Determine key areas to focus review on"""
        base_focus = []

        if doc_type == "academic_manuscript":
            base_focus = ["methodology", "statistical_analysis", "conclusions"]
        elif doc_type == "grant_proposal":
            base_focus = ["feasibility", "innovation", "impact"]
        elif doc_type == "policy_brief":
            base_focus = ["evidence_base", "implementation", "stakeholders"]

        # Parse user prompt for additional focus areas
        if user_prompt:
            if "statistic" in user_prompt.lower():
                base_focus.append("statistical_rigor")
            if "method" in user_prompt.lower():
                base_focus.append("methodology_detail")
            if "clarity" in user_prompt.lower():
                base_focus.append("writing_clarity")

        return base_focus

    def _create_strategy(self, depth: str, focus_areas: List[str]) -> Dict:
        """Create review strategy based on depth"""
        if depth == "light":
            return {
                "approach": "surface_level",
                "time_per_section": "brief",
                "issue_threshold": "major_only",
                "tracks_emphasis": {"A": 0.2, "B": 0.6, "C": 0.2}
            }
        elif depth == "heavy":
            return {
                "approach": "exhaustive",
                "time_per_section": "thorough",
                "issue_threshold": "all_issues",
                "tracks_emphasis": {"A": 0.4, "B": 0.2, "C": 0.4}
            }
        else:  # medium
            return {
                "approach": "balanced",
                "time_per_section": "moderate",
                "issue_threshold": "moderate_and_major",
                "tracks_emphasis": {"A": 0.33, "B": 0.34, "C": 0.33}
            }