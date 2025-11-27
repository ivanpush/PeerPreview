"""
Planning Agent - Creates review strategy and global understanding in a single pass
"""

import logging
from typing import Dict, List, Optional
from models.document import DocumentObject

logger = logging.getLogger(__name__)

class PlanningAgent:
    """
    Single global-prepass agent that:
    1. Creates review plan based on document type and user requirements
    2. Builds global document map (claims, terms, sections, early hostile sketch)
    3. Feeds both outputs to downstream track reviewers

    This merged approach eliminates duplicate full-document LLM calls.
    """

    async def analyze(
        self,
        document: DocumentObject,
        depth: str,
        user_prompt: Optional[str] = None
    ) -> Dict:
        """
        Single global pass that creates both review plan and global map
        """
        logger.info(f"Planning review and creating global map for {document.document_type}")

        # === PLANNING PHASE ===
        # Analyze document structure
        section_priorities = self._prioritize_sections(document, document.document_type)

        # Determine review focus areas
        focus_areas = self._determine_focus(document.document_type, user_prompt)

        # Create depth-specific strategy
        strategy = self._create_strategy(depth, focus_areas)

        # === GLOBAL MAP PHASE ===
        # Extract key themes and claims
        themes = await self._extract_themes(document)

        # Map section relationships
        section_map = self._map_sections(document)

        # Identify critical passages based on plan priorities
        critical_passages = await self._identify_critical(
            document, section_priorities, focus_areas
        )

        # Create consistency checkpoints
        checkpoints = self._create_checkpoints(themes, section_map)

        # Create document summary
        document_summary = await self._summarize_document(document)

        # === COMBINED OUTPUT ===
        return {
            # Planning outputs
            "document_type": document.document_type,
            "section_priorities": section_priorities,
            "focus_areas": focus_areas,
            "strategy": strategy,
            "custom_instructions": user_prompt,

            # Global map outputs
            "themes": themes,
            "section_map": section_map,
            "critical_passages": critical_passages,
            "consistency_checkpoints": checkpoints,
            "document_summary": document_summary,

            # Metadata
            "depth": depth,
            "total_sections": len(document.sections),
            "estimated_tokens": self._estimate_token_usage(document, depth)
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

    # === GLOBAL MAP METHODS (from merged global_map_agent) ===

    async def _extract_themes(self, document: DocumentObject) -> List[Dict]:
        """Extract main themes and claims from document"""
        # TODO: Implement LLM call to identify key themes
        # For now, return placeholder
        themes = []
        logger.debug("Extracting document themes and claims")
        return themes

    def _map_sections(self, document: DocumentObject) -> Dict:
        """Map relationships between sections"""
        section_map = {}
        for section in document.sections:
            section_map[section.section_id] = {
                "title": section.section_title,
                "paragraph_count": len(section.paragraph_ids),
                "dependencies": [],  # Would analyze cross-references
                "role": section.role if hasattr(section, 'role') else None
            }
        return section_map

    async def _identify_critical(
        self,
        document: DocumentObject,
        section_priorities: Dict,
        focus_areas: List[str]
    ) -> List[Dict]:
        """Identify critical passages needing special attention"""
        # TODO: Implement LLM call to identify key passages based on priorities
        critical_passages = []
        logger.debug("Identifying critical passages based on priorities")
        return critical_passages

    def _create_checkpoints(self, themes: List, section_map: Dict) -> List[Dict]:
        """Create consistency checkpoints for aggregator"""
        checkpoints = []
        # Create checkpoints for cross-section consistency
        for section_id, info in section_map.items():
            checkpoints.append({
                "section": section_id,
                "type": "consistency",
                "check_against": info.get("dependencies", [])
            })
        return checkpoints

    async def _summarize_document(self, document: DocumentObject) -> str:
        """Create concise document summary"""
        # TODO: Implement LLM call to summarize
        # For now, return basic summary
        summary = f"Document: {document.title} ({document.document_type})"
        summary += f" - {len(document.sections)} sections"
        return summary

    def _estimate_token_usage(self, document: DocumentObject, depth: str) -> int:
        """Estimate total token usage based on document size and depth"""
        # Rough estimation based on document size
        total_words = sum(
            len(section.content.split()) if hasattr(section, 'content') else 100
            for section in document.sections
        )

        multiplier = {"light": 1.5, "medium": 3.0, "heavy": 5.0}
        estimated_tokens = int(total_words * multiplier.get(depth, 2.0))

        return estimated_tokens