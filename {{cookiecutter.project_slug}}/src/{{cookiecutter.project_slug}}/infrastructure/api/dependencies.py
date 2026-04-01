"""Dependency injection — wires infrastructure implementations to application layer.

This is the single place where concrete infrastructure classes are instantiated
and injected into agents and services. The application layer never instantiates
infrastructure directly — it only receives injected dependencies.

This file is framework-agnostic. The examples below use FastAPI's dependency
injection system, but the same pattern works with any DI container or manual
wiring.

Rules:
    - This is the ONLY place in infrastructure/ where concrete classes are
      instantiated and wired together.
    - Return type hints should use the Protocol types from domain/interfaces.py,
      not the concrete implementation types.
    - Use module-level singletons (created once at startup) for expensive
      resources like SDK clients. Use per-request factories for lightweight deps.

Example (FastAPI):
    @router.post("/ask")
    async def ask(
        request: AskRequest,
        llm: LLMProvider = Depends(get_llm),
        store: VectorStore = Depends(get_vector_store),
    ) -> AskResponse:
        ...
"""

from {{ cookiecutter.project_slug }}.domain.interfaces import LLMProvider, MemoryStore, VectorStore
from {{ cookiecutter.project_slug }}.infrastructure.llm.llm_provider import LLMProvider as LLMProviderImpl
from {{ cookiecutter.project_slug }}.infrastructure.memory.memory_store import InMemoryStore
from {{ cookiecutter.project_slug }}.infrastructure.retrieval.vector_store import VectorStore as VectorStoreImpl

# ── Singletons — created once at application startup ─────────────────────────
# These are expensive to construct (SDK clients, connection pools, etc.)
# and should be shared across all requests.

_llm_instance: LLMProvider | None = None
_store_instance: VectorStore | None = None
_memory_instance: MemoryStore | None = None


def get_llm() -> LLMProvider:
    """Return the shared LLMProvider instance.

    Returns:
        The application-wide LLMProvider (lazy-initialized on first call).
    """
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = LLMProviderImpl()
    return _llm_instance


def get_vector_store() -> VectorStore:
    """Return the shared VectorStore instance.

    Returns:
        The application-wide VectorStore (lazy-initialized on first call).
    """
    global _store_instance
    if _store_instance is None:
        _store_instance = VectorStoreImpl()
    return _store_instance


def get_memory() -> MemoryStore:
    """Return the shared MemoryStore instance.

    Returns:
        The application-wide MemoryStore (lazy-initialized on first call).
    """
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = InMemoryStore()
    return _memory_instance


# TODO: Add dependency factories for other infrastructure components.
# TODO: Replace InMemoryStore with a persistent implementation for production.
