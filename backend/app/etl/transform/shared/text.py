"""Text cleanup and normalization utilities."""

import re
from typing import Any


def clean_text(value: Any) -> str | None:
    """Cleans a text string by stripping outer whitespace and normalizing inner spaces."""
    if value is None:
        return None

    val_str = str(value).strip()
    if not val_str:
        return None

    # Normalize multiple whitespace characters to a single space
    val_str = re.sub(r"\s+", " ", val_str)
    return val_str


def clean_alphanumeric(value: Any) -> str | None:
    """Retains only alphanumeric characters, spaces, and hyphens."""
    cleaned = clean_text(value)
    if cleaned is None:
        return None

    # Remove special characters except alphanumeric, space, and hyphen
    return re.sub(r"[^\w\s\-]", "", cleaned).strip()
