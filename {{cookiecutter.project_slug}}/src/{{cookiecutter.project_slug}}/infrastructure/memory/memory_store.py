"""Memory store implementation — conversational history persistence.

Implement the MemoryStore Protocol defined in::

    domain/interfaces.py → class MemoryStore(Protocol)

Required methods:
    async def get(self, session_id: str) -> list[Message]
    async def append(self, session_id: str, message: Message) -> None
    async def clear(self, session_id: str) -> None

Conventions:
    - All connection config comes from config.py (Settings).
    - Catch storage-specific exceptions and re-raise as domain exceptions::

        from {{ cookiecutter.project_slug }}.domain.exceptions import MemoryError

        try:
            await self._client.set(key, value)
        except SomeStorageError as exc:
            raise MemoryError("Failed to write session history") from exc

    - Session IDs are opaque strings. The store does not interpret them.
    - When you pick your backend, rename this file for clarity:
        redis_store.py, firestore_store.py, sqlite_store.py, postgres_store.py

Examples of backends you could implement:
    - In-memory dict (zero deps, perfect for tests and local dev)
    - Redis (pip install redis)
    - Firestore (pip install google-cloud-firestore)
    - PostgreSQL via asyncpg (pip install asyncpg)
    - SQLite via aiosqlite (pip install aiosqlite)

A recommended approach: start with InMemoryStore for development and testing,
then add a persistent implementation (Redis, Firestore, etc.) for production.
"""

from {{ cookiecutter.project_slug }}.domain.models import Message


class InMemoryStore:
    """In-memory MemoryStore — for local development and unit tests.

    Stores conversation history in a plain dict. Data is lost on restart.
    Use this during development and replace with a persistent store for production.
    """

    def __init__(self) -> None:
        self._sessions: dict[str, list[Message]] = {}

    async def get(self, session_id: str) -> list[Message]:
        """Retrieve conversation history for a session.

        Args:
            session_id: Unique identifier for the conversation session.

        Returns:
            Ordered list of messages (oldest first). Empty list if no history.
        """
        return list(self._sessions.get(session_id, []))

    async def append(self, session_id: str, message: Message) -> None:
        """Append a message to a session's history.

        Args:
            session_id: Unique identifier for the conversation session.
            message: The message to append.
        """
        if session_id not in self._sessions:
            self._sessions[session_id] = []
        self._sessions[session_id].append(message)

    async def clear(self, session_id: str) -> None:
        """Delete the conversation history for a session.

        Args:
            session_id: Unique identifier for the conversation session.
        """
        self._sessions.pop(session_id, None)


# TODO: Add a persistent MemoryStore implementation for production.
# When ready, register it in infrastructure/api/dependencies.py.
