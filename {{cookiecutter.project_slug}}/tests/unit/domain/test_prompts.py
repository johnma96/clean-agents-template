"""Unit tests for the PromptTemplate loader.

Templates use Python str.format() syntax — {variable_name}.
Missing variables raise KeyError; missing template files raise PromptNotFoundError.
"""

import pytest

from {{ cookiecutter.project_slug }}.domain.exceptions import PromptNotFoundError
from {{ cookiecutter.project_slug }}.domain.prompts import PromptTemplate


@pytest.mark.unit
class TestPromptTemplate:
    def test_load_system_prompt(self) -> None:
        template = PromptTemplate("system", "agent")
        rendered = template.render(system_instructions="Be helpful.")
        assert "Be helpful." in rendered

    def test_load_task_prompt_with_variables(self) -> None:
        template = PromptTemplate("tasks", "example_task")
        rendered = template.render(
            task_name="extraction",
            context="Some context here.",
            user_input="Extract the key points.",
            instructions="List each point on a new line.",
        )
        assert "extraction" in rendered
        assert "Some context here." in rendered

    def test_missing_template_raises_prompt_not_found(self) -> None:
        with pytest.raises(PromptNotFoundError):
            PromptTemplate("tasks", "this_template_does_not_exist")

    def test_repr(self) -> None:
        template = PromptTemplate("system", "agent")
        assert "system/agent.txt" in repr(template)
