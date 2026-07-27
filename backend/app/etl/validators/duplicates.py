"""Duplicate detection validator rule."""

from app.etl.models.dataset import CanonicalVehicleDataset
from app.etl.validators.models import ValidationReport


class DuplicateDetector:
    """Tracks composite vehicle keys across a batch to identify duplicates."""

    def __init__(self) -> None:
        # Set of (brand_name, model, variant, year)
        self._seen_keys: set[tuple[str, str, str, int]] = set()

    def validate_duplicates(
        self, dataset: CanonicalVehicleDataset, row_index: int, report: ValidationReport
    ) -> None:
        """Checks if a vehicle with the same brand, model, variant, and year is duplicated in the batch."""
        brand_name = dataset.brand.name.strip().upper()
        model = dataset.vehicle.model.strip().upper()
        variant = dataset.vehicle.variant.strip().upper()
        year = dataset.vehicle.year

        composite_key = (brand_name, model, variant, year)

        if composite_key in self._seen_keys:
            report.add_error(
                row_index=row_index,
                field="vehicle.model+variant+year",
                error_type="duplicate_record",
                message=f"Duplicate vehicle variant found in batch: "
                f"'{dataset.brand.name} {dataset.vehicle.model} {dataset.vehicle.variant} ({year})'.",
            )
        else:
            self._seen_keys.add(composite_key)

    def clear(self) -> None:
        """Resets the detector's cache."""
        self._seen_keys.clear()
