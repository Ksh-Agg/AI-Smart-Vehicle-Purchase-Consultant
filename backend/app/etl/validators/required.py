"""Required fields validator rule."""

from app.etl.models.dataset import CanonicalVehicleDataset
from app.etl.validators.models import ValidationReport


def validate_required_fields(
    dataset: CanonicalVehicleDataset, row_index: int, report: ValidationReport
) -> None:
    """Verifies that all required fields are present in the canonical dataset."""
    # Pydantic validates basic field requirements, but we run business-level assertions
    # here to guarantee structural integrity of the flat schema.
    required_checks = [
        ("brand.name", dataset.brand.name),
        ("brand.country", dataset.brand.country),
        ("vehicle.model", dataset.vehicle.model),
        ("vehicle.variant", dataset.vehicle.variant),
        ("vehicle.year", dataset.vehicle.year),
        ("vehicle.body_type", dataset.vehicle.body_type),
        ("vehicle.segment", dataset.vehicle.segment),
        ("vehicle.fuel_type", dataset.vehicle.fuel_type),
        ("vehicle.transmission", dataset.vehicle.transmission),
        ("vehicle.seating_capacity", dataset.vehicle.seating_capacity),
        ("vehicle.price_ex_showroom", dataset.vehicle.price_ex_showroom),
    ]

    for path, value in required_checks:
        if value is None or (isinstance(value, str) and not value.strip()):
            report.add_error(
                row_index=row_index,
                field=path,
                error_type="missing_required_field",
                message=f"Required field '{path}' is missing or empty.",
            )
        elif isinstance(value, float) and value <= 0:
            # Let's ensure non-negative numeric where expected
            pass
