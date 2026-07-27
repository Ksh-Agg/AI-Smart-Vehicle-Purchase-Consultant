"""Canonical Vehicle Pydantic Model."""

from decimal import Decimal
from pydantic import BaseModel, Field

from app.db.models.enums import (
    BodyType,
    DrivetrainType,
    FuelType,
    SegmentType,
    TransmissionType,
)


class CanonicalVehicle(BaseModel):
    """Canonical model for Vehicle data matching the database schema."""

    model: str = Field(..., max_length=100)
    variant: str = Field(..., max_length=100)
    year: int
    body_type: BodyType
    segment: SegmentType
    fuel_type: FuelType
    transmission: TransmissionType
    drivetrain: DrivetrainType | None = None
    seating_capacity: int
    doors: int | None = None
    price_ex_showroom: Decimal = Field(..., gt=0)
    price_on_road: Decimal | None = None

    class Config:
        frozen = True
        use_enum_values = False
