"""Domain exceptions — typed business errors for {{ cookiecutter.project_name }}.

All exceptions in the system should inherit from the base exception defined here.
Infrastructure errors must be caught at the infrastructure boundary and re-raised
as domain exceptions — the application layer should never see SDK-specific errors.

Rules:
    - Only stdlib here. No external dependencies.
    - Map infrastructure errors to domain exceptions in infrastructure/ code:

        # infrastructure/llm/llm_provider.py
        try:
            response = await sdk_client.generate(...)
        except SomeSDKError as exc:
            raise GenerationError("LLM generation failed") from exc

    - Catch domain exceptions in the application layer to handle business logic.
    - Never catch the base {{ cookiecutter.project_slug | upper }}_ERROR broadly —
      be specific to enable precise error handling.

How to add a new exception:
    1. Identify which business operation can fail.
    2. Create a class inheriting from {{ cookiecutter.project_name | replace(' ', '') }}Error.
    3. Document when it is raised in the class docstring.
    4. Raise it from the appropriate layer (never from domain/ itself).
"""


class {{ cookiecutter.project_name | replace(' ', '') }}Error(Exception):
    """Base exception for all {{ cookiecutter.project_name }} errors.

    All other exceptions in this project inherit from this class,
    making it easy to catch all project errors in one place if needed.
    """


class ConfigurationError({{ cookiecutter.project_name | replace(' ', '') }}Error):
    """Raised when a required configuration value is missing or invalid."""


class ProviderError({{ cookiecutter.project_name | replace(' ', '') }}Error):
    """Raised when an external provider (LLM, vector store, etc.) fails.

    Infrastructure code should wrap provider-specific errors into this exception
    before they propagate to the application layer.
    """


class GenerationError({{ cookiecutter.project_name | replace(' ', '') }}Error):
    """Raised when LLM generation fails (API error, timeout, invalid response)."""


class RetrievalError({{ cookiecutter.project_name | replace(' ', '') }}Error):
    """Raised when the retrieval pipeline fails (vector store error, no results)."""


class IngestionError({{ cookiecutter.project_name | replace(' ', '') }}Error):
    """Raised when document ingestion fails (parse error, embedding error, etc.)."""


class MemoryError({{ cookiecutter.project_name | replace(' ', '') }}Error):  # noqa: A001
    """Raised when reading from or writing to the memory store fails."""


class PromptNotFoundError({{ cookiecutter.project_name | replace(' ', '') }}Error):
    """Raised when a prompt template file cannot be found on disk."""


class RateLimitError({{ cookiecutter.project_name | replace(' ', '') }}Error):
    """Raised when an external API rate limit is hit.

    Callers can catch this specifically to implement retry / backoff logic.
    """


# TODO: Add domain-specific exceptions below.
# Example: class DocumentNotFoundError({{ cookiecutter.project_name | replace(' ', '') }}Error): ...
