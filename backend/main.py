"""Main FastAPI application for manuscript review system."""

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uuid
import os
import logging
from datetime import datetime
import hashlib

from core.config import settings
from core.models import ParsedDocument, FullReviewOutput
from services.parser.pdf_parser import DocumentBuilder
from services.indexers.cross_doc_indexer import CrossDocIndexer
from services.indexers.citation_indexer import CitationIndexer
from services.indexers.figure_indexer import FigureIndexer

# Configure logging
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="PeerPreview API",
    description="AI-powered manuscript review system",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for demo (replace with database in production)
documents_store: Dict[str, ParsedDocument] = {}
reviews_store: Dict[str, FullReviewOutput] = {}
processing_status: Dict[str, str] = {}
builders_store: Dict[str, Any] = {}  # Store builder instances for stage debugging


# ============== Request/Response Models ==============

class UploadResponse(BaseModel):
    document_id: str
    title: str
    sections: list[str]
    section_validation: dict[str, bool]  # e.g., {"has_introduction": True, "has_methods": False}
    message: str


class ReviewRequest(BaseModel):
    document_id: str
    track_b_enabled: bool = True
    agents_to_run: Optional[list[str]] = None  # None means all agents


class StatusResponse(BaseModel):
    document_id: str
    status: str
    message: Optional[str] = None
    progress: Optional[float] = None


# ============== Health Check ==============

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "PeerPreview API",
        "version": "0.1.0",
        "demo_mode": settings.demo_mode
    }


@app.get("/health")
async def health():
    """Detailed health check."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "pdf_parser": "ready",
            "llm_providers": {
                "claude": bool(settings.claude_api_key),
                "openai": bool(settings.openai_api_key),
                "groq": bool(settings.groq_api_key)
            }
        }
    }


# ============== Document Upload ==============

@app.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload and parse a PDF document."""
    try:
        # Validate file type
        if not file.filename.endswith('.pdf'):
            raise HTTPException(400, "Only PDF files are supported")

        # Check file size
        contents = await file.read()
        if len(contents) > settings.max_file_size:
            raise HTTPException(413, f"File too large. Maximum size is {settings.max_file_size / 1024 / 1024}MB")

        # Parse document
        logger.info(f"Parsing document: {file.filename}")
        builder = DocumentBuilder(capture_stages=True)  # Enable stage capture for debugging
        parsed_doc = builder.build(contents, file.filename)

        # Store document and builder
        documents_store[parsed_doc.doc_id] = parsed_doc
        builders_store[parsed_doc.doc_id] = builder  # Store for stage debugging
        processing_status[parsed_doc.doc_id] = "uploaded"

        # Check if this is the demo paper
        if settings.demo_mode and parsed_doc.doc_hash == settings.demo_paper_hash:
            logger.info("Demo paper detected")

        # Validate sections
        from services.parser.pipeline.stages.formatting import validate_required_sections
        # Check if we have authors from Phase 4 detection
        has_authors = bool(builder.structure_info and
                          builder.structure_info.authors and
                          len(builder.structure_info.authors.authors) > 0)
        section_validation = validate_required_sections(
            parsed_doc.sections,
            title=parsed_doc.title,
            has_authors=has_authors
        )

        return UploadResponse(
            document_id=parsed_doc.doc_id,
            title=parsed_doc.title,
            sections=list(parsed_doc.sections.keys()),
            section_validation=section_validation,
            message="Document uploaded and parsed successfully"
        )

    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise HTTPException(500, str(e))


# ============== Document Analysis ==============

@app.get("/document/{document_id}")
async def get_document(document_id: str):
    """Get parsed document details."""
    if document_id not in documents_store:
        raise HTTPException(404, "Document not found")

    doc = documents_store[document_id]

    # Build indices for analysis
    cross_index = CrossDocIndexer().build(doc)
    citation_index = CitationIndexer().build(doc)
    figure_index = FigureIndexer().build(doc)

    # Validate sections
    from services.parser.pipeline.stages.formatting import validate_required_sections
    # Check if we have authors from Phase 4 detection
    builder = builders_store.get(document_id)
    has_authors = bool(builder and builder.structure_info and
                      builder.structure_info.authors and
                      len(builder.structure_info.authors.authors) > 0)
    section_validation = validate_required_sections(
        doc.sections,
        title=doc.title,
        has_authors=has_authors
    )

    return {
        "document_id": doc.doc_id,
        "title": doc.title,
        "raw_markdown": doc.raw_markdown,
        "sections": {
            name: {
                "text": section.text[:500] + "..." if len(section.text) > 500 else section.text,
                "sentence_count": len(section.sentences),
                "word_count": len(section.text.split())
            }
            for name, section in doc.sections.items()
        },
        "section_validation": section_validation,
        "statistics": {
            "total_citations": len(doc.citations),
            "total_bibliography": len(doc.bibliography),
            "total_figures": len(doc.figures),
            "figure_references": len(doc.figure_refs),
            "sample_sizes": cross_index.ns_by_section,
            "unmatched_citations": citation_index.unmatched_citations,
            "orphaned_figures": [f.label for f in figure_index.orphaned_figures],
            "dangling_figure_refs": [r.label for r in figure_index.dangling_refs]
        }
    }


# ============== Review Trigger ==============

@app.post("/review")
async def trigger_review(request: ReviewRequest, background_tasks: BackgroundTasks):
    """Trigger the review process for a document."""
    if request.document_id not in documents_store:
        raise HTTPException(404, "Document not found")

    # Check if already processing
    if processing_status.get(request.document_id) == "processing":
        raise HTTPException(409, "Review already in progress")

    # Start processing
    processing_status[request.document_id] = "processing"

    # In production, this would use Celery or similar
    # For now, we'll use background tasks
    background_tasks.add_task(
        run_review_pipeline,
        request.document_id,
        request.track_b_enabled,
        request.agents_to_run
    )

    return {
        "document_id": request.document_id,
        "status": "processing",
        "message": "Review started. Check status endpoint for progress."
    }


async def run_review_pipeline(document_id: str, track_b_enabled: bool, agents_to_run: Optional[list[str]]):
    """Run the complete review pipeline."""
    try:
        doc = documents_store[document_id]

        # For now, create a mock review
        # In next phase, this will call actual agents
        from core.models import (
            FullReviewOutput, SectionReviewReport, CrossDocReport,
            CitationPoliceReport, FigureReport, GroupedIssues,
            Issue, TextLocation, Severity, OverallStatus
        )

        # Create mock reports
        mock_review = FullReviewOutput(
            document_id=document_id,
            title=doc.title,
            sections=[
                SectionReviewReport(
                    section="methods",
                    track_a_issues=[
                        Issue(
                            issue_type="missing_sample_size",
                            severity=Severity.MAJOR,
                            description="Sample size not explicitly stated",
                            location=TextLocation(
                                section="methods",
                                quote="participants were recruited"
                            )
                        )
                    ],
                    track_b_suggestions=[],
                    passed_checks=["IRB statement present", "Statistical methods described"]
                )
            ],
            cross_doc=CrossDocReport(
                issues=[],
                consistency_score=0.85,
                ns_found={"methods": [150], "results": [150]}
            ),
            citation_police=CitationPoliceReport(
                total_citations=len(doc.citations),
                lazy_citations=[],
                imprecise_citations=[],
                appropriate_citations=len(doc.citations)
            ),
            figures=FigureReport(
                total_figures=len(doc.figures),
                track_a_issues=[],
                track_b_suggestions=[],
                passed_checks=["Sequential numbering", "All figures referenced"]
            ),
            grouped_issues=GroupedIssues(
                major_issues=[],
                minor_issues=[],
                additional_comments=[],
                guideline_violations=[]
            ),
            overall_status=OverallStatus.MAJOR_ISSUES,
            summary="Document has 1 major issue that should be addressed.",
            processing_time_seconds=12.5
        )

        # Store review
        reviews_store[document_id] = mock_review
        processing_status[document_id] = "completed"

    except Exception as e:
        logger.error(f"Review pipeline failed: {e}")
        processing_status[document_id] = f"failed: {str(e)}"


# ============== Status & Results ==============

@app.get("/status/{document_id}", response_model=StatusResponse)
async def get_status(document_id: str):
    """Get processing status for a document."""
    if document_id not in documents_store:
        raise HTTPException(404, "Document not found")

    status = processing_status.get(document_id, "unknown")

    return StatusResponse(
        document_id=document_id,
        status=status,
        message=f"Document is {status}",
        progress=0.5 if status == "processing" else 1.0 if status == "completed" else 0.0
    )


@app.get("/results/{document_id}")
async def get_results(document_id: str):
    """Get review results for a document."""
    if document_id not in reviews_store:
        # Check if still processing
        if processing_status.get(document_id) == "processing":
            raise HTTPException(202, "Review still in progress")
        raise HTTPException(404, "No results found for this document")

    review = reviews_store[document_id]
    return review.dict()


# ============== Debug Endpoints (remove in production) ==============

@app.get("/debug/documents")
async def list_documents():
    """List all uploaded documents (debug only)."""
    if not settings.debug:
        raise HTTPException(403, "Debug endpoints disabled")

    return {
        "documents": [
            {
                "id": doc_id,
                "title": doc.title,
                "status": processing_status.get(doc_id, "unknown"),
                "sections": list(doc.sections.keys())
            }
            for doc_id, doc in documents_store.items()
        ]
    }


@app.delete("/debug/clear")
async def clear_all():
    """Clear all stored data (debug only)."""
    if not settings.debug:
        raise HTTPException(403, "Debug endpoints disabled")

    documents_store.clear()
    reviews_store.clear()
    processing_status.clear()
    builders_store.clear()

    return {"message": "All data cleared"}


@app.get("/debug/pipeline-stages/{document_id}")
async def get_pipeline_stages(document_id: str):
    """Get all pipeline stage outputs for debugging (debug only)."""
    if not settings.debug:
        raise HTTPException(403, "Debug endpoints disabled")

    if document_id not in builders_store:
        raise HTTPException(404, "Document not found or stages not captured")

    builder = builders_store[document_id]

    # Return stages with nice labels (updated for refactored pipeline)
    stage_labels = {
        "01_raw_pdf": "1. Raw PDF Text",
        "02_analyze_structure": "2. Structure Analysis (Title, Abstract, Sections)",
        "03_geometric_cleaning": "3. Geometric Cleaning (Crop + Caption Detection + Figure Detection)",
        "04_extract_markdown": "4. Extract Markdown (with Figure Filtering)",
        "05_reflow_text": "5. Reflow Text",
        "06_cleanup_artifacts": "6. Cleanup Artifacts",
        "07_inject_section_labels": "7. Inject Section Labels",
        "08_split_sections": "8. Split into Sections",
        "09_validate_sections": "9. Validate Sections",
        "10_index_sentences": "10. Index Sentences",
        "11_extract_metadata": "11. Extract Metadata",
        "12_final_output": "12. Final Output"
    }

    stages = []
    for key in sorted(builder.stage_outputs.keys()):
        stages.append({
            "id": key,
            "label": stage_labels.get(key, key),
            "content": builder.stage_outputs[key]
        })

    return {
        "document_id": document_id,
        "stages": stages
    }


# ============== Run Server ==============

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=settings.debug)