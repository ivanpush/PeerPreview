"""
API Routes for review orchestration
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Optional
import logging
import json
import uuid
from datetime import datetime

from models.document import DocumentObject
from models.review import ReviewRequest, ReviewResult, Issue, RubricCode
from agents.orchestrator import OrchestratorAgent, OrchestratorConfig

logger = logging.getLogger(__name__)
router = APIRouter()

# In-memory storage for demo (would use database in production)
review_jobs = {}

@router.post("/run-review")
async def run_review(request: ReviewRequest, background_tasks: BackgroundTasks):
    """
    Main endpoint called by ProcessScreen in dynamic mode.
    Initiates the orchestrator agent to run the complete review pipeline.
    """
    try:
        # Parse document from request
        document = DocumentObject(**request.document)

        # Create orchestrator configuration
        config = OrchestratorConfig(
            depth=request.depth,
            user_prompt=request.user_prompt,
            document_type=request.document_type,
            enable_hostile_review=(request.depth == "heavy")
        )

        # For demo, return mock data immediately
        # In production, this would run async with job tracking
        mock_result = create_mock_review_result(document.document_id, request.depth)

        # In production:
        # job_id = str(uuid.uuid4())
        # review_jobs[job_id] = {"status": "running", "started": datetime.now()}
        # background_tasks.add_task(run_orchestrator_async, job_id, document, config)
        # return {"job_id": job_id, "status": "started"}

        return mock_result

    except Exception as e:
        logger.error(f"Review failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/review-status/{job_id}")
async def get_review_status(job_id: str):
    """
    Check status of a running review job
    """
    if job_id not in review_jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    return review_jobs[job_id]

@router.post("/parse-document")
async def parse_document(file_data: Dict):
    """
    Parse uploaded document into DocumentObject format
    """
    # This would integrate with the PDF parser pipeline
    # For now, return mock parsed document
    return {
        "status": "success",
        "document": create_mock_document()
    }

def create_mock_review_result(document_id: str, depth: str) -> Dict:
    """
    Create mock review result for demo
    Matches the format expected by ReviewScreen
    """
    # Number of issues based on depth
    issue_counts = {
        "light": 8,
        "medium": 15,
        "heavy": 25
    }

    issues = []
    issue_count = issue_counts.get(depth, 15)

    # Generate diverse issues across all rubric codes
    rubric_rotation = [
        ("A1", "Logic Error", "The reasoning in this passage contains a logical fallacy"),
        ("A2", "Insufficient Evidence", "Claims lack supporting evidence"),
        ("A3", "Methodological Issue", "The methodology has limitations"),
        ("A4", "Statistical Error", "Statistical analysis needs improvement"),
        ("B1", "Unclear Writing", "This section lacks clarity"),
        ("B2", "Poor Organization", "The flow could be improved"),
        ("C1", "Overstated Claim", "This claim appears exaggerated"),
        ("C2", "Alternative Ignored", "Alternative explanations not considered"),
    ]

    for i in range(issue_count):
        rubric_info = rubric_rotation[i % len(rubric_rotation)]
        severity = ["high", "medium", "low"][i % 3]

        issue = {
            "issue_id": f"issue_{i+1}",
            "rubric_code": rubric_info[0],
            "severity": severity,
            "paragraph_id": f"p_int_{(i % 3) + 1}",  # Rotate through intro paragraphs
            "sentence_ids": [f"s_int_{(i % 3) + 1}_{(i % 2) + 1}"],
            "title": rubric_info[1],
            "description": f"{rubric_info[2]}. This is issue {i+1} found during {depth} review.",
            "recommendation": f"Consider revising this section to address the {rubric_info[1].lower()}.",
            "metadata": {
                "track": rubric_info[0][0],  # A, B, or C
                "flagged": i < 3  # Flag first 3 issues
            }
        }
        issues.append(issue)

    return {
        "document_id": document_id,
        "issues": issues,
        "summary": (
            f"Review complete using {depth} depth analysis. "
            f"Found {len(issues)} issues across all review tracks. "
            f"Track A identified {len([i for i in issues if i['rubric_code'].startswith('A')])} rigor issues, "
            f"Track B found {len([i for i in issues if i['rubric_code'].startswith('B')])} clarity issues, "
            f"Track C raised {len([i for i in issues if i['rubric_code'].startswith('C')])} critical concerns."
        ),
        "metadata": {
            "depth": depth,
            "completion_time": "2024-01-15T10:30:00Z",
            "tracks_executed": ["A", "B", "C"],
            "total_issues": len(issues)
        }
    }

def create_mock_document() -> Dict:
    """Create mock document for testing"""
    return {
        "document_id": "doc_001",
        "document_type": "academic_manuscript",
        "source_format": "pdf",
        "title": "Sample Academic Paper",
        "sections": [
            {
                "section_id": "sec_intro",
                "section_title": "Introduction",
                "paragraph_ids": ["p_int_1", "p_int_2"]
            }
        ],
        "paragraphs": [
            {
                "paragraph_id": "p_int_1",
                "section_id": "sec_intro",
                "para_type": "text",
                "text": "This is the introduction.",
                "sentences": []
            }
        ],
        "meta": {}
    }

async def run_orchestrator_async(job_id: str, document: DocumentObject, config: OrchestratorConfig):
    """
    Run orchestrator in background (for production)
    """
    try:
        orchestrator = OrchestratorAgent(config)
        result = await orchestrator.run_review(document)
        review_jobs[job_id]["status"] = "completed"
        review_jobs[job_id]["result"] = result.dict()
    except Exception as e:
        logger.error(f"Orchestrator failed for job {job_id}: {str(e)}")
        review_jobs[job_id]["status"] = "failed"
        review_jobs[job_id]["error"] = str(e)

review_router = router