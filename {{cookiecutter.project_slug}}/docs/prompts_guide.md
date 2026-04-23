# Prompt Management Guide

## Where prompts live

All prompts are in `src/{{ cookiecutter.project_slug }}/domain/prompts/`:

```
domain/prompts/
├── __init__.py        ← PromptTemplate class (stdlib str.format())
├── system/            ← Agent persona and behavior prompts
│   └── agent.txt
└── tasks/             ← Task-specific prompts (extraction, summarization, etc.)
    └── example_task.txt
```

## How to load a prompt

```python
from {{ cookiecutter.project_slug }}.domain.prompts import PromptTemplate

template = PromptTemplate("tasks", "example_task")
rendered = template.render(
    task_name="extraction",
    context="...",
    user_input="...",
    instructions="...",
)
```

## How to add a new prompt

1. Create a `.txt` file in the appropriate subdirectory
2. Use `{variable_name}` for dynamic content (Python `str.format()` syntax)
3. Load it with `PromptTemplate("category", "name")`
4. Add a test in `tests/unit/domain/test_prompts.py`

## How to version prompts

Prompts are plain text files tracked in git. Use meaningful commit messages:

```
feat(prompts): add extraction prompt for pension documents
fix(prompts): improve citation instructions in system prompt
```

## Prompt engineering tips

- Keep system prompts focused on persona and constraints, not task details
- Put task-specific instructions in task prompts, not system prompts
- Use `{variable_name}` placeholders for dynamic content; avoid complex logic in templates
- Test prompts with representative inputs before committing
- Document the expected variables for each template in a comment at the top of the .txt file
