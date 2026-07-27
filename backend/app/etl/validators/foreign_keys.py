"""Foreign key and structural validation rule."""

from app.etl.models.dataset import CanonicalVehicleDataset
from app.etl.validators.models import ValidationReport


def validate_foreign_keys(
    dataset: CanonicalVehicleDataset, row_index: int, report: ValidationReport
) -> None:
    """Performs integrity checks on related structures (e.g. brand names)."""
    # Verify that the linked brand has a non-empty name
    if not dataset.brand.name.strip():
        report.add_error(
            row_index=row_index,
            field="vehicle.brand_id",
            error_type="missing_foreign_key",
            message="Associated brand name is empty.",
        )
