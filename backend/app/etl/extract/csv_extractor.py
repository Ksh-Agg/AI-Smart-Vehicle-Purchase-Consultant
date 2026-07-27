"""CSV File Extractor."""

from pathlib import Path
from typing import Any, Iterable
import pandas as pd  # type: ignore[import-untyped]

from app.etl.exceptions import ExtractionError
from app.etl.extract.base import BaseExtractor


class CSVExtractor(BaseExtractor):
    """Concrete extractor to read data from CSV files."""

    def extract(self, file_path: str | Path) -> Iterable[dict[str, Any]]:
        path = Path(file_path)
        if not path.exists():
            raise ExtractionError(f"CSV file not found: {path}")

        try:
            # Load CSV using pandas
            df = pd.read_csv(path)
            # Replace NaN values with None for clean model mapping
            df = df.where(pd.notnull(df), None)

            # Yield records as dicts
            for _, row in df.iterrows():
                yield row.to_dict()
        except Exception as e:
            raise ExtractionError(f"Failed to extract CSV from {path}: {e}") from e
