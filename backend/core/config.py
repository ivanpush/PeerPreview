"""Configuration management using Pydantic settings."""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings with environment variable loading."""

    # API Keys
    claude_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    groq_api_key: Optional[str] = None
    together_api_key: Optional[str] = None
    semantic_scholar_api_key: Optional[str] = None

    # Demo Mode
    demo_mode: bool = True
    demo_paper_hash: str = "abc123def456"

    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5432/peerpreview"
    redis_url: Optional[str] = "redis://localhost:6379"

    # Server
    debug: bool = True
    log_level: str = "INFO"
    cors_origins: list = ["http://localhost:3000", "http://localhost:8000"]

    # File Storage
    upload_dir: str = "uploads"
    fixtures_dir: str = "fixtures"
    prompts_dir: str = "prompts"
    max_file_size: int = 50 * 1024 * 1024  # 50MB

    # Processing
    max_pages: int = 100
    processing_timeout: int = 180  # seconds
    agent_timeout: int = 30  # seconds per agent

    # LLM Settings
    claude_model: str = "claude-3-opus-20240229"
    openai_model: str = "gpt-4-turbo-preview"
    groq_model: str = "mixtral-8x7b-32768"  # Fast for simple checks
    temperature: float = 0.1  # Low for consistency
    max_tokens: int = 4000

    # Cache
    enable_cache: bool = True
    cache_ttl: int = 3600  # 1 hour

    class Config:
        env_file = ".env"
        case_sensitive = False


# Singleton instance
settings = Settings()


# Helper functions
def get_llm_provider(agent_type: str) -> str:
    """Determine which LLM provider to use for a given agent."""
    # Primary reviewers use Claude
    if agent_type in ["methods_reviewer", "results_reviewer", "discussion_reviewer"]:
        return "claude"
    # Style and consistency checks use OpenAI
    elif agent_type in ["cross_doc_consistency", "figure_agent"]:
        return "openai"
    # Fast checks use Groq/mini models
    elif agent_type in ["citation_extractor", "section_splitter"]:
        return "groq"
    # Default to Claude
    return "claude"


def is_demo_paper(doc_hash: str) -> bool:
    """Check if document is the demo paper."""
    return settings.demo_mode and doc_hash == settings.demo_paper_hash