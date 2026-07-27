"""ETL Validation Pipeline orchestrator."""

from typing import Any, Iterable

from pydantic import ValidationError

from app.etl.context import ETLContext
from app.etl.models import (
    CanonicalBrand,
    CanonicalVehicle,
    CanonicalEngineSpec,
    CanonicalDimensionSpec,
    CanonicalSafetySpec,
    CanonicalFeatureSpec,
    CanonicalOwnershipSpec,
    CanonicalAvailabilitySpec,
    CanonicalEnvironmentalSpec,
    CanonicalVehicleDataset,
)
from app.etl.validators.duplicates import DuplicateDetector
from app.etl.validators.enums import validate_enums
from app.etl.validators.foreign_keys import validate_foreign_keys
from app.etl.validators.models import ValidationReport
from app.etl.validators.numeric import validate_numeric_ranges
from app.etl.validators.required import validate_required_fields


class ValidationPipeline:
    """Orchestrates Stage 1 (Pydantic type checks) and Stage 2 (Business rule assertions)."""

    def __init__(self, context: ETLContext) -> None:
        self.context = context
        self.duplicate_detector = DuplicateDetector()

    def validate_batch(
        self, raw_mapped_records: Iterable[dict[str, dict[str, Any]]]
    ) -> tuple[list[CanonicalVehicleDataset], ValidationReport]:
        """Validates a batch of mapped records.

        Stage 1: Attempt to instantiate CanonicalVehicleDataset. If it fails, log as a Validation Report error.
        Stage 2: Run all semantic constraints, numeric ranges, and duplicate checks.

        Returns:
            A tuple containing:
              - A list of successfully validated CanonicalVehicleDataset objects.
              - A combined ValidationReport containing all validation failures.
        """
        valid_datasets: list[CanonicalVehicleDataset] = []
        report = ValidationReport()
        self.duplicate_detector.clear()

        for idx, mapped_record in enumerate(raw_mapped_records, start=1):
            self.context.metrics.inc_validated()

            # --- Stage 1: Pydantic Validation ---
            try:
                # Instantiate nested Pydantic models explicitly for mypy safety
                brand = CanonicalBrand(**mapped_record.get("brand", {}))
                vehicle = CanonicalVehicle(**mapped_record.get("vehicle", {}))
                engine_spec = CanonicalEngineSpec(
                    **mapped_record.get("engine_spec", {})
                )
                dimension_spec = CanonicalDimensionSpec(
                    **mapped_record.get("dimension_spec", {})
                )
                safety_spec = CanonicalSafetySpec(
                    **mapped_record.get("safety_spec", {})
                )
                feature_spec = CanonicalFeatureSpec(
                    **mapped_record.get("feature_spec", {})
                )
                ownership_spec = CanonicalOwnershipSpec(
                    **mapped_record.get("ownership_spec", {})
                )
                availability_spec = CanonicalAvailabilitySpec(
                    **mapped_record.get("availability_spec", {})
                )
                environmental_spec = CanonicalEnvironmentalSpec(
                    **mapped_record.get("environmental_spec", {})
                )

                # Instantiate root dataset model
                dataset = CanonicalVehicleDataset(
                    brand=brand,
                    vehicle=vehicle,
                    engine_spec=engine_spec,
                    dimension_spec=dimension_spec,
                    safety_spec=safety_spec,
                    feature_spec=feature_spec,
                    ownership_spec=ownership_spec,
                    availability_spec=availability_spec,
                    environmental_spec=environmental_spec,
                )
            except ValidationError as ve:
                self.context.metrics.inc_rejected()
                # Unpack Pydantic errors into structured report
                for error in ve.errors():
                    field_loc = " -> ".join(str(loc) for loc in error["loc"])
                    report.add_error(
                        row_index=idx,
                        field=field_loc,
                        error_type=error["type"],
                        message=error["msg"],
                    )
                continue

            # --- Stage 2: Business rule Validation ---
            # Create a separate row-level report to track issues in this record
            row_report = ValidationReport()
            validate_required_fields(dataset, idx, row_report)
            validate_numeric_ranges(dataset, idx, row_report)
            validate_enums(dataset, idx, row_report)
            validate_foreign_keys(dataset, idx, row_report)
            self.duplicate_detector.validate_duplicates(dataset, idx, row_report)

            if row_report.is_valid:
                valid_datasets.append(dataset)
            else:
                self.context.metrics.inc_rejected()
                # Merge row-level errors into the batch report
                report.errors.extend(row_report.errors)

        return valid_datasets, report
