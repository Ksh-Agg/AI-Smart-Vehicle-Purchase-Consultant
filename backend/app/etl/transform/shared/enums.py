"""Enum normalization utility."""

import re
from enum import Enum
from typing import Any, Type, TypeVar

from app.etl.exceptions import TransformationError

T = TypeVar("T", bound=Enum)


def normalize_enum(value: Any, enum_class: Type[T]) -> T | None:
    """Standardizes string values to match project-specific enums.

    Args:
        value: Raw input value (typically string).
        enum_class: Target Enum class to map to.

    Returns:
        The matched Enum instance, or None if the input value was empty/None.

    Raises:
        TransformationError: If the value cannot be parsed to any enum member.
    """
    if value is None:
        return None

    val_str = str(value).strip().upper()
    if not val_str:
        return None

    # Strip punctuation and standard whitespace for matching
    cleaned = re.sub(r"[\s\.\-_]", "", val_str)

    # Dictionary containing common variations to canonical names
    custom_mappings: dict[str, str] = {
        # Drivetrain mappings
        "4WD": "4WD",
        "4X4": "4WD",
        "FOURWD": "4WD",
        "FOURWHEELDRIVE": "4WD",
        "FRONTWHEELDRIVE": "FWD",
        "REARWHEELDRIVE": "RWD",
        "ALLWHEELDRIVE": "AWD",
        # Fuel Type mappings
        "PETROLCNG": "CNG",
        "PLUGINHYBRID": "PLUGIN_HYBRID",
        "PHEV": "PLUGIN_HYBRID",
        "STRONGHYBRID": "HYBRID",
        "MILDHYBRID": "HYBRID",
        # Emission standard mappings
        "BSIV": "BS4",
        "BSVI": "BS6",
        "BS6PHASE2": "BS6_PHASE2",
        "BSVIPHASE2": "BS6_PHASE2",
        "BS62": "BS6_PHASE2",
    }

    # If it is inside custom mapping, use that target string
    lookup_val = custom_mappings.get(cleaned, cleaned)

    # First attempt: Match against Enum names
    for member in enum_class:
        if member.name == lookup_val:
            return member

    # Second attempt: Match against Enum values
    for member in enum_class:
        canonical_val = str(member.value).upper()
        # Clean both for strict comparison
        clean_canonical = re.sub(r"[\s\.\-_]", "", canonical_val)
        if clean_canonical == lookup_val or canonical_val == lookup_val:
            return member

    raise TransformationError(
        f"Value '{value}' could not be normalized to Enum '{enum_class.__name__}'. "
        f"Valid choices are: {[e.value for e in enum_class]}"
    )
