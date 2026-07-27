"""Database models package."""

from app.db.models.availability_spec import AvailabilitySpec
from app.db.models.brand import Brand
from app.db.models.dimension_spec import DimensionSpec
from app.db.models.engine_spec import EngineSpec
from app.db.models.enums import (
    BodyType,
    DrivetrainType,
    EmissionStandard,
    FuelType,
    SegmentType,
    TransmissionType,
    VehicleStatus,
)
from app.db.models.environmental_spec import EnvironmentalSpec
from app.db.models.feature_spec import FeatureSpec
from app.db.models.ownership_spec import OwnershipSpec
from app.db.models.safety_spec import SafetySpec
from app.db.models.vehicle import Vehicle

__all__ = [
    # Models
    "Brand",
    "Vehicle",
    "EngineSpec",
    "DimensionSpec",
    "SafetySpec",
    "FeatureSpec",
    "OwnershipSpec",
    "AvailabilitySpec",
    "EnvironmentalSpec",
    # Enums
    "BodyType",
    "DrivetrainType",
    "EmissionStandard",
    "FuelType",
    "SegmentType",
    "TransmissionType",
    "VehicleStatus",
]
