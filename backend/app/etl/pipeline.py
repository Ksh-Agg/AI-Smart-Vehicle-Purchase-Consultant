"""ETL Pipeline orchestrator."""

from pathlib import Path
from typing import Any

from app.db.session import SessionLocal
from app.etl.context import ETLContext
from app.etl.exceptions import ExtractionError, MappingError
from app.etl.extract.base import BaseExtractor
from app.etl.mapping.registry import mapping_registry
from app.etl.transform.base import DefaultTransformer
from app.etl.validators.pipeline import ValidationPipeline
from app.etl.load.orchestrator import LoaderOrchestrator
from app.etl.models.dataset import CanonicalVehicleDataset
from app.etl.utils.timer import ExecutionTimer


class ETLPipeline:
    """Manages the full ETL execution flow: Extract -> Map -> Transform -> Validate -> Load."""

    def __init__(
        self,
        source_name: str,
        extractor: BaseExtractor,
        batch_size: int | None = None,
    ) -> None:
        self.source_name = source_name
        self.extractor = extractor
        self.context = ETLContext(source_name=source_name, batch_size=batch_size)
        self.transformer = DefaultTransformer()
        self.validator_pipeline = ValidationPipeline(self.context)
        self.loader_orchestrator = LoaderOrchestrator(self.context)

    def run(self, file_path: str | Path) -> dict[str, Any]:
        """Runs the complete ETL pipeline process on the input file.

        Extracts raw data, maps and standardizes it, validates against constraints,
        and saves valid records to PostgreSQL in batched transactions.

        Returns:
            A summary report dictionary detailing elapsed time and record processing metrics.
        """
        self.context.logger.info(
            f"Starting ETL pipeline execution for source: '{self.source_name}'"
        )
        self.context.logger.info(f"Input file path: {file_path}")

        try:
            # 1. Retrieve the mapping config for this source
            mapping_config = mapping_registry.get(self.source_name)
        except MappingError as me:
            self.context.logger.error(f"Configuration mapping failure: {me}")
            raise me

        try:
            # 2. Extract raw records
            with ExecutionTimer("Extraction") as timer:
                raw_records = list(self.extractor.extract(file_path))
            self.context.metrics.inc_extracted(len(raw_records))
            self.context.logger.info(
                f"Extracted {len(raw_records)} records in {timer.elapsed:.4f} seconds."
            )
        except ExtractionError as ee:
            self.context.logger.error(f"Extraction failed: {ee}")
            raise ee

        # 3. Map & Transform raw records
        mapped_and_normalized = []
        with ExecutionTimer("Transformation & Normalization") as timer:
            for raw_rec in raw_records:
                try:
                    # Flat source Dict -> Grouped dict (brand, vehicle, specs)
                    mapped_rec = mapping_config.map_record(raw_rec)

                    # Run text, numeric and enum normalization helpers
                    normalized_rec = self.transformer.transform(mapped_rec)

                    mapped_and_normalized.append(normalized_rec)
                    self.context.metrics.inc_transformed()
                except Exception as te:
                    self.context.logger.warning(
                        f"Transform failed for a raw record: {te}. Skipping record."
                    )
                    self.context.metrics.inc_rejected()

        self.context.logger.info(
            f"Transformed {len(mapped_and_normalized)} records in {timer.elapsed:.4f} seconds."
        )

        # 4. Validate records
        with ExecutionTimer("Validation Pipeline") as timer:
            valid_datasets, validation_report = self.validator_pipeline.validate_batch(
                mapped_and_normalized
            )

        if not validation_report.is_valid:
            self.context.logger.warning(
                f"Validation detected {len(validation_report.errors)} failures in batch."
            )
            for err in validation_report.errors[:10]:  # Log first 10 validation issues
                self.context.logger.warning(
                    f"Row {err.row_index} | Field: '{err.field}' | "
                    f"Error: {err.error_type} | Message: {err.message}"
                )
            if len(validation_report.errors) > 10:
                self.context.logger.warning(
                    f"... and {len(validation_report.errors) - 10} more validation failures."
                )

        self.context.logger.info(
            f"Validated records. Valid count: {len(valid_datasets)}. "
            f"Validation took {timer.elapsed:.4f} seconds."
        )

        # 5. Database Load
        if valid_datasets:
            with ExecutionTimer("Database Loading") as timer:
                self._load_records(valid_datasets)
            self.context.logger.info(
                f"Loading complete. Duration: {timer.elapsed:.4f} seconds."
            )
        else:
            self.context.logger.warning(
                "No valid records found in batch. Database load skipped."
            )

        # Stop total metrics execution timer
        self.context.metrics.stop_timer()
        report = self.context.metrics.get_report()

        self.context.logger.info("ETL pipeline execution completed successfully.")
        self.context.logger.info(f"Execution report: {report}")

        return report

    def _load_records(self, valid_datasets: list[CanonicalVehicleDataset]) -> None:
        """Helper to orchestrate loading valid canonical records into the DB in batches."""
        # Process in batches using session context
        batch_size = self.context.batch_size
        total_records = len(valid_datasets)

        for i in range(0, total_records, batch_size):
            chunk = valid_datasets[i : i + batch_size]
            self.context.logger.info(
                f"Loading batch chunk: {i // batch_size + 1} "
                f"({len(chunk)} records, offset={i})..."
            )
            # Create a clean session context per batch chunk
            with SessionLocal() as session:
                try:
                    with session.begin():
                        self.loader_orchestrator.load_batch(session, chunk)
                except Exception as le:
                    self.context.logger.error(
                        f"Database load chunk failure (offset={i}): {le}"
                    )
                    # We raise custom LoadingError if batch loader crashes
                    raise le
