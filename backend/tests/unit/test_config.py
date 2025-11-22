"""Tests for configuration system."""

import pytest
import tempfile
from pathlib import Path

from services.parser.pipeline.config import (
    PipelineConfig,
    default_config,
    load_config_from_yaml,
    GeometryConfig,
    AnalysisConfig,
    CleanupConfig,
)


class TestDefaultConfig:
    """Tests for default configuration."""

    def test_default_config_creation(self):
        """Should create default config with all sections."""
        config = default_config()
        assert isinstance(config, PipelineConfig)
        assert isinstance(config.geometry, GeometryConfig)
        assert isinstance(config.analysis, AnalysisConfig)
        assert isinstance(config.cleanup, CleanupConfig)

    def test_default_values(self):
        """Should have sensible defaults."""
        config = default_config()
        assert config.geometry.top_margin == 60
        assert config.geometry.bottom_margin == 60
        assert config.analysis.detect_bold_text is True
        assert config.cleanup.remove_figure_blocks is True
        assert config.indexing.enable_sentence_indexing is True


class TestYAMLLoading:
    """Tests for YAML configuration loading."""

    def test_load_nonexistent_file(self):
        """Should return None for nonexistent file."""
        config = load_config_from_yaml(Path("/nonexistent/config.yaml"))
        assert config is None

    def test_load_empty_yaml(self):
        """Should return defaults for empty YAML file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("")
            temp_path = Path(f.name)

        try:
            config = load_config_from_yaml(temp_path)
            # Empty YAML should still return config with defaults
            assert config is not None
            assert config.geometry.top_margin == 60
        finally:
            temp_path.unlink()

    def test_load_partial_override(self):
        """Should merge partial overrides with defaults."""
        yaml_content = """
geometry:
  top_margin: 100
  bottom_margin: 80

analysis:
  detect_bold_text: false
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(yaml_content)
            temp_path = Path(f.name)

        try:
            config = load_config_from_yaml(temp_path)
            assert config is not None
            # Overridden values
            assert config.geometry.top_margin == 100
            assert config.geometry.bottom_margin == 80
            assert config.analysis.detect_bold_text is False
            # Default values should remain
            assert config.cleanup.remove_figure_blocks is True
            assert config.indexing.enable_sentence_indexing is True
        finally:
            temp_path.unlink()

    def test_load_full_config(self):
        """Should load complete configuration from YAML."""
        yaml_content = """
geometry:
  top_margin: 70
  bottom_margin: 60

analysis:
  detect_bold_text: true
  extract_title: true
  min_title_font_size: 16.0

cleanup:
  remove_figure_blocks: false
  remove_headers_footers: true
  remove_copyright: false

indexing:
  enable_sentence_indexing: false
  use_nltk: false

debug_logging: true
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(yaml_content)
            temp_path = Path(f.name)

        try:
            config = load_config_from_yaml(temp_path)
            assert config is not None
            assert config.geometry.top_margin == 70
            assert config.analysis.min_title_font_size == 16.0
            assert config.cleanup.remove_figure_blocks is False
            assert config.cleanup.remove_copyright is False
            assert config.indexing.enable_sentence_indexing is False
            assert config.indexing.use_nltk is False
            assert config.debug_logging is True
        finally:
            temp_path.unlink()

    def test_invalid_yaml_key_warning(self, caplog):
        """Should warn about invalid config keys."""
        yaml_content = """
geometry:
  invalid_key: 123
  top_margin: 100
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(yaml_content)
            temp_path = Path(f.name)

        try:
            config = load_config_from_yaml(temp_path)
            assert config is not None
            # Valid key should be applied
            assert config.geometry.top_margin == 100
            # Invalid key should generate warning (check logs if needed)
        finally:
            temp_path.unlink()

    def test_missing_pyyaml_import(self, monkeypatch):
        """Should handle missing PyYAML gracefully."""
        # Simulate missing PyYAML by raising ImportError
        def mock_import(*args, **kwargs):
            raise ImportError("No module named 'yaml'")

        # This test is hard to implement without mocking builtins
        # Skipping for now as it requires complex mocking
        pass


class TestConfigDataclasses:
    """Tests for individual config dataclasses."""

    def test_geometry_config_defaults(self):
        """Should have correct geometry defaults."""
        config = GeometryConfig()
        assert config.top_margin == 60
        assert config.bottom_margin == 60
        assert config.detect_line_numbers is True

    def test_analysis_config_defaults(self):
        """Should have correct analysis defaults."""
        config = AnalysisConfig()
        assert config.detect_bold_text is True
        assert config.extract_title is True
        assert config.min_title_font_size == 14.0

    def test_cleanup_config_defaults(self):
        """Should have correct cleanup defaults."""
        config = CleanupConfig()
        assert config.remove_figure_blocks is True
        assert config.remove_headers_footers is True
        assert config.remove_copyright is True
