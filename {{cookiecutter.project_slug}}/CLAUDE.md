# {{ cookiecutter.project_name }} — Context for Claude Code

> Read automatically by Claude Code at the start of every session.
> Keep this file up to date as the project evolves.

---

## Architecture: Clean Architecture (3 layers)

```
src/{{ cookiecutter.project_slug }}/
├── config.py                          # Pydantic Settings — single source of config
├── domain/                            # PURE LOGIC — zero external dependencies
│   ├── models.py                      # Business entities (Pydantic v2)
│   ├── exceptions.py                  # Typed domain exceptions
│   ├── interfaces.py                  # Protocols: LLMProvider, VectorStore, MemoryStore
│   └── prompts/                       # .txt templates + PromptTemplate (Jinja2)
│       ├── system/                    # Agent persona / behavior prompts
│       └── tasks/                     # Task-specific prompts
├── application/                       # ORCHESTRATION — programs against Protocols
│   ├── agents/                        # Autonomous components (decide, iterate, call tools)
│   │   ├── agent_utils.py             # Shared functions via COMPOSITION (no inheritance)
│   │   └── example_agent.py
│   ├── services/                      # Deterministic flows (same steps every time)
│   │   └── example_service.py
│   └── workflows/                     # Multi-agent / multi-service orchestration
│       └── example_workflow.py
└── infrastructure/                    # CONCRETE IMPLEMENTATIONS — all SDKs live here
    ├── llm/llm_provider.py            # Implements LLMProvider Protocol
    ├── memory/memory_store.py         # Implements MemoryStore Protocol
    ├── retrieval/vector_store.py      # Implements VectorStore Protocol
    ├── data/data_source.py            # External / corporate data access
    ├── mcp/mcp_client.py              # MCP server connections (if include_mcp=yes)
    ├── api/                           # HTTP entry point (if include_api=yes)
    │   ├── main.py
    │   ├── dependencies.py            # Dependency injection — wire infra to application
    │   ├── schemas.py                 # API request/response models (separate from domain)
    │   └── routers/
    └── monitoring/tracer.py           # LLM call tracing (if include_monitoring=yes)
```

### Dependency direction (NEVER violate)

```
infrastructure → application → domain
```

- `domain/` imports nothing outside stdlib and Pydantic
- `application/` imports from `domain/` only (never from `infrastructure/`)
- `infrastructure/` imports from `domain/` and `application/`
- The wiring happens in `infrastructure/api/dependencies.py`

---

## How to add a new agent

1. Create `src/{{ cookiecutter.project_slug }}/application/agents/your_agent.py`
2. Define input/output models in `domain/models.py` if the existing ones are not enough
3. Add a system prompt in `domain/prompts/system/your_agent.txt`
4. Write an async function that:
   - Accepts typed domain models as input
   - Receives infrastructure dependencies (LLMProvider, VectorStore, etc.) as parameters
   - Composes functions from `agent_utils.py`
   - Returns a typed domain model
5. Add tests in `tests/unit/application/test_your_agent.py` using mock fixtures from `conftest.py`
6. Wire the agent into `infrastructure/api/routers/` if it needs an HTTP endpoint

---

## How to add a new LLM provider

1. Create `src/{{ cookiecutter.project_slug }}/infrastructure/llm/your_provider.py`
   (e.g., `anthropic_llm.py`, `gemini_llm.py`)
2. Implement the `LLMProvider` Protocol from `domain/interfaces.py`:
   - `async def generate(self, messages: list[Message]) -> str`
   - `async def stream(self, messages: list[Message]) -> AsyncIterator[str]`
3. Catch SDK-specific exceptions and re-raise as `GenerationError` or `RateLimitError`
4. Register it in `infrastructure/api/dependencies.py` → `get_llm()`
5. Add the SDK to `pyproject.toml` dependencies

---

## How to add a new service (deterministic flow)

1. Create `src/{{ cookiecutter.project_slug }}/application/services/your_service.py`
2. Write async functions that:
   - Execute a fixed sequence of steps (no branching or tool-use loops)
   - Accept infrastructure dependencies as parameters
   - Return domain models
3. Add tests in `tests/unit/application/`

---

## How to add a new vector store implementation

1. Create `src/{{ cookiecutter.project_slug }}/infrastructure/retrieval/your_store.py`
2. Implement the `VectorStore` Protocol from `domain/interfaces.py`:
   - `async def search(self, query: str, k: int) -> list[Document]`
   - `async def upsert(self, documents: list[Document]) -> None`
3. Handle embedding internally (the application layer passes raw text)
4. Register it in `infrastructure/api/dependencies.py` → `get_vector_store()`

---

## Coding conventions

- **Type hints** on all function signatures (parameters and return types)
- **Pydantic v2** for all data models — no raw dicts crossing layer boundaries
- **Google-style docstrings** on all public functions and classes
- **`async/await`** throughout — no blocking I/O
- **`logging`** module — never use `print()` in production code
- **Config** via `from {{ cookiecutter.project_slug }}.config import settings` — nowhere else
- **Line length**: 100 characters (enforced by ruff)
- **Imports**: sorted by ruff (isort-compatible)

---

## What NOT to do

- Do NOT import from `infrastructure/` in `domain/` or `application/`
- Do NOT instantiate infrastructure classes inside agents or services
- Do NOT hardcode API keys, URLs, or secrets — use `config.py` + `.env`
- Do NOT use class inheritance for agents — use composition via `agent_utils.py`
- Do NOT hardcode prompts as Python f-strings — use `domain/prompts/*.txt`
- Do NOT put business logic in `infrastructure/` — it belongs in `application/`
- Do NOT catch broad exceptions silently — always log or re-raise as domain exceptions

---

## Running tests

```bash
make test        # Unit tests only — fast, no IO, no API calls
make test-all    # Unit + integration tests
make lint        # ruff check
make format      # ruff format + autofix
```

Unit tests use mock Protocol implementations from `tests/conftest.py`.
Integration tests require real (or local ephemeral) backends.

---

## Adding a dependency

```bash
uv add <package>           # Production dependency
uv add --dev <package>     # Dev-only dependency
```

Always add the corresponding field to `config.py` (Settings) and `.env.example`
when adding a new SDK that requires credentials.
