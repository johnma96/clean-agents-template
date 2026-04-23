"""Unit tests for domain models."""

import pytest

from {{ cookiecutter.project_slug }}.domain.exceptions import (
    ConfigurationError,
    GenerationError,
    IngestionError,
    PromptNotFoundError,
    ProviderError,
    RateLimitError,
    RetrievalError,
    {{ cookiecutter.project_slug | title | replace('_', '') }}Error,
)
from {{ cookiecutter.project_slug }}.domain.models import AgentInput, AgentOutput, Document, Message


@pytest.mark.unit
class TestMessageModel:
    def test_message_creation(self) -> None:
        msg = Message(role="user", content="Hello")
        assert msg.role == "user"
        assert msg.content == "Hello"


@pytest.mark.unit
class TestDocumentModel:
    def test_document_defaults(self) -> None:
        doc = Document(doc_id="1", text="Some text")
        assert doc.score == 0.0
        assert doc.metadata == {}

    def test_document_with_score(self) -> None:
        doc = Document(doc_id="1", text="Some text", score=0.95)
        assert doc.score == 0.95


@pytest.mark.unit
class TestAgentInput:
    def test_default_session_id(self) -> None:
        inp = AgentInput(query="What is this?")
        assert inp.session_id == "default"

    def test_custom_session_id(self) -> None:
        inp = AgentInput(query="What is this?", session_id="abc-123")
        assert inp.session_id == "abc-123"


@pytest.mark.unit
class TestAgentOutput:
    def test_output_defaults(self) -> None:
        out = AgentOutput(answer="Some answer")
        assert out.sources == []
        assert out.metadata == {}


@pytest.mark.unit
class TestExceptions:
    def test_all_exceptions_inherit_from_base(self) -> None:
        base = {{ cookiecutter.project_slug | title | replace('_', '') }}Error
        assert issubclass(ConfigurationError, base)
        assert issubclass(ProviderError, base)
        assert issubclass(GenerationError, base)
        assert issubclass(RetrievalError, base)
        assert issubclass(IngestionError, base)
        assert issubclass(PromptNotFoundError, base)
        assert issubclass(RateLimitError, base)

    def test_exception_can_be_raised_and_caught(self) -> None:
        with pytest.raises({{ cookiecutter.project_slug | title | replace('_', '') }}Error):
            raise GenerationError("LLM failed")
