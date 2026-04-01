"""Integration tests for the HTTP API layer.

These tests hit the real API endpoints (no mocks for the HTTP layer).
Infrastructure dependencies (LLM, vector store) may be mocked or real
depending on your CI setup.

Conventions:
    - Mark with @pytest.mark.integration so they can be excluded from fast runs.
    - Use a test client provided by your HTTP framework (e.g., FastAPI TestClient).
    - Do NOT make real LLM API calls in CI — use MockLLMProvider instead.

To run only integration tests:
    uv run pytest -v -m integration
"""

import pytest

# TODO: Uncomment and implement once infrastructure/api/main.py is set up.
#
# from fastapi.testclient import TestClient
# from {{ cookiecutter.project_slug }}.infrastructure.api.main import app
# from {{ cookiecutter.project_slug }}.infrastructure.api.dependencies import get_llm, get_vector_store
# from tests.conftest import MockLLMProvider, MockVectorStore
#
#
# @pytest.fixture
# def client(mock_llm, mock_vector_store):
#     app.dependency_overrides[get_llm] = lambda: mock_llm
#     app.dependency_overrides[get_vector_store] = lambda: mock_vector_store
#     with TestClient(app) as c:
#         yield c
#     app.dependency_overrides.clear()
#
#
# @pytest.mark.integration
# class TestHealthEndpoint:
#     def test_health_returns_200(self, client):
#         response = client.get("/health/")
#         assert response.status_code == 200
#         assert response.json()["status"] == "ok"
#
#
# @pytest.mark.integration
# class TestAgentEndpoint:
#     def test_ask_returns_answer(self, client):
#         response = client.post("/agent/ask", json={"question": "What is this?"})
#         assert response.status_code == 200
#         assert "answer" in response.json()
