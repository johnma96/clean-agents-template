"""
Cookiecutter post-generation hook.

Runs after the project is generated. Responsibilities:
    1. Remove conditional directories based on user choices
    2. Initialize a git repository
    3. Run `uv sync` if uv is available
    4. Print a welcome message with next steps

All steps are handled gracefully — a failure in one step never silently
swallows the error, but also never aborts the remaining steps.
"""

import os
import shutil
import subprocess
import sys


# ── Helpers ──────────────────────────────────────────────────────────────────

def remove_dir(path: str) -> None:
    """Remove a directory tree if it exists, with a clear log message."""
    if os.path.exists(path):
        shutil.rmtree(path)
        print(f"  [removed]  {path}")
    else:
        print(f"  [skipped]  {path} (not found — nothing to remove)")


def run(cmd: list[str], description: str) -> bool:
    """
    Run a subprocess command and return True on success.

    Prints a clear message whether the command succeeded or failed.
    Never raises — all exceptions are caught and reported.
    """
    try:
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
        )
        print(f"  [ok]  {description}")
        if result.stdout.strip():
            # Indent stdout so it reads as subordinate to the step
            for line in result.stdout.strip().splitlines():
                print(f"        {line}")
        return True
    except FileNotFoundError:
        print(f"  [skip]  {description} — command not found: {cmd[0]}")
        return False
    except subprocess.CalledProcessError as exc:
        print(f"  [fail]  {description}")
        if exc.stderr.strip():
            for line in exc.stderr.strip().splitlines():
                print(f"        {line}")
        return False
    except Exception as exc:  # noqa: BLE001
        print(f"  [fail]  {description} — unexpected error: {exc}")
        return False


# ── Step 1: Remove conditional directories ───────────────────────────────────

def remove_conditional_dirs() -> None:
    print("\n── Conditional directories ──")

    include_api: str = "{{ cookiecutter.include_api }}"
    include_monitoring: str = "{{ cookiecutter.include_monitoring }}"
    include_mcp: str = "{{ cookiecutter.include_mcp }}"

    project_slug: str = "{{ cookiecutter.project_slug }}"
    infra_root = os.path.join("src", project_slug, "infrastructure")

    if include_api == "no":
        remove_dir(os.path.join(infra_root, "api"))

    if include_monitoring == "no":
        remove_dir(os.path.join(infra_root, "monitoring"))

    if include_mcp == "no":
        remove_dir(os.path.join(infra_root, "mcp"))

    if all(v == "yes" for v in [include_api, include_monitoring, include_mcp]):
        print("  [ok]  all optional directories retained")


# ── Step 2: Git init ──────────────────────────────────────────────────────────

def git_init() -> None:
    print("\n── Git ──")
    run(["git", "init"], "git init")


# ── Step 3: uv sync ───────────────────────────────────────────────────────────

def uv_sync() -> None:
    print("\n── Python environment ──")
    uv_available = shutil.which("uv") is not None
    if uv_available:
        run(["uv", "sync"], "uv sync")
    else:
        print("  [skip]  uv sync — uv not found on PATH")
        print("          Install uv: https://docs.astral.sh/uv/getting-started/installation/")
        print("          Then run: uv sync")


# ── Step 4: Welcome message ───────────────────────────────────────────────────

def print_welcome() -> None:
    project_name: str = "{{ cookiecutter.project_name }}"
    project_slug: str = "{{ cookiecutter.project_slug }}"
    include_api: str = "{{ cookiecutter.include_api }}"
    include_monitoring: str = "{{ cookiecutter.include_monitoring }}"
    include_mcp: str = "{{ cookiecutter.include_mcp }}"

    optional_notes = []
    if include_api == "yes":
        optional_notes.append("  - API layer included → implement your HTTP entry point in infrastructure/api/")
    if include_monitoring == "yes":
        optional_notes.append("  - Monitoring included → implement your tracer in infrastructure/monitoring/tracer.py")
    if include_mcp == "yes":
        optional_notes.append("  - MCP client included → implement your MCP connection in infrastructure/mcp/mcp_client.py")

    optional_block = "\n".join(optional_notes) if optional_notes else "  (no optional layers selected)"

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║   {project_name:<58}║
╚══════════════════════════════════════════════════════════════╝

Project generated at: ./{project_slug}/

Optional layers selected:
{optional_block}

Next steps:
  1. cd {project_slug}
  2. Review src/{project_slug}/domain/interfaces.py
     → Define the Protocols your infrastructure must implement
  3. Review src/{project_slug}/domain/models.py
     → Define your core business entities (Pydantic v2)
  4. Implement infrastructure/ providers
     → Each file has a detailed docstring explaining what to implement
  5. Install your chosen dependencies:
     uv add <your-llm-sdk> <your-vector-store> ...
  6. Run tests:
     make test        # unit tests only (fast, no IO)
     make test-all    # unit + integration

Architecture rule to keep in mind:
  infrastructure → application → domain   (never the reverse)

Read CLAUDE.md for the full architecture guide and anti-patterns.
""")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    try:
        remove_conditional_dirs()
        git_init()
        uv_sync()
        print_welcome()
    except Exception as exc:  # noqa: BLE001
        # Last-resort catch so cookiecutter always sees a clean exit.
        # Individual steps already handle their own errors above.
        print(f"\n[post_gen_project] Unexpected error: {exc}", file=sys.stderr)
        sys.exit(1)
