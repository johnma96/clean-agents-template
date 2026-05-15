"""Project path constants — single source of truth for all filesystem locations.

This is the ONLY file in the project that uses Path(__file__) to resolve paths.
All other modules that need filesystem paths must import constants from here.

Convention:
    Never use Path(__file__) outside this module. Import paths from here instead:

        from {{ cookiecutter.project_slug }}.paths import PROJECT_ROOT, DATA_DIR, PROMPTS_DIR
"""

from pathlib import Path

_PACKAGE_DIR = Path(__file__).resolve().parent  # src/{{ cookiecutter.project_slug }}/

PROJECT_ROOT = _PACKAGE_DIR.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
SAMPLES_DIR = DATA_DIR / "samples"
SCHEMAS_DIR = DATA_DIR / "schemas"
RAW_DIR = DATA_DIR / "raw"
CHROMA_DIR = DATA_DIR / "chroma"
STATIC_DIR = PROJECT_ROOT / "static"
PROMPTS_DIR = _PACKAGE_DIR / "domain" / "prompts"


def ensure_dirs() -> None:
    """Create all data directories if they don't exist.

    Call this once at application startup (e.g., in main.py or a script),
    not on every import.
    """
    for d in [SAMPLES_DIR, SCHEMAS_DIR, RAW_DIR, CHROMA_DIR]:
        d.mkdir(parents=True, exist_ok=True)
