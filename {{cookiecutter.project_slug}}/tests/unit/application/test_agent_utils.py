"""Unit tests for agent_utils — uses mock Protocol implementations, no IO."""

import pytest

from {{ cookiecutter.project_slug }}.application.agents.agent_utils import (
    build_rag_messages,
    retrieve_and_generate,
    retrieve_context,
    wrap_output,
)
from {{ cookiecutter.project_slug }}.domain.models import Document

from tests.conftest import MockLLMProvider, MockVectorStore


@pytest.mark.unit
class TestRetrieveContext:
    @pytest.mark.asyncio
    async def test_returns_documents(self, mock_vector_store: MockVectorStore) -> None:
        docs = await retrieve_context("test query", mock_vector_store, top_k=2)
        assert len(docs) == 2
        assert isinstance(docs[0], Document)

    @pytest.mark.asyncio
    async def test_respects_top_k(self, mock_vector_store: MockVectorStore) -> None:
        docs = await retrieve_context("query", mock_vector_store, top_k=1)
        assert len(docs) == 1


@pytest.mark.unit
class TestBuildRagMessages:
    def test_produces_two_messages(self, sample_documents: list[Document]) -> None:
        messages = build_rag_messages("What is this?", sample_documents, "You are helpful.")
        assert len(messages) == 2

    def test_first_message_is_system(self, sample_documents: list[Document]) -> None:
        messages = build_rag_messages("query", sample_documents, "System prompt here.")
        assert messages[0].role == "system"
        assert "System prompt here." in messages[0].content

    def test_second_message_contains_query(self, sample_documents: list[Document]) -> None:
        messages = build_rag_messages("My question", sample_documents, "System.")
        assert messages[1].role == "user"
        assert "My question" in messages[1].content

    def test_context_includes_all_documents(self, sample_documents: list[Document]) -> None:
        messages = build_rag_messages("query", sample_documents, "System.")
        for doc in sample_documents:
            assert doc.text in messages[1].content


@pytest.mark.unit
class TestRetrieveAndGenerate:
    @pytest.mark.asyncio
    async def test_returns_llm_response(
        self,
        mock_llm: MockLLMProvider,
        mock_vector_store: MockVectorStore,
    ) -> None:
        result = await retrieve_and_generate(
            query="What is this about?",
            llm=mock_llm,
            store=mock_vector_store,
            system_prompt="You are helpful.",
        )
        assert result == mock_llm.response

    @pytest.mark.asyncio
    async def test_llm_is_called_exactly_once(
        self,
        mock_llm: MockLLMProvider,
        mock_vector_store: MockVectorStore,
    ) -> None:
        await retrieve_and_generate("query", mock_llm, mock_vector_store, "System.")
        assert len(mock_llm.calls) == 1


@pytest.mark.unit
class TestWrapOutput:
    def test_wraps_string_into_agent_output(self) -> None:
        output = wrap_output("The answer is 42.")
        assert output.answer == "The answer is 42."
        assert output.sources == []

    def test_includes_sources_when_provided(self, sample_documents: list[Document]) -> None:
        output = wrap_output("Answer", sources=sample_documents)
        assert len(output.sources) == len(sample_documents)
