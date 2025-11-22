"""Pipeline orchestrator - coordinates all stages.

This is the main entry point that runs the complete parsing pipeline.
"""

import hashlib
import uuid
from typing import Optional
import logging

from .config import PipelineConfig, default_config
from .models import ParsedDocument, GeometryInfo, StructureInfo
from .stages import loader, geometry, analysis, extraction, reflow, cleanup, labeling, formatting, indexing
from .extractors import citations, figures, bibliography

logger = logging.getLogger(__name__)


class PipelineBuilder:
    """Coordinates the complete PDF parsing pipeline."""

    def __init__(self, config: Optional[PipelineConfig] = None, capture_stages: bool = False):
        """Initialize pipeline with configuration.

        Args:
            config: Pipeline configuration (uses defaults if None)
            capture_stages: Whether to capture intermediate stage outputs for debugging
        """
        self.config = config or default_config()
        self.capture_stages = capture_stages
        self.stage_outputs = {}  # Store intermediate stage outputs for debug

        if self.config.debug_logging:
            logging.basicConfig(level=logging.DEBUG)

    def build(self, pdf_bytes: bytes, filename: str) -> ParsedDocument:
        """Run complete parsing pipeline.

        Args:
            pdf_bytes: Raw PDF file bytes
            filename: PDF filename

        Returns:
            ParsedDocument with all extracted data

        Pipeline stages:
        1. Load PDF
        2. Analyze structure (bold text)
        3. Apply geometric cleaning
        4. Extract markdown
        5. Reflow text
        6. Cleanup artifacts
        7. Inject section labels
        8. Split into sections
        9. Validate sections
        10. Index sentences
        11. Extract metadata (citations, figures, bibliography)
        """
        logger.info(f"Starting pipeline for {filename}")

        # Generate document ID and hash
        doc_hash = hashlib.sha256(pdf_bytes).hexdigest()
        doc_id = str(uuid.uuid4())

        # Stage 1: Load PDF
        doc = loader.load_pdf(pdf_bytes)
        metadata = loader.extract_metadata(doc)
        loader.validate_pdf(doc)

        # Capture raw text BEFORE any processing
        if self.capture_stages:
            raw_text = ""
            for page in doc:
                raw_text += page.get_text() + "\n\n"
            self.stage_outputs['01_raw_pdf'] = raw_text

        # Stage 2: Analyze structure (before cropping)
        structure_info = analysis.analyze_structure(doc, self.config.analysis)
        if self.capture_stages:
            self.stage_outputs['02_analyze_structure'] = f"Title: {structure_info.title}\nAbstract: {structure_info.abstract[:200] if structure_info.abstract else 'None'}...\nSections found: {len(structure_info.section_headers)}"

        # Stage 3: Geometric cleaning
        doc, geom_info = geometry.apply_geometric_cleaning(doc, self.config.geometry)

        # Capture text AFTER cropping
        if self.capture_stages:
            cropped_text = ""
            for page in doc:
                cropped_text += page.get_text() + "\n\n"
            self.stage_outputs['03_after_crop'] = cropped_text

        # Stage 4: Extract markdown (ignoring images/graphics)
        markdown = extraction.extract_markdown(doc)
        if self.capture_stages:
            self.stage_outputs['04_extract_markdown'] = markdown

        # Stage 5: Reflow text
        markdown = reflow.reflow_text(markdown, self.config.reflow)
        if self.capture_stages:
            self.stage_outputs['05_reflow_text'] = markdown

        # Stage 6: Cleanup artifacts
        markdown = cleanup.cleanup_all(markdown, self.config.cleanup)
        if self.capture_stages:
            self.stage_outputs['06_cleanup_artifacts'] = markdown

        # Stage 7: Inject section labels
        markdown = labeling.inject_section_labels(markdown, structure_info)
        if self.capture_stages:
            self.stage_outputs['07_inject_section_labels'] = markdown

        # Stage 8: Split into sections
        sections = formatting.split_sections(markdown, self.config.sections)
        if self.capture_stages:
            self.stage_outputs['08_split_sections'] = markdown

        # Stage 9: Validate required sections
        validation = formatting.validate_required_sections(sections, self.config.sections)
        if self.capture_stages:
            self.stage_outputs['09_validate_sections'] = markdown
        for check, passed in validation.items():
            if not passed:
                logger.warning(f"Validation failed: {check}")

        # Stage 10: Index sentences
        if self.config.indexing.enable_sentence_indexing:
            sections = indexing.index_sentences(sections, self.config.indexing)
            if self.capture_stages:
                self.stage_outputs['10_index_sentences'] = markdown

        # Stage 11: Extract metadata
        citation_list = []
        figure_list = []
        figure_refs = []
        bib_list = []

        if self.config.extraction.extract_citations:
            citation_list = citations.extract_citations(sections)

        if self.config.extraction.extract_figures:
            figure_list, figure_refs = figures.extract_figures(markdown, sections)

        if self.config.extraction.extract_bibliography:
            bib_section = sections.get('references') or sections.get('bibliography')
            bib_list = bibliography.parse_bibliography(bib_section)

        if self.capture_stages:
            self.stage_outputs['11_extract_metadata'] = markdown
            self.stage_outputs['12_final_output'] = markdown

        # Extract title
        title = structure_info.title or metadata.get('pdf_title', '') or filename

        # Build final document
        parsed_doc = ParsedDocument(
            doc_id=doc_id,
            doc_hash=doc_hash,
            title=title,
            sections=sections,
            figures=figure_list,
            figure_refs=figure_refs,
            citations=citation_list,
            bibliography=bib_list,
            raw_markdown=markdown
        )

        logger.info(f"Pipeline complete: {len(sections)} sections, {len(citation_list)} citations, "
                   f"{len(figure_list)} figures, {len(bib_list)} bibliography entries")

        # Close PDF document
        doc.close()

        return parsed_doc
