"""
Cookiecutter pre-generation hook.

Runs before the project is generated. Validates user inputs and aborts
with a clear message if anything is invalid.
"""

import re
import sys


def validate_project_slug(slug: str) -> None:
    """
    Ensure project_slug is a valid Python package name.

    Rules:
        - Starts with a lowercase letter
        - Contains only lowercase letters, digits, and underscores
        - At least 2 characters long
    """
    pattern = r"^[a-z][a-z0-9_]+$"
    if not re.match(pattern, slug):
        print(
            f"\nERROR: project_slug '{slug}' is not valid.\n"
            "  - Must start with a lowercase letter\n"
            "  - May only contain lowercase letters, digits, and underscores\n"
            "  - Must be at least 2 characters long\n"
            "  - Example: my_agent_project\n"
        )
        sys.exit(1)


def validate_author_email(email: str) -> None:
    """
    Ensure author_email has a minimally valid format.

    Uses a simple pattern sufficient for catching obvious mistakes.
    Does not attempt full RFC 5322 validation.
    """
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    if not re.match(pattern, email):
        print(
            f"\nERROR: author_email '{email}' does not look like a valid email address.\n"
            "  - Expected format: user@domain.tld\n"
            "  - Example: mario@example.com\n"
        )
        sys.exit(1)


if __name__ == "__main__":
    project_slug = "{{ cookiecutter.project_slug }}"
    author_email = "{{ cookiecutter.author_email }}"

    validate_project_slug(project_slug)
    validate_author_email(author_email)
