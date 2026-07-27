"""Loader orchestrator component."""

from sqlalchemy.orm import Session
from app.etl.context import ETLContext
from app.etl.exceptions import LoadingError
from app.etl.load.brand_loader import BrandLoader
from app.etl.load.specs_loader import SpecsLoader
from app.etl.load.vehicle_loader import VehicleLoader
from app.etl.models.dataset import CanonicalVehicleDataset


class LoaderOrchestrator:
    """Manages transaction scopes, batch sizes, commits, rollbacks, and record loaders."""

    def __init__(self, context: ETLContext) -> None:
        self.context = context
        self.brand_loader = BrandLoader()
        self.vehicle_loader = VehicleLoader()
        self.specs_loader = SpecsLoader()

    def load_batch(
        self, session: Session, datasets: list[CanonicalVehicleDataset]
    ) -> int:
        """Loads a batch of validated canonical records into the database.

        If any record in the batch fails to load, the transaction is rolled back
        and a LoadingError is raised.
        """
        loaded_count = 0
        try:
            for dataset in datasets:
                # 1. Load or resolve the Brand
                brand = self.brand_loader.get_or_create(session, dataset.brand)

                # 2. Load the Vehicle variant linked to resolved Brand ID
                vehicle, created = self.vehicle_loader.load_vehicle(
                    session, dataset.vehicle, brand.id
                )

                # 3. Load all child specifications linked to Vehicle ID
                self.specs_loader.load_specs(
                    session,
                    vehicle.id,
                    dataset.engine_spec,
                    dataset.dimension_spec,
                    dataset.safety_spec,
                    dataset.feature_spec,
                    dataset.ownership_spec,
                    dataset.availability_spec,
                    dataset.environmental_spec,
                )

                loaded_count += 1
                self.context.metrics.inc_loaded()

            # Flush all records in the batch to the database
            session.flush()
            self.context.logger.info(
                f"Successfully processed and flushed batch of {loaded_count} records."
            )

        except Exception as e:
            session.rollback()
            self.context.logger.error(
                f"Database load transaction failed. Rolled back the batch. Error: {e}"
            )
            # Subtract count of loaded items since the batch failed
            # We decrement the metrics counter accordingly
            self.context.metrics.loaded -= loaded_count
            self.context.metrics.inc_rejected(len(datasets))
            raise LoadingError(f"Database transaction load error: {e}") from e

        return loaded_count
