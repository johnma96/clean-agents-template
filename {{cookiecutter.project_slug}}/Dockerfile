# Multi-stage Dockerfile for {{ cookiecutter.project_name }}
# Adjust the CMD to match your entry point once infrastructure/api/main.py is implemented.

FROM python:{{ cookiecutter.python_version }}-slim AS base

WORKDIR /app

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# ── Dependencies stage ────────────────────────────────────────────────────────
FROM base AS deps

COPY pyproject.toml ./
RUN uv sync --no-dev --no-install-project

# ── Application stage ─────────────────────────────────────────────────────────
FROM base AS app

# Copy installed dependencies from deps stage
COPY --from=deps /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy application source
COPY src/ ./src/
COPY configs/ ./configs/

# Run as non-root user
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

# TODO: Update the CMD once infrastructure/api/main.py is implemented.
# CMD ["uvicorn", "{{ cookiecutter.project_slug }}.infrastructure.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["echo", "Update CMD in Dockerfile to start your application."]
