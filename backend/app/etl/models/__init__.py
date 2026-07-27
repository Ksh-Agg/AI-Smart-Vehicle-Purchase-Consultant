"""ETL Canonical Pydantic Models Package."""

from app.etl.models.brand import CanonicalBrand
from app.etl.models.dataset import CanonicalVehicleDataset
from app.etl.models.specs import (
    CanonicalAvailabilitySpec,
    CanonicalDimensionSpec,
    CanonicalEngineSpec,
    CanonicalEnvironmentalSpec,
    CanonicalFeatureSpec,
    CanonicalOwnershipSpec,
    CanonicalSafetySpec,
)
from app.etl.models.vehicle import CanonicalVehicle

__all__ = [
    "CanonicalBrand",
    "CanonicalVehicle",
    "CanonicalEngineSpec",
    "CanonicalDimensionSpec",
    "CanonicalSafetySpec",
    "CanonicalFeatureSpec",
    "CanonicalOwnershipSpec",
    "CanonicalAvailabilitySpec",
    "CanonicalEnvironmentalSpec",
    "CanonicalVehicleDataset",
]
