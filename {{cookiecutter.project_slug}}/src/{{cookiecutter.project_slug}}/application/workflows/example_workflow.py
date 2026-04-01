"""Example workflow — illustrates multi-agent / multi-service orchestration.

A workflow coordinates two or more agents or services in sequence or in
parallel. It is the right abstraction when a single user request requires
multiple processing steps that each deserve their own function.

When to use a workflow vs. an agent:
    - Workflow: fixed topology of agents/services (step A → step B → step C).
    - Agent: dynamic — the agent itself decides which tools to call and when.

Workflows are still part of the application layer and must:
    - Program against Protocols from domain/interfaces.py.
    - Never import from infrastructure/.
    - Accept all infrastructure dependencies as parameters.

Example use cases:
    - Ingest documents, then answer a question about them.
    - Run a research agent, then format the output for a specific channel.
    - Validate input with a guard agent, then route to a specialized agent.

How to add a real workflow:
    1. Copy this file and rename it (e.g., research_workflow.py).
    2. Import the agents and services you want to orchestrate.
    3. Accept all dependencies as parameters and thread them through.
    4. Add tests in tests/unit/application/.
"""

import logging

from {{ cookiecutter.project_slug }}.domain.interfaces import LLMProvider, VectorStore
from {{ cookiecutter.project_slug }}.domain.models import AgentInput, AgentOutput, Document

from ..agents.example_agent import run_example_agent
from ..services.example_service import run_ingestion

logger = logging.getLogger(__name__)


async def ingest_then_answer(
    documents: list[Document],
    query: str,
    llm: LLMProvider,
    store: VectorStore,
    session_id: str = "default",
) -> AgentOutput:
    """Ingest a set of documents and immediately answer a query about them.

    Workflow steps:
        1. Ingest documents into the vector store (service).
        2. Run the example agent to answer the query (agent).

    Args:
        documents: Documents to ingest before answering.
        query: The question to answer after ingestion.
        llm: An LLMProvider implementation (injected).
        store: A VectorStore implementation (injected).
        session_id: Session identifier for conversational memory.

    Returns:
        An AgentOutput with the answer grounded in the newly ingested documents.
    """
    ingested = await run_ingestion(documents, store)
    logger.info("Workflow: ingested %d documents, now answering query", ingested)

    return await run_example_agent(
        input=AgentInput(query=query, session_id=session_id),
        llm=llm,
        store=store,
    )


# TODO: Replace or extend this example with your actual workflows.
