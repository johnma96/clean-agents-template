"""Shared test fixtures — mock Protocol implementations and sample data.

All mocks here implement the domain Protocols structurally (duck typing).
They do NOT inherit from the Protocols — they just implement the same methods.
This keeps tests fully decoupled from any infrastructure implementation.

Usage:
    def test_something(mock_llm, mock_vector_store, mock_memory):
        # All three are injected via pytest fixtures defined below.
        ...
"""

from typing import AsyncIterator

import pytest

from {{ cookiecutter.project_slug }}.domain.models import AgentInput, AgentOutput, Document, Message


# ── Mock Protocol implementations ────────────────────────────────────────────

class MockLLMProvider:
    """Mock LLM provider — implements LLMProvider Protocol.

    Returns a fixed response by default. Tracks all calls for assertions.

    Args:
        response: The string to return from generate() and stream().
    """

    def __init__(self, response: str = "This is a mock LLM response.") -> None:
        self.response = response
        self.calls: list[list[Message]] = []

    async def generate(self, messages: list[Message]) -> str:
        """Record the call and return the fixed response.

        Args:
            messages: Messages passed by the agent (recorded for assertions).

        Returns:
            The fixed response string.
        """
        self.calls.append(messages)
        return self.response

    async def stream(self, messages: list[Message]) -> AsyncIterator[str]:
        """Record the call and yield words from the fixed response.

        Args:
            messages: Messages passed by the agent (recorded for assertions).

        Yields:
            Individual words from the fixed response.
        """
        self.calls.append(messages)
        for word in self.response.split():
            yield word + " "


class MockVectorStore:
    """Mock vector store — implements VectorStore Protocol.

    Returns a fixed list of documents from search(). Tracks upserted documents.

    Args:
        documents: Documents to return from search().
    """

    def __init__(self, documents: list[Document] | None = None) -> None:
        self.documents = documents or []
        self.upserted: list[Document] = []

    async def search(self, query: str, k: int) -> list[Document]:
        """Return the first k documents from the fixed list.

        Args:
            query: Ignored in the mock.
            k: Maximum number of documents to return.

        Returns:
            Up to k documents from the fixed list.
        """
        return self.documents[:k]

    async def upsert(self, documents: list[Document]) -> None:
        """Record upserted documents for later assertions.

        Args:
            documents: Documents to record.
        """
        self.upserted.extend(documents)


class MockMemoryStore:
    """Mock memory store — implements MemoryStore Protocol.

    Uses an in-memory dict. Useful for testing multi-turn conversations.
    """

    def __init__(self) -> None:
        self._sessions: dict[str, list[Message]] = {}

    async def get(self, session_id: str) -> list[Message]:
        """Retrieve conversation history for a session.

        Args:
            session_id: Unique identifier for the conversation session.

        Returns:
            Ordered list of messages. Empty list if no history.
        """
        return list(self._sessions.get(session_id, []))

    async def append(self, session_id: str, message: Message) -> None:
        """Append a message to a session's history.

        Args:
            session_id: Unique identifier for the conversation session.
            message: The message to append.
        """
        self._sessions.setdefault(session_id, []).append(message)

    async def clear(self, session_id: str) -> None:
        """Delete the conversation history for a session.

        Args:
            session_id: Unique identifier for the conversation session.
        """
        self._sessions.pop(session_id, None)


# ── Sample data fixtures ──────────────────────────────────────────────────────

@pytest.fixture
def sample_documents() -> list[Document]:
    """A small set of documents for retrieval tests."""
    return [
        Document(doc_id="doc_1", text="First sample document for testing.", score=0.95),
        Document(doc_id="doc_2", text="Second sample document for testing.", score=0.82),
        Document(doc_id="doc_3", text="Third sample document for testing.", score=0.74),
    ]


@pytest.fixture
def sample_messages() -> list[Message]:
    """A short conversation history for memory tests."""
    return [
        Message(role="user", content="Hello, what can you do?"),
        Message(role="assistant", content="I can answer questions using context."),
    ]


@pytest.fixture
def sample_agent_input() -> AgentInput:
    """A minimal AgentInput for agent tests."""
    return AgentInput(query="What is the main topic?", session_id="test-session")


# ── Mock fixtures ─────────────────────────────────────────────────────────────

@pytest.fixture
def mock_llm() -> MockLLMProvider:
    """Return a fresh MockLLMProvider for each test."""
    return MockLLMProvider()


@pytest.fixture
def mock_vector_store(sample_documents: list[Document]) -> MockVectorStore:
    """Return a MockVectorStore pre-loaded with sample_documents."""
    return MockVectorStore(documents=sample_documents)


@pytest.fixture
def mock_memory() -> MockMemoryStore:
    """Return a fresh MockMemoryStore for each test."""
    return MockMemoryStore()
