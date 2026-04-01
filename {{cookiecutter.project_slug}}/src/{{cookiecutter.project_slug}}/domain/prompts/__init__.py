"""Prompt template loader for {{ cookiecutter.project_name }}.

Prompts are stored as plain .txt files with Jinja2 syntax and organized
into subdirectories by purpose:

    domain/prompts/
    ├── system/     ← system prompts that define agent persona/behavior
    └── tasks/      ← task-specific prompts (extraction, summarization, etc.)

Keeping prompts as .txt files means they are:
    - Versionable and diffable in git
    - Editable without touching Python code
    - Testable independently from the rest of the system

Usage:
    from {{ cookiecutter.project_slug }}.domain.prompts import PromptTemplate

    template = PromptTemplate("tasks", "extraction")
    rendered = template.render(topic="AI agents", text="...")
"""

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined, TemplateNotFound

from {{ cookiecutter.project_slug }}.domain.exceptions import PromptNotFoundError

_PROMPTS_DIR = Path(__file__).parent

# Jinja2 environment scoped to this directory.
# StrictUndefined raises an error for any variable referenced in the template
# that was not passed to render(), catching mistakes early.
_env = Environment(
    loader=FileSystemLoader(str(_PROMPTS_DIR)),
    undefined=StrictUndefined,
    trim_blocks=True,
    lstrip_blocks=True,
)


class PromptTemplate:
    """Loads and renders a prompt template from a .txt file.

    Templates live in subdirectories under domain/prompts/:
        - system/   → agent system prompts
        - tasks/    → task-specific prompts

    Variables in templates use Jinja2 syntax: {{ variable_name }}

    Example:
        template = PromptTemplate("tasks", "extraction")
        rendered = template.render(topic="pensions", document_text="...")

    Args:
        category: Subdirectory name (e.g., "system", "tasks").
        name: Template filename without the .txt extension.

    Raises:
        PromptNotFoundError: If the template file does not exist.
    """

    def __init__(self, category: str, name: str) -> None:
        self._path = f"{category}/{name}.txt"
        try:
            self._template = _env.get_template(self._path)
        except TemplateNotFound as exc:
            raise PromptNotFoundError(
                f"Prompt template not found: {self._path}. "
                f"Expected file at: {_PROMPTS_DIR / self._path}"
            ) from exc

    def render(self, **kwargs: str) -> str:
        """Render the template with the provided variables.

        Args:
            **kwargs: Variables referenced in the template.

        Returns:
            The rendered prompt string.

        Raises:
            jinja2.UndefinedError: If a required variable is missing from kwargs.
        """
        return self._template.render(**kwargs)

    def __repr__(self) -> str:
        return f"PromptTemplate({self._path!r})"
