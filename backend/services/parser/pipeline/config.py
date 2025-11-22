"""Configuration system for PDF parsing pipeline.

Provides dataclasses for each stage configuration with sensible defaults.
Supports optional YAML override loading.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


@dataclass
class GeometryConfig:
    """Configuration for geometric cleaning stage."""
    top_margin: int = 60  # Points to crop from top
    bottom_margin: int = 60  # Points to crop from bottom
    detect_line_numbers: bool = True
    detect_columns: bool = False  # Future feature


@dataclass
class AnalysisConfig:
    """Configuration for structure analysis stage."""
    detect_bold_text: bool = True
    extract_title: bool = True
    extract_abstract_fallback: bool = True
    min_title_font_size: float = 14.0
    title_position_threshold: float = 0.3  # Top 30% of first page


@dataclass
class ReflowConfig:
    """Configuration for text reflow stage."""
    enable_reflow: bool = True
    merge_hyphenations: bool = True
    min_line_length: int = 40  # Minimum chars to not merge


@dataclass
class CleanupConfig:
    """Configuration for artifact cleanup stage."""
    remove_figure_blocks: bool = True
    remove_headers_footers: bool = True
    remove_affiliations: bool = True
    remove_page_numbers: bool = True
    remove_copyright: bool = True
    remove_doi_blocks: bool = True
    # Add more cleanup options as needed


@dataclass
class SectionConfig:
    """Configuration for section formatting and validation."""

    # Section priority ordering (lower = earlier in document)
    section_order: Dict[str, int] = field(default_factory=lambda: {
        'abstract': 1,
        'keywords': 2,
        'introduction': 10,
        'background': 11,
        'related_work': 12,
        'methods': 20,
        'materials_and_methods': 20,
        'experimental': 21,
        'results': 30,
        'discussion': 40,
        'conclusion': 50,
        'conclusions': 50,
        'acknowledgments': 60,
        'acknowledgements': 60,
        'author_contributions': 61,
        'funding': 62,
        'competing_interests': 63,
        'data_availability': 64,
        'references': 70,
        'bibliography': 70,
    })

    # Standard section names for detection
    standard_sections: List[str] = field(default_factory=lambda: [
        'abstract', 'introduction', 'background', 'related work',
        'methods', 'materials and methods', 'experimental', 'methodology',
        'results', 'discussion', 'results and discussion',
        'conclusion', 'conclusions', 'summary',
        'references', 'bibliography', 'acknowledgments', 'acknowledgements'
    ])

    # Required section groups (at least one from each group must exist)
    required_groups: Dict[str, List[str]] = field(default_factory=lambda: {
        'introduction': ['introduction'],
        'methods': ['methods', 'materials_and_methods', 'experimental',
                    'methodology', 'materials and methods'],
        'results': ['results'],
        'discussion': ['discussion', 'conclusions', 'results_and_discussion', 'conclusion']
    })

    # Whether to detect unlabeled sections by keyword analysis
    detect_by_keywords: bool = True

    # Whether to move administrative sections (refs, acknowledgements) to end
    reorder_admin_sections: bool = True


@dataclass
class IndexingConfig:
    """Configuration for sentence indexing stage."""
    enable_sentence_indexing: bool = True
    use_nltk: bool = True
    # Language for NLTK tokenization
    language: str = 'english'


@dataclass
class ExtractionConfig:
    """Configuration for metadata extraction."""
    extract_citations: bool = True
    extract_figures: bool = True
    extract_bibliography: bool = True
    parse_doi_from_bibliography: bool = True


@dataclass
class PipelineConfig:
    """Complete pipeline configuration."""
    geometry: GeometryConfig = field(default_factory=GeometryConfig)
    analysis: AnalysisConfig = field(default_factory=AnalysisConfig)
    reflow: ReflowConfig = field(default_factory=ReflowConfig)
    cleanup: CleanupConfig = field(default_factory=CleanupConfig)
    sections: SectionConfig = field(default_factory=SectionConfig)
    indexing: IndexingConfig = field(default_factory=IndexingConfig)
    extraction: ExtractionConfig = field(default_factory=ExtractionConfig)

    # Global options
    debug_logging: bool = False


def default_config() -> PipelineConfig:
    """Get default pipeline configuration."""
    return PipelineConfig()


def load_config_from_yaml(yaml_path: Path) -> Optional[PipelineConfig]:
    """Load configuration from YAML file, merge with defaults.

    Args:
        yaml_path: Path to YAML configuration file

    Returns:
        PipelineConfig with overrides from YAML, or None if file doesn't exist
    """
    if not yaml_path.exists():
        logger.info(f"No config file found at {yaml_path}, using defaults")
        return None

    try:
        import yaml
        with open(yaml_path, 'r') as f:
            config_dict = yaml.safe_load(f)

        # Start with defaults
        config = default_config()

        # Deep merge YAML overrides into default config
        if config_dict:
            _deep_merge_config(config, config_dict)

        logger.info(f"Loaded configuration from {yaml_path}")
        return config

    except ImportError:
        logger.warning("PyYAML not installed, cannot load YAML config. Install with: pip install pyyaml")
        return None
    except Exception as e:
        logger.error(f"Error loading config from {yaml_path}: {e}")
        return None


def _deep_merge_config(config: PipelineConfig, yaml_dict: dict) -> None:
    """Deep merge YAML dictionary into config object.

    Args:
        config: Config object to update
        yaml_dict: Dictionary from YAML file
    """
    # Map of section names to config attributes
    section_map = {
        'geometry': config.geometry,
        'analysis': config.analysis,
        'reflow': config.reflow,
        'cleanup': config.cleanup,
        'sections': config.sections,
        'indexing': config.indexing,
        'extraction': config.extraction,
    }

    # Update each section
    for section_name, section_config in section_map.items():
        if section_name in yaml_dict:
            section_dict = yaml_dict[section_name]
            for key, value in section_dict.items():
                if hasattr(section_config, key):
                    setattr(section_config, key, value)
                else:
                    logger.warning(f"Unknown config key: {section_name}.{key}")

    # Update global options
    if 'debug_logging' in yaml_dict:
        config.debug_logging = yaml_dict['debug_logging']


def merge_configs(base: PipelineConfig, override: Optional[PipelineConfig]) -> PipelineConfig:
    """Merge two configurations, with override taking precedence.

    Args:
        base: Base configuration
        override: Override configuration (optional)

    Returns:
        Merged configuration
    """
    if override is None:
        return base

    # For now, just return override if it exists
    # TODO: Implement proper deep merge
    return override
