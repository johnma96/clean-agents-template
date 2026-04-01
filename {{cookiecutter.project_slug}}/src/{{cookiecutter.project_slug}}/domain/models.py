"""Domain models — core business entities for {{ cookiecutter.project_name }}.

This file defines the data structures that flow through every layer of the system.
Models defined here are the shared language of the entire application.

Rules:
    - Only stdlib and Pydantic are allowed here. No external SDKs.
    - Models must be immutable where possible (use frozen=True or avoid mutation).
    - Use Field(description=...) to document the intent of each field.
    - No business logic in models — keep them as pure data containers.
    - All layers reference these models. Never create parallel "DTO" structures
      unless there is a strong API-contract reason (e.g., a versioned public API).

Reference:
    Pydantic v2 docs: https://docs.pydantic.dev/latest/

How to add a new model:
    1. Define a Pydantic BaseModel below.
    2. Import it in the layers that need it (application/, infrastructure/).
    3. If the model crosses the HTTP boundary, add a corresponding schema in
       infrastructure/api/schemas.py (to decouple API shape from domain shape).
"""

from pydantic import BaseModel, Field


# ── Core conversation types ───────────────────────────────────────────────────

class Message(BaseModel):
    """A single message in a conversation with an LLM."""

    role: str = Field(description="One of: 'system', 'user', 'assistant'")
    content: str


# ── Retrieval types ───────────────────────────────────────────────────────────

class Document(BaseModel):
    """A document retrieved from a vector store or knowledge base."""

    doc_id: str
    text: str
    metadata: dict = Field(default_factory=dict)
    score: float = Field(default=0.0, description="Relevance score from the retriever (0–1)")


# ── Agent I/O types ───────────────────────────────────────────────────────────

class AgentInput(BaseModel):
    """Standard input envelope for an agent invocation.

    Extend this model or create domain-specific variants as your project grows.
    """

    query: str = Field(description="The user's request or question")
    session_id: str = Field(default="default", description="Identifies the conversation session")
    metadata: dict = Field(default_factory=dict, description="Optional extra context")


class AgentOutput(BaseModel):
    """Standard output envelope from an agent invocation."""

    answer: str
    sources: list[Document] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)


# ── TODO: Add your domain-specific models below ───────────────────────────────
# Examples of what you might add depending on your domain:
#
#   class ResearchPaper(BaseModel):         # document-processing domain
#   class CustomerProfile(BaseModel):       # CRM / financial domain
#   class Transaction(BaseModel):           # payments domain
#   class PolicyDocument(BaseModel):        # insurance / pensions domain
#
# Keep models focused on your business domain, not on infrastructure details.
