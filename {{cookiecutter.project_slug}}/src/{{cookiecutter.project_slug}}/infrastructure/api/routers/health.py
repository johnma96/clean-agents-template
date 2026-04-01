"""Health check router.

Exposes a /health endpoint that confirms the service is running.
Extend this to check connectivity to critical dependencies
(vector store, LLM provider, memory store) before reporting healthy.

Example (FastAPI):
    from fastapi import APIRouter
    from {{ cookiecutter.project_slug }}.infrastructure.api.schemas import HealthResponse
    from {{ cookiecutter.project_slug }} import __version__

    router = APIRouter()

    @router.get("/", response_model=HealthResponse)
    async def health() -> HealthResponse:
        return HealthResponse(status="ok", version=__version__)
"""

# TODO: Implement the health router for your chosen HTTP framework.
