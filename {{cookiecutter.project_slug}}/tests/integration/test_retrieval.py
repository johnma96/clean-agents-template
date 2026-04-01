"""Integration tests for the retrieval pipeline.

These tests verify that the VectorStore implementation works correctly
against a real (or local) backend.

Conventions:
    - Mark with @pytest.mark.integration.
    - Use a local / ephemeral backend (e.g., Chroma in-memory) so tests
      don't depend on external services in CI.
    - Clean up any data created during the test in a teardown fixture.

To run only integration tests:
    uv run pytest -v -m integration
"""

import pytest

# TODO: Uncomment and implement once infrastructure/retrieval/vector_store.py is set up.
#
# from {{ cookiecutter.project_slug }}.infrastructure.retrieval.vector_store import VectorStore
# from {{ cookiecutter.project_slug }}.domain.models import Document
#
#
# @pytest.fixture
# async def store():
#     # Use an ephemeral local backend for tests.
#     s = VectorStore(collection="test_collection")
#     yield s
#     # Teardown: clean up test data
#
#
# @pytest.mark.integration
# class TestVectorStoreRoundTrip:
#     @pytest.mark.asyncio
#     async def test_upsert_and_search(self, store: VectorStore) -> None:
#         docs = [Document(doc_id="t1", text="Clean architecture for LLM agents")]
#         await store.upsert(docs)
#         results = await store.search("LLM agent architecture", k=1)
#         assert len(results) == 1
#         assert results[0].doc_id == "t1"
