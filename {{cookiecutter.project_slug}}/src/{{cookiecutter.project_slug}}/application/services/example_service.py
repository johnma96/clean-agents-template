"""Example service — illustrates the deterministic service pattern.

A service in this architecture is an async function that:
    1. Executes a fixed, predictable sequence of steps.
    2. Coordinates multiple infrastructure components (VectorStore, DataSource, etc.)
    3. Programs exclusively against Protocols from domain/interfaces.py.
    4. Returns typed outputs (Pydantic models from domain/).

The difference between a service and an agent:
    - Service: always runs the same steps in the same order (deterministic).
    - Agent: makes decisions, may iterate, may choose which tools to call.

Typical service responsibilities:
    - Ingestion pipelines (fetch → parse → chunk → embed → upsert)
    - Scheduled batch jobs (fetch data → process → store results)
    - Retrieval pipelines (search → rerank → format)
    - Evaluation flows (load dataset → run agent → compute metrics)

How to add a real service:
    1. Copy this file and rename it (e.g., ingestion_service.py).
    2. Define input/output models in domain/models.py if needed.
    3. Accept all infrastructure dependencies as parameters (never instantiate here).
    4. Add tests in tests/unit/application/.
"""

import logging

from {{ cookiecutter.project_slug }}.domain.interfaces import VectorStore
from {{ cookiecutter.project_slug }}.domain.models import Document

logger = logging.getLogger(__name__)


async def run_ingestion(
    documents: list[Document],
    store: VectorStore,
) -> int:
    """Ingest a list of documents into the vector store.

    This is a deterministic pipeline: validate → upsert → return count.
    No decisions are made — the same steps always run in the same order.

    Args:
        documents: Documents to index. Must have non-empty doc_id and text.
        store: A VectorStore implementation (injected by the caller).

    Returns:
        Number of documents successfully ingested.

    Raises:
        IngestionError: If the upsert operation fails (propagated from store).
        ValueError: If any document has an empty doc_id or text.
    """
    valid = [d for d in documents if d.doc_id and d.text]
    skipped = len(documents) - len(valid)

    if skipped:
        logger.warning("Skipping %d documents with empty doc_id or text", skipped)

    if not valid:
        logger.info("No valid documents to ingest")
        return 0

    logger.info("Ingesting %d documents", len(valid))
    await store.upsert(valid)
    logger.info("Ingestion complete")
    return len(valid)


# TODO: Replace or extend this example with your actual services.
# Common services to implement:
#   - ingestion_service.py  → fetch, parse, chunk, embed, upsert
#   - retrieval_service.py  → search, rerank, format for LLM context
#   - evaluation_service.py → load golden dataset, run agent, compute metrics
