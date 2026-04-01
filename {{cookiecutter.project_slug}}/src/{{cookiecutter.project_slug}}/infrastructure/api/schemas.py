"""API request and response schemas — HTTP boundary models.

These Pydantic models define the shape of the HTTP API contract.
They are intentionally separate from domain models (domain/models.py)
to allow the API shape to evolve independently from the domain.

Rules:
    - These schemas live in infrastructure/, not domain/.
    - Convert API schemas → domain models at the router level before
      calling into the application layer.
    - Convert domain models → API schemas before returning HTTP responses.
    - Add validation and field aliases here (e.g., camelCase for JSON),
      not in domain models.

Example conversion in a router:
    from {{ cookiecutter.project_slug }}.domain.models import AgentInput

    @router.post("/ask")
    async def ask(request: AskRequest, ...) -> AskResponse:
        domain_input = AgentInput(
            query=request.question,
            session_id=request.session_id or "default",
        )
        output = await run_example_agent(domain_input, llm=llm, store=store)
        return AskResponse(answer=output.answer)
"""

from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    """Request body for the /ask endpoint."""

    question: str = Field(description="The user's question or query.")
    session_id: str | None = Field(
        default=None,
        description="Session identifier for multi-turn conversations. "
        "Omit to start a new session.",
    )


class AskResponse(BaseModel):
    """Response body for the /ask endpoint."""

    answer: str
    session_id: str
    sources: list[str] = Field(
        default_factory=list,
        description="Document IDs used as context for this answer.",
    )


class HealthResponse(BaseModel):
    """Response body for the /health endpoint."""

    status: str = "ok"
    version: str


# TODO: Add request/response schemas for your actual API endpoints.
