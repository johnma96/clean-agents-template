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
│   └── prompts/                       # .txt templates + PromptTemplate (str.format())
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

---

## Git Workflow

### Commit cadence
- Claude Code should suggest a commit after each complete logical task,
  not after each modified file.
- A "logical task" is: an implemented feature, a passing test, a fixed bug,
  a finished refactor, a completed docs section.
- When finishing a task, Claude should say: "This task is complete.
  Suggested commit: `<proposed message>`. Shall I proceed?"
- Claude NEVER commits automatically without user confirmation.

### Commit message format
Use Conventional Commits. Messages must be written in English.

   **Format:** `<type>(<scope>): <description>`

   **Types:**
   - `feat` — new feature or capability
   - `fix` — bug fix
   - `refactor` — code change that neither fixes a bug nor adds a feature
   - `test` — adding or updating tests
   - `docs` — documentation only
   - `chore` — tooling, dependencies, CI, config
   - `style` — formatting, whitespace (no logic change)
   - `perf` — performance improvement

   **Scopes** match the project's architectural layers and components.
   Use lowercase, one word. Common scopes for agent projects:
   `domain`, `application`, `infrastructure`, `llm`, `retrieval`, `memory`,
   `api`, `agent`, `prompts`, `config`, `deps`, `ci`, `tests`, `docs`.

   **Examples:**
   ```
   feat(llm): add streaming support to provider
   fix(retrieval): handle empty search results
   refactor(agent): switch from inheritance to composition
   test(domain): add unit tests for Protocol implementations
   docs(architecture): add ADR for prompt loading decision
   chore(deps): upgrade pydantic to v2.9
   ```

### Commit body (optional)
Use the body to explain **why**, not **what**. The diff already shows the what.
Leave a blank line between the title and the body. Example:

   ```
   refactor(agent): switch from inheritance to composition

   Base class was creating coupling between ResearchAgent and PQRSAgent
   because streaming behavior differed. Composition via agent_utils.py
   keeps each agent self-contained.
   ```

### Commit granularity
One commit per logical task, not per file. If you implement `AnthropicLLM` and its
tests, that is ONE commit with both files. If you implement the arXiv client and also
fix a typo in the README, those are TWO separate commits (`feat` + `docs`).
A commit should be revertable without breaking other things and must have a clear purpose.

For a typical development session, aim for 3–6 commits per day.

### Two additional rules
1. Commit messages are written in English even if the project code has comments in
   Spanish. This is industry standard and keeps the repo professional.
2. The commit body (optional) explains the *why*, not the *what*.
   The diff already shows the what.

---

## Work Log and Session Summary

The project's historical record lives in `docs/work_log.md` at the repo root.

**End-of-session protocol:**
When the user requests a session summary (or uses similar commands like
"Generate today's summary...", "Summarize the work we did..."), you MUST execute
this exact flow to update `work_log.md`:

1. **Analyze Manual Context:** Extract and summarize any explicit information the user
   provided in that same prompt (e.g., external meetings, parallel research,
   conversations with other models).
2. **Analyze the Claude Code Session:** Review your own memory of the current session:
   Which Clean Architecture files did we explore? What code or dependency problems did
   we solve together? What new implementations were developed? What tasks remain pending?
3. **Analyze the Repository (Git):** Use your terminal tools to review commits from the
   last 24 hours (`git log --since="1 day ago"`) and current uncommitted changes
   (`git status` or `git diff`).
4. **Draft and Save:** Create a new entry at the end of `work_log.md` with today's date.
   The format MUST be:

   ### [Date in YYYY-MM-DD format]
   - **Developer Context:** [Summary of the user's manual input]
   - **Work with Claude Code:** [Summary of files touched, bugs fixed, or logic discussed]
   - **Git History:** [Summary of commits made and current repo state]
   - **Pending Tasks:** [Summary of tasks pending for the next session]
