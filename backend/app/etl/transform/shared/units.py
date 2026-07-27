"""Unit conversion and numeric extraction utilities."""

import re
from typing import Any


def extract_numeric(value: Any) -> float | None:
    """Extracts the first numeric value found in a string or returns the value if already numeric.

    Handles commas (e.g. "1,25,000") and unit suffixes (e.g. "119.8 bhp @ 6000 rpm", "16.8 kmpl", "1497 cc").
    """
    if value is None:
        return None

    if isinstance(value, (int, float)):
        return float(value)

    val_str = str(value).strip()
    if not val_str:
        return None

    # Remove commas
    val_str = val_str.replace(",", "")

    # Regex search for first float/int in string (handles decimals)
    match = re.search(r"[-+]?\d*\.\d+|\d+", val_str)
    if match:
        return float(match.group())

    return None


def convert_to_float(value: Any) -> float | None:
    """Extracts and converts value to float."""
    return extract_numeric(value)


def convert_to_int(value: Any) -> int | None:
    """Extracts and converts value to integer."""
    num = extract_numeric(value)
    if num is None:
        return None
    return int(round(num))
