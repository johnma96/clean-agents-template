# Clean Agents Template 🤖

A production-ready [Cookiecutter](https://github.com/cookiecutter/cookiecutter) template for building AI Agents and LLM applications using Python and Clean Architecture.

This template is designed to scale from simple prototypes to complex, multi-agent enterprise systems. It enforces a strict separation of concerns (Domain, Application, Infrastructure) so you can easily swap models, vector databases, or APIs without rewriting your core logic.

## 🌟 Features

- **Clean Architecture:** Strict boundaries (`domain/` → `application/` → `infrastructure/`).
- **Prompt Management:** Versionable Jinja2 prompt templates decoupled from Python code.
- **Agent Patterns:** Utilities for retrieve-and-generate, tool calling, and workflow orchestration.
- **Configurable Layers:** Choose to include an HTTP API (FastAPI), Monitoring/Tracing, or MCP (Model Context Protocol) clients during setup.
- **Robust Tooling:** Pre-configured with `uv` (fast package manager), `pytest`, `ruff` (linter/formatter), and pre-commit hooks.
- **Production Ready:** Includes Dockerfiles, CI/CD GitHub action workflows, and incident response runbooks.

## 🚀 Quickstart

To generate a new project using this template, you need [Cookiecutter](https://cookiecutter.readthedocs.io/) installed.

### 1. Generate the project

```bash
# Using pipx (recommended)
pipx run cookiecutter https://github.com/tu-usuario/clean-agents-template

# Or if you have cookiecutter installed globally:
cookiecutter https://github.com/tu-usuario/clean-agents-template
```

### 2. Answer the prompts

You will be asked a few questions to configure your project. You can skip the optional layers if you are building a simple script.

```text
project_name [My Agent Project]: Support Bot
project_slug [support_bot]: support_bot
description [A short description of the project]: AI Agent for customer support
author_name [Your Name]: Mario
author_email [you@example.com]: mario@example.com
python_version [3.11]: 3.11
include_api [yes]: yes
include_monitoring [yes]: yes
include_mcp [yes]: no
```

### 3. Start building

The template will automatically initialize a Git repository and use `uv` to sync dependencies (if installed). 

```bash
cd support_bot/
cp .env.example .env
make test
```

Read the generated `README.md` and `CLAUDE.md` in your new project for architecture details and next steps.

## 🏗️ What does this generate?

```text
support_bot/
├── .github/workflows/         # CI/CD pipelines (ci.yml, deploy.yml)
├── configs/                   # Environment-specific configs (base.yaml, development.yaml, etc.)
├── data/                      # Local data stores, samples, and schemas
├── docs/                      # Architecture decisions (ADRs) and Incident Runbooks
├── notebooks/                 # Jupyter notebooks for experimentation
├── scripts/                   # Utility scripts (e.g., ingest_documents, evaluate_agent)
├── src/support_bot/
│   ├── config.py              # Centralized pydantic settings
│   ├── domain/                # Business logic, interfaces (Protocols), exceptions
│   │   └── prompts/           # Versionable Jinja2 prompt templates
│   ├── application/           # Orchestration layer
│   │   ├── agents/            # Autonomous agent definitions and utils
│   │   ├── services/          # Deterministic services
│   │   └── workflows/         # Multi-agent workflows
│   └── infrastructure/        # External system implementations
│       ├── api/               # FastAPI endpoints, dependencies, and schemas
│       ├── data/              # Data source connectors
│       ├── llm/               # LLM provider implementations
│       ├── mcp/               # Model Context Protocol clients
│       ├── memory/            # InMemory or persistent memory stores
│       ├── monitoring/        # Tracing and observability tools
│       └── retrieval/         # Vector stores and document loaders
├── tests/                     # conftest.py with mocks, unit/ and integration/ tests
├── .env.example               # Environment variables template
├── .gitignore                 # Pre-configured Python gitignore
├── .pre-commit-config.yaml    # Pre-commit hooks for code quality
├── CLAUDE.md                  # Architecture context for AI coding assistants like Claude Code
├── Dockerfile                 # Production-ready container definition
├── docker-compose.yaml        # Local stack definition
├── Makefile                   # Essential developer commands (test, lint, format)
├── pyproject.toml             # Modern Python packaging configuration
└── README.md                  # Generated project README with quickstart
```

## 📝 License

This project is licensed under the MIT License.
