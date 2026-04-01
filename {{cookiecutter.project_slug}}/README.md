# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

---

## Architecture

Clean Architecture with three layers and explicit contracts:

```
Domain (pure logic + Protocols) → Application (orchestration) → Infrastructure (external systems)
```

- **Domain:** Business entities, typed exceptions, interfaces (Protocols), prompt templates. Zero external dependencies.
- **Application:** Agents (autonomous) and Services (deterministic) that orchestrate workflows. Programs against Protocols.
- **Infrastructure:** All external implementations — LLM providers, vector stores, memory stores, APIs.

See [docs/architecture.md](docs/architecture.md) for design decisions (ADRs).

---

## Quick start

```bash
# Prerequisites: Python {{ cookiecutter.python_version }}, uv
git clone <your-repo-url>
cd {{ cookiecutter.project_slug }}

uv sync --all-extras       # Install all dependencies
cp .env.example .env       # Edit with your API keys and config

make test                  # Verify the setup with unit tests
```

---

## Project structure

```
src/{{ cookiecutter.project_slug }}/
├── config.py              # Pydantic Settings — all config in one place
├── domain/                # Pure business logic (no external deps)
│   ├── models.py
│   ├── exceptions.py
│   ├── interfaces.py      # Protocols: LLMProvider, VectorStore, MemoryStore
│   └── prompts/           # Jinja2 prompt templates
├── application/
│   ├── agents/            # Autonomous behavior
│   ├── services/          # Deterministic flows
│   └── workflows/         # Multi-agent orchestration
└── infrastructure/        # All external implementations
    ├── llm/
    ├── memory/
    ├── retrieval/
    ├── data/
    ├── api/               # HTTP entry point
    └── monitoring/        # Tracing / observability
```

---

## Commands

```bash
make test        # Unit tests (fast, no IO)
make test-all    # All tests (unit + integration)
make lint        # Linter (ruff)
make format      # Format code
make run-api     # Start HTTP server
make evaluate    # Run agent evaluation script
```

---

## Next steps

1. Implement `infrastructure/llm/llm_provider.py` with your chosen LLM SDK
2. Implement `infrastructure/retrieval/vector_store.py` with your chosen vector store
3. Define your domain models in `domain/models.py`
4. Write your first real agent in `application/agents/`
5. Run `make test` to verify everything works

Read [CLAUDE.md](CLAUDE.md) for the full architecture guide (also read by Claude Code automatically).

---

## License

MIT — {{ cookiecutter.author_name }}
