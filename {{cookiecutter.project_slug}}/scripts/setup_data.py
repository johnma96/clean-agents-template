"""Script: download and prepare data from corporate sources.

This is an operational script, not part of the installable package.
Run it once before starting development to populate data/raw/ and data/samples/.

Usage:
    uv run python scripts/setup_data.py
    # or via Makefile: make setup-data  (add the target if needed)

Steps to implement:
    1. Connect to your data source (BigQuery, RDBMS, API, file share, etc.).
    2. Download raw data and save to data/raw/.
    3. Transform or sample a subset and save to data/samples/ for local development.
    4. Log what was downloaded and where it was saved.

Example:
    from {{ cookiecutter.project_slug }}.infrastructure.data.data_source import DataSource
    from {{ cookiecutter.project_slug }}.paths import RAW_DIR, SAMPLES_DIR

    async def main():
        source = DataSource()
        records = await source.fetch(query="SELECT * FROM my_table LIMIT 1000")
        # Save raw
        (RAW_DIR / "my_table.json").write_text(json.dumps(records))
        # Save a small sample for development
        (SAMPLES_DIR / "my_table_sample.json").write_text(json.dumps(records[:50]))
        print(f"Downloaded {len(records)} records")
"""

# TODO: Import your data access client from infrastructure/data/
# TODO: Download raw data to data/raw/
# TODO: Transform and save samples to data/samples/ for local development
# TODO: Log what was downloaded and where it was saved
