"""
Document models matching frontend structure
"""

from pydantic import BaseModel
from typing import List, Optional, Dict

class Sentence(BaseModel):
    sentence_id: str
    text: str
    position: int

class Paragraph(BaseModel):
    paragraph_id: str
    section_id: str
    para_type: str = "text"
    text: str
    sentences: List[Sentence]
    metadata: Optional[Dict] = {}

class Section(BaseModel):
    section_id: str
    section_title: str
    paragraph_ids: List[str]

class DocumentObject(BaseModel):
    """Main document object matching frontend ReviewScreen expectations"""
    document_id: str
    document_type: str
    source_format: str
    title: str
    authors: Optional[str] = None
    affiliations: Optional[str] = None
    sections: List[Section]
    paragraphs: List[Paragraph]
    meta: Dict = {}
    references: Optional[str] = None