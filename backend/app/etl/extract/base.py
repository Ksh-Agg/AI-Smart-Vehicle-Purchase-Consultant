"""Base extractor interface."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Iterable


class BaseExtractor(ABC):
    """Abstract base class for all raw file extractors."""

    @abstractmethod
    def extract(self, file_path: str | Path) -> Iterable[dict[str, Any]]:
        """Reads a raw data source and yields records as dictionaries.

        Args:
            file_path: Absolute or relative path to the raw data file.

        Yields:
            Dict representing a single row/record.
        """
        pass
