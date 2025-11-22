"""Data models for figure extraction."""

from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class FigureUnit:
    """Represents an extracted figure with its caption and placement context."""

    # Identity
    id: str                          # auto-generated uuid
    figure_number: Optional[str]     # "1", "2a", None (if unlabeled)

    # Caption content
    caption_text: str                # Clean caption without "Figure 1:" prefix
    raw_caption: str                 # Full caption with prefix

    # Location in PDF
    page_number: int
    image_bbox: Dict                 # {x0, y0, x1, y1} in PDF points
    image_index: int                 # Index in page.get_images()
    caption_bbox: Optional[Dict]     # Caption location for debugging

    # Image data (future)
    image_bytes: Optional[bytes] = None

    # PLACEMENT CONTEXT - critical for understanding document flow
    placement_type: str = "inline"   # "inline" | "end_of_section" | "appendix"
    markdown_position: Optional[int] = None  # Character index in original markdown
    surrounding_context: Optional[str] = None  # ~200 chars before/after
    section_id: Optional[str] = None  # Which section it appeared in

    # Placement recommendation
    suggested_action: str = "keep_inline"  # "keep_inline" | "move_to_end" | "group_with_figures"
    move_reason: Optional[str] = None      # Why suggest moving (if applicable)

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            'id': self.id,
            'figure_number': self.figure_number,
            'caption_text': self.caption_text,
            'raw_caption': self.raw_caption,
            'page_number': self.page_number,
            'image_bbox': self.image_bbox,
            'image_index': self.image_index,
            'caption_bbox': self.caption_bbox,
            'placement_type': self.placement_type,
            'markdown_position': self.markdown_position,
            'surrounding_context': self.surrounding_context,
            'section_id': self.section_id,
            'suggested_action': self.suggested_action,
            'move_reason': self.move_reason
        }
