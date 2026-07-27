"""Base and default transformer implementations."""

from abc import ABC, abstractmethod
from typing import Any

from app.etl.transform.shared.normalizer import normalize_field


class BaseTransformer(ABC):
    """Abstract base class for all data transformers."""

    @abstractmethod
    def transform(
        self, mapped_record: dict[str, dict[str, Any]]
    ) -> dict[str, dict[str, Any]]:
        """Takes mapped category dictionaries and normalizes their values.

        Args:
            mapped_record: Structured dictionaries representing raw mapped values.

        Returns:
            Normalized dictionary ready for Pydantic instantiation.
        """
        pass


class DefaultTransformer(BaseTransformer):
    """A generic, lightweight, and reusable transformer mapping raw fields to canonical types.

    Delegates all value cleaning and conversion to shared helper functions dynamically,
    preventing it from becoming a monolithic database schema-coupled class.
    """

    def transform(
        self, mapped_record: dict[str, dict[str, Any]]
    ) -> dict[str, dict[str, Any]]:
        """Applies generic conversions to normalize mapped records.

        Iterates over structured categories and delegates individual field cleanups to the normalizer dispatcher.
        """
        result: dict[str, dict[str, Any]] = {}

        for category, fields in mapped_record.items():
            result[category] = {}
            for field, val in fields.items():
                result[category][field] = normalize_field(category, field, val)

        return result
