"""Excel File Extractor."""

from pathlib import Path
from typing import Any, Iterable
import pandas as pd  # type: ignore[import-untyped]

from app.etl.exceptions import ExtractionError
from app.etl.extract.base import BaseExtractor


class ExcelExtractor(BaseExtractor):
    """Concrete extractor to read data from Excel files."""

    def extract(self, file_path: str | Path) -> Iterable[dict[str, Any]]:
        path = Path(file_path)
        if not path.exists():
            raise ExtractionError(f"Excel file not found: {path}")

        try:
            # Load Excel sheet using pandas
            df = pd.read_excel(path)
            df = df.where(pd.notnull(df), None)

            for _, row in df.iterrows():
                yield row.to_dict()
        except Exception as e:
            raise ExtractionError(f"Failed to extract Excel from {path}: {e}") from e
