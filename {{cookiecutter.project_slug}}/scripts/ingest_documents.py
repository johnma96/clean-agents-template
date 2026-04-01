"""Script: ingest documents into the vector store.

This is an operational script, not part of the installable package.
Run it to populate the vector store before using the agent.

Usage:
    uv run python scripts/ingest_documents.py
    # or via Makefile: make ingest  (add the target if needed)

Steps to implement:
    1. Load documents from your data source (files, API, database, etc.)
    2. Convert them to domain Document models.
    3. Instantiate the VectorStore implementation.
    4. Call the ingestion service.

Example:
    import asyncio
    from {{ cookiecutter.project_slug }}.application.services.example_service import run_ingestion
    from {{ cookiecutter.project_slug }}.infrastructure.retrieval.vector_store import VectorStore
    from {{ cookiecutter.project_slug }}.domain.models import Document

    async def main():
        store = VectorStore()
        documents = [...]  # Load from your source
        n = await run_ingestion(documents, store)
        print(f"Ingested {n} documents")

    asyncio.run(main())
"""

# TODO: Implement the ingestion script for your data source.
