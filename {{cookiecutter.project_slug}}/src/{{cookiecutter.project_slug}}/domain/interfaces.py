"""Domain interfaces — Protocols (contracts) that infrastructure must implement.

This file defines WHAT each external component must be able to do,
without specifying HOW it does it. Concrete implementations live in
infrastructure/ and are injected at runtime.

Rules:
    - Only stdlib, Pydantic, and other domain/ modules are allowed here.
    - NEVER import from application/ or infrastructure/.
    - Each Protocol must have a docstring explaining its responsibility.
    - Use @runtime_checkable to enable isinstance() checks in tests.

Why Protocols instead of ABCs?
    Protocols enable structural subtyping (duck typing with type safety).
    Infrastructure classes do not need to explicitly inherit from the Protocol —
    they just need to implement the required methods. This makes swapping
    implementations trivial and keeps infrastructure/ decoupled from domain/.

Example:
    Usage in application layer — program against the Protocol, not the implementation::

        from {{ cookiecutter.project_slug }}.domain.interfaces import LLMProvider

        async def run_agent(query: str, llm: LLMProvider) -> str:
            messages = [Message(role="user", content=query)]
            return await llm.generate(messages)

    Usage in tests — implement the Protocol with a mock, no infrastructure imports::

        class MockLLMProvider:
            async def generate(self, messages: list[Message]) -> str:
                return "mocked response"
            async def stream(self, messages: list[Message]) -> AsyncIterator[str]:
                yield "mocked"

Reference:
    PEP 544 — Protocols: https://peps.python.org/pep-0544/
"""

from typing import AsyncIterator, Protocol, runtime_checkable

from .models import Document, Message


@runtime_checkable
class LLMProvider(Protocol):
    """Contract for any large language model provider.

    Implementations belong in infrastructure/llm/.
    Possible implementations: Claude (Anthropic), Gemini (Vertex AI),
    GPT-4 (OpenAI), any OpenAI-compatible endpoint, Ollama (local), etc.
    """

    async def generate(self, messages: list[Message]) -> str:
        """Generate a complete response from a list of messages.

        Args:
            messages: Conversation history including the current user message.

        Returns:
            The model's response as a plain string.

        Raises:
            GenerationError: If the provider fails or returns an invalid response.
            RateLimitError: If the provider's rate limit is exceeded.
        """
        ...

    async def stream(self, messages: list[Message]) -> AsyncIterator[str]:
        """Stream a response token by token.

        Args:
            messages: Conversation history including the current user message.

        Yields:
            Individual tokens or chunks as they are generated.

        Raises:
            GenerationError: If the stream fails mid-way.
        """
        ...


@runtime_checkable
class VectorStore(Protocol):
    """Contract for any vector similarity store.

    Implementations belong in infrastructure/retrieval/.
    Possible implementations: Chroma, Pinecone, Qdrant, pgvector,
    Vertex AI Search, OpenSearch, Weaviate, etc.
    """

    async def search(self, query: str, k: int) -> list[Document]:
        """Find the top-k most semantically similar documents to a query.

        Args:
            query: The search string (embedded by the implementation).
            k: Number of results to return.

        Returns:
            List of documents sorted by descending relevance score.

        Raises:
            RetrievalError: If the search operation fails.
        """
        ...

    async def upsert(self, documents: list[Document]) -> None:
        """Insert or update documents in the store.

        If a document with the same doc_id already exists, it is replaced.

        Args:
            documents: Documents to index. The implementation handles embedding.

        Raises:
            IngestionError: If the upsert operation fails.
        """
        ...


@runtime_checkable
class MemoryStore(Protocol):
    """Contract for conversational memory persistence.

    Implementations belong in infrastructure/memory/.
    Possible implementations: Redis, Firestore, PostgreSQL, DynamoDB,
    SQLite (local dev), in-memory dict (tests), etc.
    """

    async def get(self, session_id: str) -> list[Message]:
        """Retrieve the full conversation history for a session.

        Args:
            session_id: Unique identifier for the conversation session.

        Returns:
            Ordered list of messages (oldest first). Empty list if no history.

        Raises:
            MemoryError: If the read operation fails.
        """
        ...

    async def append(self, session_id: str, message: Message) -> None:
        """Append a single message to a session's history.

        Args:
            session_id: Unique identifier for the conversation session.
            message: The message to append.

        Raises:
            MemoryError: If the write operation fails.
        """
        ...

    async def clear(self, session_id: str) -> None:
        """Delete the conversation history for a session.

        Args:
            session_id: Unique identifier for the conversation session.

        Raises:
            MemoryError: If the delete operation fails.
        """
        ...


# TODO: Add Protocols for other external components your project needs.
# Examples:
#
#   class DataSource(Protocol):
#       """Contract for corporate data access (databases, data warehouses, etc.)."""
#       async def fetch(self, query: str) -> list[dict]: ...
#
#   class NotificationSender(Protocol):
#       """Contract for sending notifications (email, Slack, Telegram, etc.)."""
#       async def send(self, recipient: str, message: str) -> None: ...
#
#   class MCPClient(Protocol):
#       """Contract for MCP server connections."""
#       async def call_tool(self, tool_name: str, args: dict) -> dict: ...
