"""Canonical Vehicle Dataset Model."""

from pydantic import BaseModel

from app.etl.models.brand import CanonicalBrand
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


class CanonicalVehicleDataset(BaseModel):
    """Aggregates all canonical entities representing a single vehicle variant and its specifications.

    This aggregate model is passed through mapping, transformation, validation,
    and loading stages of the ETL pipeline.
    """

    brand: CanonicalBrand
    vehicle: CanonicalVehicle
    engine_spec: CanonicalEngineSpec
    dimension_spec: CanonicalDimensionSpec
    safety_spec: CanonicalSafetySpec
    feature_spec: CanonicalFeatureSpec
    ownership_spec: CanonicalOwnershipSpec
    availability_spec: CanonicalAvailabilitySpec
    environmental_spec: CanonicalEnvironmentalSpec

    class Config:
        frozen = True
