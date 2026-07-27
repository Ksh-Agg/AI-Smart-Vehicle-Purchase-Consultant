"""Boolean normalization utility."""

from typing import Any


def normalize_bool(value: Any) -> bool | None:
    """Standardizes input values to boolean values."""
    if value is None:
        return None

    if isinstance(value, bool):
        return value

    val_str = str(value).strip().upper()
    if val_str in ("YES", "TRUE", "1", "Y", "T"):
        return True
    if val_str in ("NO", "FALSE", "0", "N", "F"):
        return False

    return None
