"""
Orchestrator Agent - Main coordinator for the review pipeline

The orchestrator manages the three-phase review process:
1. Planning + Global Map Phase
2. Local Track Execution Phase (A, B, C tracks in parallel)
3. Global Consistency & Aggregation Phase
"""

import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
import asyncio

from agents.planning_agent import PlanningAgent
from agents.track_agents import TrackAAgent, TrackBAgent, TrackCAgent
from agents.aggregator_agent import AggregatorAgent
from agents.hostile_agent import HostileAgent
from models.document import DocumentObject
from models.review import ReviewResult, Issue

logger = logging.getLogger(__name__)

@dataclass
class OrchestratorConfig:
    depth: str = "medium"  # light, medium, heavy
    user_prompt: Optional[str] = None
    document_type: str = "academic_manuscript"
    enable_hostile_review: bool = True

class OrchestratorAgent:
    """
    Main orchestrator that coordinates all review agents.
    This is called from the /api/run-review endpoint.
    """

    def __init__(self, config: OrchestratorConfig):
        self.config = config

        # Initialize all agents
        self.planning_agent = PlanningAgent()  # Combined planning + global map
        self.track_a_agent = TrackAAgent()  # Rigor
        self.track_b_agent = TrackBAgent()  # Clarity
        self.track_c_agent = TrackCAgent()  # Skeptic
        self.aggregator_agent = AggregatorAgent()
        self.hostile_agent = HostileAgent()

    async def run_review(self, document: DocumentObject) -> ReviewResult:
        """
        Main entry point for review orchestration.
        Executes the complete three-phase review pipeline.
        """
        logger.info(f"Starting review for document: {document.document_id}")

        try:
            # Phase 1: Planning and Global Mapping
            logger.info("Phase 1: Planning and Global Mapping")
            planning_output = await self._phase1_planning(document)

            # Phase 2: Parallel Track Execution
            logger.info("Phase 2: Executing review tracks in parallel")
            track_results = await self._phase2_tracks(document, planning_output)

            # Phase 3: Aggregation and Global Consistency
            logger.info("Phase 3: Aggregation and consistency check")
            final_review = await self._phase3_aggregation(
                document, planning_output, track_results
            )

            return final_review

        except Exception as e:
            logger.error(f"Review orchestration failed: {str(e)}")
            raise

    async def _phase1_planning(self, document: DocumentObject) -> Dict:
        """
        Phase 1: Single global pass for planning and document understanding

        The merged planning agent now handles both:
        - Review planning (priorities, focus areas, strategy)
        - Global mapping (themes, claims, section relationships, critical passages)
        """
        # Single LLM pass that produces both plan and global map
        planning_output = await self.planning_agent.analyze(
            document=document,
            depth=self.config.depth,
            user_prompt=self.config.user_prompt
        )

        # Planning output now contains both plan and global map data
        return planning_output

    async def _phase2_tracks(self, document: DocumentObject, planning_output: Dict) -> Dict:
        """
        Phase 2: Run Track A, B, C agents in parallel
        """
        # Execute all three tracks concurrently
        track_tasks = [
            self.track_a_agent.review(document, planning_output),  # Rigor
            self.track_b_agent.review(document, planning_output),  # Clarity
            self.track_c_agent.review(document, planning_output),  # Skeptic
        ]

        # Wait for all tracks to complete
        results = await asyncio.gather(*track_tasks)

        return {
            "track_a": results[0],
            "track_b": results[1],
            "track_c": results[2]
        }

    async def _phase3_aggregation(
        self,
        document: DocumentObject,
        planning_output: Dict,
        track_results: Dict
    ) -> ReviewResult:
        """
        Phase 3: Aggregate results and ensure global consistency
        """
        # Aggregate all track results
        # The merged planning_output now contains global map data directly
        aggregated = await self.aggregator_agent.aggregate(
            track_results=track_results,
            global_map=planning_output  # Full planning output contains global map data
        )

        # Optional: Run hostile agent for extra scrutiny
        if self.config.enable_hostile_review and self.config.depth == "heavy":
            hostile_review = await self.hostile_agent.hostile_review(
                document=document,
                aggregated_issues=aggregated["issues"]
            )
            # Merge hostile review findings
            aggregated["issues"].extend(hostile_review["additional_issues"])

        # Create final review result
        review_result = ReviewResult(
            document_id=document.document_id,
            issues=aggregated["issues"],
            summary=aggregated["summary"],
            metadata={
                "depth": self.config.depth,
                "document_type": self.config.document_type,
                "tracks_executed": ["A", "B", "C"],
                "hostile_review": self.config.enable_hostile_review
            }
        )

        return review_result