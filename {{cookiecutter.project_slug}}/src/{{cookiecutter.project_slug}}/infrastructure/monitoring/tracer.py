"""LLM call tracer — observability for agent and LLM interactions.

This file is the integration point for your observability / tracing backend.
Tracing gives you visibility into:
    - Which prompts were sent to the LLM and what responses came back.
    - Latency and token usage per call.
    - Full agent traces (multi-step chains, tool calls, retrieval steps).
    - A/B comparisons between prompt versions.

Conventions:
    - All API keys and config come from config.py (Settings).
    - Tracing should be optional — if settings.tracing_enabled is False,
      all tracer methods must be no-ops (never fail because tracing is off).
    - Never let a tracing failure propagate to the caller.
      Catch all exceptions internally and log them at WARNING level.
    - When you pick your backend, rename this file for clarity:
        langfuse_tracer.py, langsmith_tracer.py, cloud_logging_tracer.py

Examples of tracing backends you could implement:
    - Langfuse (pip install langfuse) — open-source, self-hostable
    - LangSmith (pip install langsmith) — hosted, LangChain ecosystem
    - Arize Phoenix (pip install arize-phoenix)
    - OpenTelemetry (pip install opentelemetry-sdk) — vendor-neutral standard
    - Google Cloud Logging / Cloud Trace — if deploying on GCP
    - A simple JSON logger to stdout — good starting point
"""

import logging

from {{ cookiecutter.project_slug }}.config import settings

logger = logging.getLogger(__name__)

# TODO: Install your chosen tracing SDK and import it here.


class Tracer:
    """Observability wrapper for LLM calls and agent traces.

    All methods are safe to call unconditionally — if tracing is disabled
    or the backend is unavailable, they silently do nothing.
    """

    def __init__(self) -> None:
        self.enabled = settings.tracing_enabled
        if self.enabled:
            # TODO: Initialize your tracing SDK client here.
            # Example (Langfuse):
            #   from langfuse import Langfuse
            #   self._client = Langfuse(
            #       public_key=settings.tracing_api_key,
            #       ...
            #   )
            logger.info("Tracing enabled")
        else:
            logger.debug("Tracing disabled — set TRACING_ENABLED=true to enable")

    def trace_generation(
        self,
        name: str,
        input: list[dict],
        output: str,
        model: str = "",
        metadata: dict | None = None,
    ) -> None:
        """Record a single LLM generation call.

        Args:
            name: A descriptive name for this generation (e.g., "example_agent").
            input: The messages sent to the LLM (list of role/content dicts).
            output: The LLM's response text.
            model: The model identifier used for this call.
            metadata: Optional extra data to attach to the trace.
        """
        if not self.enabled:
            return
        try:
            # TODO: Record the generation in your tracing backend.
            pass
        except Exception:  # noqa: BLE001
            logger.warning("Failed to record trace for '%s'", name, exc_info=True)

    def trace_span(self, name: str, metadata: dict | None = None) -> None:
        """Open a named span to group multiple operations under one trace.

        Args:
            name: A descriptive name for this span (e.g., "ingest_then_answer").
            metadata: Optional extra data to attach to the span.
        """
        if not self.enabled:
            return
        try:
            # TODO: Open a span in your tracing backend.
            pass
        except Exception:  # noqa: BLE001
            logger.warning("Failed to open span '%s'", name, exc_info=True)


# Module-level singleton — import this in infrastructure/api/dependencies.py
# or pass it explicitly as a parameter to agents that need tracing.
tracer = Tracer()
