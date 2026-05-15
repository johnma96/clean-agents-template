"""Centralized configuration — single source of truth for all settings.

All settings are loaded from environment variables and/or a .env file.
No other file in the project should read from the environment directly.

Usage:
    from {{ cookiecutter.project_slug }}.config import settings

    client = SomeSDK(api_key=settings.llm_api_key)

Conventions:
    - Add a new field here for every new environment variable.
    - Use Literal types to constrain choices (e.g., Literal["dev", "prod"]).
    - Never hardcode secrets or environment-specific values outside this file.
    - Group fields by component with comment sections for readability.

Reference:
    Pydantic Settings docs: https://docs.pydantic.dev/latest/concepts/pydantic_settings/
"""

from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

from {{ cookiecutter.project_slug }}.paths import PROJECT_ROOT


class Settings(BaseSettings):
    """Application settings loaded from .env and environment variables.

    Priority (highest to lowest):
        1. Environment variables
        2. .env file values
        3. Default values defined here

    To add a new setting:
        1. Add a field with its type and a default value (or no default if required).
        2. Add the corresponding variable to .env.example.
        3. Document the expected values in the field's description.
    """

    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # Ignore unknown env vars instead of raising
    )

    # ── Environment ───────────────────────────────────────────────────────────
    environment: Literal["development", "staging", "production"] = "development"

    # ── LLM provider ─────────────────────────────────────────────────────────
    # Replace or extend these fields once you choose your LLM provider.
    # Examples: anthropic_api_key, openai_api_key, google_cloud_project, etc.
    llm_api_key: str = ""
    llm_model: str = ""  # e.g. "claude-sonnet-4-6", "gemini-2.0-flash", "gpt-4o"

    # ── Vector store ──────────────────────────────────────────────────────────
    # Configure the connection to your vector store of choice.
    # Examples: chroma_persist_dir, pinecone_api_key, qdrant_url, etc.
    vector_store_url: str = ""

    # ── Memory / session store ────────────────────────────────────────────────
    # Configure persistence for conversational memory.
    # Examples: redis_url, firestore_collection, sqlite_db_path, etc.
    memory_store_url: str = ""

    # ── Embeddings ────────────────────────────────────────────────────────────
    embedding_model: str = ""  # e.g. "all-MiniLM-L6-v2", "text-embedding-004"

    # ── API server (if include_api = "yes") ───────────────────────────────────
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # ── Monitoring (if include_monitoring = "yes") ────────────────────────────
    # Configure your observability/tracing backend.
    # Examples: langfuse_public_key, langsmith_api_key, etc.
    tracing_enabled: bool = False
    tracing_api_key: str = ""

    # ── Add your project-specific settings below ──────────────────────────────
    # TODO: Add the settings your project needs, grouped by component.


settings = Settings()
