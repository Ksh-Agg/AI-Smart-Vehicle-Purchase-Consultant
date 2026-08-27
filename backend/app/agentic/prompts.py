"""Load agent prompts from the adjacent YAML file."""

from functools import lru_cache
from pathlib import Path
from string import Template

import yaml

PROMPT_FILE = Path(__file__).with_name("prompts.yaml")
REQUIRED_PROMPTS = {
    "intake.system",
    "sql_agent.system",
    "rag_agent.system",
    "web_agent.system",
    "synthesis.system",
}


@lru_cache(maxsize=1)
def _prompts() -> dict[str, str]:
    raw = yaml.safe_load(PROMPT_FILE.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise RuntimeError("prompts.yaml must contain a key/value mapping")
    missing = REQUIRED_PROMPTS - raw.keys()
    if missing:
        raise RuntimeError(f"Missing prompts: {', '.join(sorted(missing))}")
    return {key: str(value).strip() for key, value in raw.items()}


def prompt(name: str, **values: object) -> str:
    """Return one prompt, substituting only explicit runtime values."""
    return Template(_prompts()[name]).safe_substitute(values)
