"""
Review models for issues and results
"""

from pydantic import BaseModel
from typing import List, Optional, Dict, Literal
from enum import Enum

class RubricCode(str, Enum):
    """Review rubric codes"""
    # Track A - Rigor
    A1 = "A1"  # Logic and reasoning errors
    A2 = "A2"  # Insufficient evidence
    A3 = "A3"  # Methodological problems
    A4 = "A4"  # Statistical errors
    A5 = "A5"  # Missing controls
    A6 = "A6"  # Citation problems

    # Track B - Clarity
    B1 = "B1"  # Unclear writing
    B2 = "B2"  # Poor organization
    B3 = "B3"  # Missing explanations
    B4 = "B4"  # Figure/presentation issues

    # Track C - Skeptical
    C1 = "C1"  # Overstated claims
    C2 = "C2"  # Alternative interpretations ignored
    C3 = "C3"  # Limitations understated
    C4 = "C4"  # Questionable assumptions

class Issue(BaseModel):
    """Individual review issue matching frontend structure"""
    issue_id: str
    rubric_code: RubricCode
    severity: Literal["low", "medium", "high"]
    paragraph_id: str
    sentence_ids: List[str]
    title: str
    description: str
    recommendation: str
    metadata: Optional[Dict] = {}

class ReviewResult(BaseModel):
    """Complete review result"""
    document_id: str
    issues: List[Issue]
    summary: str
    metadata: Dict = {}

class ReviewRequest(BaseModel):
    """Request model for review API"""
    document: Dict  # Will be parsed to DocumentObject
    depth: Literal["light", "medium", "heavy"] = "medium"
    user_prompt: Optional[str] = None
    document_type: str = "academic_manuscript"