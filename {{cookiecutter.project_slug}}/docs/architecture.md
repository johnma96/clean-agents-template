# Architecture Decision Records (ADRs)

This document captures the architectural decisions made in **{{ cookiecutter.project_name }}**.
Add a new ADR for every significant design choice so future team members understand the context.

---

## ADR-001: Clean Architecture with three layers

**Date:** <!-- fill in -->
**Status:** Accepted

**Context:**
We need a project structure that scales from a simple prototype to a production system
and is easy to test, maintain, and extend as providers change.

**Decision:**
Adopt Clean Architecture with three explicit layers:
- `domain/` — pure business logic, zero external dependencies
- `application/` — orchestration against domain Protocols
- `infrastructure/` — all external implementations (LLMs, databases, APIs)

Contracts between layers are defined as Python Protocols in `domain/interfaces.py`.

**Consequences:**
Slightly more boilerplate upfront. Significantly easier to test (mock Protocols),
swap implementations, and onboard new contributors.

---

## ADR-002: Composition over inheritance for agents

**Date:** <!-- fill in -->
**Status:** Accepted

**Context:**
Agents share patterns (retrieve-and-generate, tool calling, memory access) but differ
enough in behavior that a base class would create tight coupling and hidden behavior.

**Decision:**
Use shared functions in `application/agents/agent_utils.py` instead of a base class.
Each agent imports only the utilities it needs.

**Consequences:**
More explicit imports per agent. No hidden behavior inherited from parent classes.
Each agent is self-contained and independently testable.

---

## ADR-003: Prompts as .txt files with str.format()

**Date:** <!-- fill in -->
**Status:** Accepted

**Context:**
Prompts need to be versionable (diff in git), editable without touching Python code,
and testable independently. Inline f-strings make this hard.
A Jinja2-based approach was considered but rejected: Jinja2 is an external dependency
that would live inside `domain/`, violating the principle that the domain layer has
zero external dependencies beyond Pydantic. The domain should not know that Jinja2 exists,
just as it should not know that GCP exists.

**Decision:**
Store prompts as `.txt` files in `domain/prompts/` with Python `str.format()` syntax
for variable substitution. Loaded via `PromptTemplate` in `domain/prompts/__init__.py`
using only Python stdlib — no external dependencies introduced.

**Consequences:**
Prompts are diffable in git and editable by non-engineers. `str.format()` is sufficient
for V1–V3 (variable substitution, no conditional logic). If conditional logic in prompts
is needed in the future (V6+), Jinja2 can be introduced as a conscious, documented decision
at that point — but only outside the domain layer.

---

<!-- Add new ADRs below following this template:

## ADR-00N: [Title]

**Date:** YYYY-MM-DD
**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-00X

**Context:** Why does this decision need to be made?

**Decision:** What was decided?

**Consequences:** What are the trade-offs?

-->
