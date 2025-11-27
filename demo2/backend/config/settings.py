"""
Configuration settings for the backend
"""

from pydantic import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # API Configuration
    api_title: str = "PeerPreview API"
    api_version: str = "0.1.0"
    debug_mode: bool = True

    # Claude API Configuration
    claude_api_key: Optional[str] = os.getenv("CLAUDE_API_KEY")
    claude_model_sonnet: str = "claude-3-sonnet-20240229"  # For review agents
    claude_model_haiku: str = "claude-3-haiku-20240307"   # For classification

    # Agent Configuration
    max_retries: int = 3
    agent_timeout: int = 300  # seconds

    # Review Configuration
    max_document_pages: int = 100
    max_document_words: int = 50000

    class Config:
        env_file = ".env"

settings = Settings()