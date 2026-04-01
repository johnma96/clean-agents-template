"""Vector store implementation — semantic document retrieval.

Implement the VectorStore Protocol defined in::

    domain/interfaces.py → class VectorStore(Protocol)

Required methods:
    async def search(self, query: str, k: int) -> list[Document]
    async def upsert(self, documents: list[Document]) -> None

Conventions:
    - All connection config comes from config.py (Settings).
    - The implementation handles embedding internally (the application layer
      passes raw text, not vectors).
    - Catch storage-specific exceptions and re-raise as domain exceptions::

        from {{ cookiecutter.project_slug }}.domain.exceptions import RetrievalError, IngestionError

        try:
            results = await self._client.query(...)
        except SomeStoreError as exc:
            raise RetrievalError("Vector search failed") from exc

    - When you pick your backend, rename this file for clarity:
        chroma_store.py, pinecone_store.py, qdrant_store.py, pgvector_store.py

Examples of backends you could implement:
    - Chroma (pip install chromadb) — good for local dev, zero infra
    - Pinecone (pip install pinecone) — managed, serverless option
    - Qdrant (pip install qdrant-client) — self-hosted or cloud
    - pgvector via asyncpg — if you already use PostgreSQL
    - Vertex AI Search (pip install google-cloud-aiplatform) — GCP native
    - OpenSearch (pip install opensearch-py) — AWS or self-hosted

Embedding models to consider:
    - sentence-transformers (local, pip install sentence-transformers)
    - text-embedding-004 (Vertex AI)
    - text-embedding-3-small (OpenAI)
    - any model served via Ollama
"""

from {{ cookiecutter.project_slug }}.config import settings
from {{ cookiecutter.project_slug }}.domain.models import Document

# TODO: Install your chosen vector store SDK and import it here.
# TODO: Install your chosen embedding library and import it here.


class VectorStore:
    """Concrete implementation of the VectorStore Protocol.

    Replace the body of search() and upsert() with calls to your
    chosen backend. The interface contract is in domain/interfaces.py.

    Args:
        collection: Name of the collection / index to use.
    """

    def __init__(self, collection: str = "default") -> None:
        self.collection = collection
        # TODO: Initialize your SDK client and embedding model here.
        # Example (Chroma):
        #   import chromadb
        #   self._client = chromadb.AsyncHttpClient(host=settings.vector_store_url)
        #   self._collection = ...

    async def search(self, query: str, k: int) -> list[Document]:
        """Search for the top-k most similar documents.

        Args:
            query: The search string (embedded by this implementation).
            k: Number of results to return.

        Returns:
            List of documents sorted by descending relevance score.

        Raises:
            RetrievalError: If the search operation fails.
        """
        # TODO: Embed the query and call your vector store's search API.
        # Example (Chroma):
        #   embedding = self._embed(query)
        #   results = await self._collection.query(
        #       query_embeddings=[embedding], n_results=k
        #   )
        #   return [
        #       Document(doc_id=id_, text=text, score=score)
        #       for id_, text, score in zip(
        #           results["ids"][0],
        #           results["documents"][0],
        #           results["distances"][0],
        #       )
        #   ]
        raise NotImplementedError("Implement search() with your chosen vector store.")

    async def upsert(self, documents: list[Document]) -> None:
        """Insert or update documents in the store.

        Args:
            documents: Documents to index. Embedding is handled here.

        Raises:
            IngestionError: If the upsert operation fails.
        """
        # TODO: Embed all documents and upsert into your vector store.
        # Example (Chroma):
        #   embeddings = [self._embed(d.text) for d in documents]
        #   await self._collection.upsert(
        #       ids=[d.doc_id for d in documents],
        #       embeddings=embeddings,
        #       documents=[d.text for d in documents],
        #       metadatas=[d.metadata for d in documents],
        #   )
        raise NotImplementedError("Implement upsert() with your chosen vector store.")
