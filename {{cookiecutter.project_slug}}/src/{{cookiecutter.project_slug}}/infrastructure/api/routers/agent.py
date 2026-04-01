"""Agent router — HTTP endpoints that invoke application agents.

This router is the translation layer between HTTP and the application layer:
    HTTP request → API schema → domain model → agent → domain model → API schema → HTTP response

Rules:
    - Never put business logic here. Call agents and services from application/.
    - Convert AskRequest → AgentInput before calling the agent.
    - Convert AgentOutput → AskResponse before returning the HTTP response.
    - Inject dependencies via the functions in infrastructure/api/dependencies.py.

Example (FastAPI):
    from fastapi import APIRouter, Depends
    from {{ cookiecutter.project_slug }}.application.agents.example_agent import run_example_agent
    from {{ cookiecutter.project_slug }}.domain.interfaces import LLMProvider, VectorStore
    from {{ cookiecutter.project_slug }}.domain.models import AgentInput
    from {{ cookiecutter.project_slug }}.infrastructure.api.dependencies import get_llm, get_vector_store
    from {{ cookiecutter.project_slug }}.infrastructure.api.schemas import AskRequest, AskResponse

    router = APIRouter()

    @router.post("/ask", response_model=AskResponse)
    async def ask(
        request: AskRequest,
        llm: LLMProvider = Depends(get_llm),
        store: VectorStore = Depends(get_vector_store),
    ) -> AskResponse:
        output = await run_example_agent(
            input=AgentInput(
                query=request.question,
                session_id=request.session_id or "default",
            ),
            llm=llm,
            store=store,
        )
        return AskResponse(
            answer=output.answer,
            session_id=request.session_id or "default",
            sources=[d.doc_id for d in output.sources],
        )
"""

# TODO: Implement the agent router for your chosen HTTP framework.
