# clean-agents-template — Context for Claude Code

> Read automatically by Claude Code at the start of every session.
> This file describes the **cookiecutter template itself**, not the generated projects.
> For generated project context, see `{{cookiecutter.project_slug}}/CLAUDE.md`.

---

## What this repo is

This is a **cookiecutter template** for building AI agents with Clean Architecture.
Running `cookiecutter .` (or `cookiecutter gh:org/clean-agents-template`) generates
a fully structured Python project under a new directory named after `project_slug`.

The template directory is `{{cookiecutter.project_slug}}/`. Every file inside it is
rendered by cookiecutter at generation time — `{{ cookiecutter.variable }}` expressions
are replaced with the values the user provides.

---

## Repository structure

```
clean-agents-template/
├── cookiecutter.json                  # Template variables and their defaults
├── hooks/
│   ├── pre_gen_project.py             # Validation before generation (slug format, etc.)
│   └── post_gen_project.py            # Cleanup + git init + uv sync after generation
└── {{cookiecutter.project_slug}}/     # The actual template (rendered on generation)
    ├── CLAUDE.md                      # Context for agents working on generated projects
    ├── .pre-commit-config.yaml
    ├── pyproject.toml
    ├── src/{{cookiecutter.project_slug}}/
    │   ├── domain/
    │   ├── application/
    │   └── infrastructure/
    └── tests/
```

---

## Cookiecutter variables

Defined in `cookiecutter.json`. Current variables:

| Variable | Default | Notes |
|---|---|---|
| `project_name` | `"My Agent Project"` | Human-readable name. May contain spaces. |
| `project_slug` | `"my_agent_project"` | Python-safe identifier (snake_case). Used for package name, dirs, imports. |
| `description` | `"A short description..."` | Used in pyproject.toml and README. |
| `author_name` | `"Your Name"` | |
| `author_email` | `"you@example.com"` | |
| `python_version` | `"3.11"` | Used in pyproject.toml and Dockerfile. |
| `include_api` | `["yes", "no"]` | First item is default. Conditional dir: `infrastructure/api/`. |
| `include_monitoring` | `["yes", "no"]` | Conditional dir: `infrastructure/monitoring/`. |
| `include_mcp` | `["yes", "no"]` | Conditional dir: `infrastructure/mcp/`. |
| `include_workflows` | `["yes", "no"]` | Conditional dir: `application/workflows/`. |

---

## Template variable syntax

Cookiecutter renders every file in `{{cookiecutter.project_slug}}/` at generation time.
This means Python files in the template contain `{{ }}` expressions that are **not
valid Python** — the IDE will flag them as syntax errors. This is expected and correct.

**Key conventions used in this template:**

```
{{ cookiecutter.project_slug }}                         → my_agent_project
{{ cookiecutter.project_name }}                         → My Agent Project
{{ cookiecutter.project_slug | title | replace('_', '') }}  → MyAgentProject  (CamelCase class names)
{{ cookiecutter.python_version | replace('.', '') }}    → 311  (for ruff target-version)
{{ cookiecutter.project_slug | upper }}_ERROR           → MY_AGENT_PROJECT_ERROR
```

**Why `project_slug` for class names?** `project_slug` is guaranteed to be a valid
Python identifier (snake_case). `project_name` may contain spaces, tildes, or digits
at the start — all of which would produce invalid class names.

---

## How to add a new template variable

1. Add the variable to `cookiecutter.json` with a sensible default.
2. Use it in the appropriate template files with `{{ cookiecutter.new_variable }}`.
3. If it controls optional directories, add the removal logic in `hooks/post_gen_project.py`.
4. Update this file and the generated project's `CLAUDE.md` if the architecture changes.

---

## How to test the template

```bash
# Generate a project with all defaults (non-interactive)
cookiecutter . --no-input --output-dir /tmp/test-gen

# Generate with specific values
cookiecutter . --no-input project_name="PQRS Classifier" project_slug="pqrs_classifier"

# Verify the generated project structure
ls /tmp/test-gen/pqrs_classifier/

# Run the generated project's tests
cd /tmp/test-gen/pqrs_classifier && make test
```

> Always test generation after modifying hooks or adding/removing template variables.

---

## Hooks

### `hooks/pre_gen_project.py`
Runs **before** generation. Currently validates:
- `project_slug` is a valid Python identifier (no spaces, no special chars, no leading digits).

### `hooks/post_gen_project.py`
Runs **after** generation. Steps (all graceful — one failure doesn't abort the rest):
1. Remove optional directories based on `include_*` choices.
2. `git init`
3. `uv sync` (if uv is on PATH)
4. Print a welcome message with next steps.

---

## What NOT to do

- Do NOT hardcode `project_slug` or `project_name` values inside template files —
  always use `{{ cookiecutter.variable }}`.
- Do NOT put business logic in hooks — keep them as thin orchestrators.
- Do NOT add a variable to `cookiecutter.json` without updating `post_gen_project.py`
  if it controls optional directories.

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

   **Scopes** for this repo. Use lowercase, one word:
   `template`, `hooks`, `config`, `docs`, `ci`, `vars`.

   **Examples:**
   ```
   feat(template): add include_memory optional directory
   fix(hooks): handle project_slug with leading digits
   refactor(template): switch exception base class to project_slug-based naming
   docs(template): update ADR-003 to reflect str.format() decision
   chore(config): bump ruff pre-commit hook to v0.7
   ```

### Commit body (optional)
Use the body to explain **why**, not **what**. The diff already shows the what.
Leave a blank line between the title and the body.

### Commit granularity
One commit per logical task, not per file. A commit should be revertable without
breaking other things and must have a clear purpose.

For a typical session, aim for 3–6 commits per day.

### Two additional rules
1. Commit messages are written in English even if notes are in Spanish.
2. The commit body (optional) explains the *why*, not the *what*.
