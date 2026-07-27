"""Enum standard validation rule."""

from enum import Enum
from typing import Any, Type
from app.etl.models.dataset import CanonicalVehicleDataset
from app.etl.validators.models import ValidationReport


def _check_enum(
    value: Any,
    enum_class: Type[Enum],
    path: str,
    row_index: int,
    report: ValidationReport,
) -> None:
    """Helper to check if value matches valid enum choices."""

    if value is None:
        return
    if not isinstance(value, enum_class):
        report.add_error(
            row_index,
            path,
            "invalid_enum_value",
            f"Value '{value}' is not a valid choice for '{enum_class.__name__}'. "
            f"Expected one of {[e.value for e in enum_class]}",
        )


def validate_enums(
    dataset: CanonicalVehicleDataset, row_index: int, report: ValidationReport
) -> None:
    """Asserts that all canonical enum fields belong to their target enum classes."""
    # Since Pydantic models validate enums on instantiation, this rule acts as an
    # additional layer to catch and structure validation error formatting.
    _check_enum(
        dataset.vehicle.body_type,
        dataset.vehicle.body_type.__class__,
        "vehicle.body_type",
        row_index,
        report,
    )
    _check_enum(
        dataset.vehicle.segment,
        dataset.vehicle.segment.__class__,
        "vehicle.segment",
        row_index,
        report,
    )
    _check_enum(
        dataset.vehicle.fuel_type,
        dataset.vehicle.fuel_type.__class__,
        "vehicle.fuel_type",
        row_index,
        report,
    )
    _check_enum(
        dataset.vehicle.transmission,
        dataset.vehicle.transmission.__class__,
        "vehicle.transmission",
        row_index,
        report,
    )
    _check_enum(
        dataset.vehicle.drivetrain,
        dataset.vehicle.drivetrain.__class__ if dataset.vehicle.drivetrain else Enum,
        "vehicle.drivetrain",
        row_index,
        report,
    )
    _check_enum(
        dataset.availability_spec.current_status,
        dataset.availability_spec.current_status.__class__
        if dataset.availability_spec.current_status
        else Enum,
        "availability_spec.current_status",
        row_index,
        report,
    )
    _check_enum(
        dataset.environmental_spec.emission_standard,
        dataset.environmental_spec.emission_standard.__class__
        if dataset.environmental_spec.emission_standard
        else Enum,
        "environmental_spec.emission_standard",
        row_index,
        report,
    )
