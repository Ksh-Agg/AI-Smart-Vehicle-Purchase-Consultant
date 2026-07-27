"""Dispatcher utility to normalize individual fields based on mapping rules."""

from decimal import Decimal
from typing import Any

from app.etl.transform.shared.booleans import normalize_bool
from app.etl.transform.shared.enums import normalize_enum
from app.etl.transform.shared.text import clean_text
from app.etl.transform.shared.rules import FIELD_RULES
from app.etl.transform.shared.units import convert_to_float, convert_to_int


def to_decimal(value: Any) -> Decimal | None:
    """Converts a value to Decimal for monetary integrity."""
    if value is None:
        return None
    try:
        cleaned = str(value).replace(",", "").replace("₹", "").strip()
        return Decimal(cleaned)
    except Exception:
        return None


def normalize_field(category: str, field: str, value: Any) -> Any:
    """Dispatches a single field value to its respective normalizer/converter rule.

    If no rule matches or the field is not registered, returns the value untouched.
    """
    category_rules = FIELD_RULES.get(category)
    if not category_rules:
        return value

    field_rule = category_rules.get(field)
    if not field_rule:
        return value

    rule_type, param = field_rule

    if value is None:
        return None

    if rule_type == "text":
        return (
            clean_text(value) or param
        )  # param can be a default fallback (e.g. 'Unknown')

    if rule_type == "int":
        return convert_to_int(value)

    if rule_type == "float":
        return convert_to_float(value)

    if rule_type == "decimal":
        return to_decimal(value)

    if rule_type == "bool":
        return normalize_bool(value)

    if rule_type == "enum" and param is not None:
        # param is the target Enum class
        return normalize_enum(value, param)

    return value
