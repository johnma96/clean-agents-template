"""Data source implementation — access to external or corporate data.

This file is the integration point for structured data sources such as
relational databases, data warehouses, REST APIs, or file systems.

If you define a DataSource Protocol in domain/interfaces.py, implement it here.
Otherwise, use this file as a thin access layer that returns domain models.

Conventions:
    - All connection config comes from config.py (Settings).
    - Return domain models (from domain/models.py), not raw SDK objects or dicts.
    - Catch data-source-specific exceptions and re-raise as domain exceptions.
    - Never put business logic here — just fetch and map to domain models.
    - When you pick your backend, rename this file for clarity:
        bigquery_source.py, postgres_source.py, rest_api_source.py

Examples of data sources you could implement:
    - PostgreSQL / Cloud SQL (pip install asyncpg)
    - BigQuery (pip install google-cloud-bigquery)
    - REST API via httpx (already in base dependencies)
    - Parquet / CSV files via pandas or polars
    - Firestore (pip install google-cloud-firestore)
"""

from {{ cookiecutter.project_slug }}.config import settings

# TODO: Install your chosen data access library and import it here.
# TODO: Import the domain models your data source returns.


class DataSource:
    """Thin access layer for your external or corporate data source.

    Args:
        connection_string: Connection URL or identifier for the data source.
            Defaults to the value in settings (add the field to config.py).
    """

    def __init__(self, connection_string: str | None = None) -> None:
        # TODO: Store connection config and initialize your client.
        pass

    async def fetch(self, query: str) -> list[dict]:
        """Fetch records matching a query from the data source.

        Replace the return type with a specific domain model once you know
        what shape of data this source returns.

        Args:
            query: A query string, SQL statement, or filter expression
                appropriate for your backend.

        Returns:
            List of records as dicts. Replace with domain models when ready.

        Raises:
            ProviderError: If the data source is unreachable or returns an error.
        """
        # TODO: Execute the query and map results to domain models.
        raise NotImplementedError("Implement fetch() for your data source.")
