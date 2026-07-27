"""JSON File Extractor."""

import json
from pathlib import Path
from typing import Any, Iterable
import pandas as pd  # type: ignore[import-untyped]

from app.etl.exceptions import ExtractionError
from app.etl.extract.base import BaseExtractor


class JSONExtractor(BaseExtractor):
    """Concrete extractor to read data from JSON files."""

    def extract(self, file_path: str | Path) -> Iterable[dict[str, Any]]:
        path = Path(file_path)
        if not path.exists():
            raise ExtractionError(f"JSON file not found: {path}")

        try:
            # We can use pandas to handle nesting or standard JSON parsing
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, dict):
                # If it's a single dictionary containing a list
                for key, val in data.items():
                    if isinstance(val, list):
                        data = val
                        break

            if not isinstance(data, list):
                raise ExtractionError(
                    f"JSON file at {path} must contain a list of records."
                )

            df = pd.DataFrame(data)
            df = df.where(pd.notnull(df), None)

            for _, row in df.iterrows():
                yield row.to_dict()
        except Exception as e:
            raise ExtractionError(f"Failed to extract JSON from {path}: {e}") from e
