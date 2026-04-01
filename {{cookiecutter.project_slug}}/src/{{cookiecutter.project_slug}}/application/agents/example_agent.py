"""Example agent — illustrates the agent composition pattern.

An agent in this architecture is an async function (or set of functions) that:
    1. Receives typed inputs (Pydantic models from domain/).
    2. Decides which services/tools to call based on the input.
    3. Programs exclusively against Protocols from domain/interfaces.py.
    4. Returns typed outputs (Pydantic models from domain/).

What an agent is NOT:
    - A class that inherits from a base agent.
    - A function that instantiates infrastructure directly.
    - A function that imports from infrastructure/.

Dependencies (LLMProvider, VectorStore, etc.) are always received as
parameters and injected at the entry point (infrastructure/api/dependencies.py
or equivalent). This makes agents trivially testable with mocks.

When to create a new agent vs. a new service:
    - Agent: the function makes decisions, may iterate, may call tools.
    - Service: the function always follows the same deterministic steps.

How to add a real agent:
    1. Copy this file and rename it (e.g., research_agent.py).
    2. Define the input/output models in domain/models.py if needed.
    3. Load your system prompt via PromptTemplate.
    4. Compose utility functions from agent_utils.py.
    5. Add tests in tests/unit/application/.
    6. Wire the agent into infrastructure/api/routers/ (if using API).
"""

import logging

from {{ cookiecutter.project_slug }}.domain.interfaces import LLMProvider, VectorStore
from {{ cookiecutter.project_slug }}.domain.models import AgentInput, AgentOutput
from {{ cookiecutter.project_slug }}.domain.prompts import PromptTemplate

from .agent_utils import retrieve_and_generate, wrap_output

logger = logging.getLogger(__name__)


async def run_example_agent(
    input: AgentInput,
    llm: LLMProvider,
    store: VectorStore,
) -> AgentOutput:
    """Run the example RAG agent.

    Retrieves relevant documents for the query and generates an answer
    grounded in that context. Replace this implementation with your
    domain-specific agent logic.

    Args:
        input: The agent's input containing the user query and session info.
        llm: An LLMProvider implementation (injected by the caller).
        store: A VectorStore implementation (injected by the caller).

    Returns:
        An AgentOutput with the generated answer and source documents.
    """
    logger.info("Running example agent", extra={"session_id": input.session_id})

    system_prompt = PromptTemplate("system", "agent").render(
        system_instructions="Answer questions using only the provided context.",
    )

    answer = await retrieve_and_generate(
        query=input.query,
        llm=llm,
        store=store,
        system_prompt=system_prompt,
        top_k=5,
    )

    logger.info("Example agent completed", extra={"session_id": input.session_id})
    return wrap_output(answer)


# TODO: Replace this example with your actual agent.
# For complex agents with tool-use loops or multi-step reasoning,
# consider splitting into multiple functions and composing them here.
