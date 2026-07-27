"""Default values handler for missing attributes."""

from typing import Any


def apply_default_values(
    record: dict[str, dict[str, Any]], defaults_config: dict[str, Any]
) -> dict[str, dict[str, Any]]:
    """Applies default values to mapped categories based on the source config.

    Defaults are only applied if the target attribute is missing or None.
    """
    for target_path, default_val in defaults_config.items():
        if "." in target_path:
            category, field = target_path.split(".", 1)
            if category in record:
                if record[category].get(field) is None:
                    record[category][field] = default_val
        else:
            # Fallback to vehicle category
            if record["vehicle"].get(target_path) is None:
                record["vehicle"][target_path] = default_val

    return record
