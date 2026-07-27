"""Vehicle ORM model mapping vehicle entities."""

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    Enum,
    ForeignKey,
    Index,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.db.models.enums import (
    BodyType,
    DrivetrainType,
    FuelType,
    SegmentType,
    TransmissionType,
)

if TYPE_CHECKING:
    from app.db.models.availability_spec import AvailabilitySpec
    from app.db.models.brand import Brand
    from app.db.models.dimension_spec import DimensionSpec
    from app.db.models.engine_spec import EngineSpec
    from app.db.models.environmental_spec import EnvironmentalSpec
    from app.db.models.feature_spec import FeatureSpec
    from app.db.models.ownership_spec import OwnershipSpec
    from app.db.models.safety_spec import SafetySpec


class Vehicle(Base, TimestampMixin):
    """Vehicle model representing core vehicle variants and details."""

    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(primary_key=True)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    variant: Mapped[str] = mapped_column(String(100), nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)
    body_type: Mapped[BodyType] = mapped_column(
        Enum(BodyType, native_enum=True), nullable=False
    )
    segment: Mapped[SegmentType] = mapped_column(
        Enum(SegmentType, native_enum=True), nullable=False
    )
    fuel_type: Mapped[FuelType] = mapped_column(
        Enum(FuelType, native_enum=True), nullable=False
    )
    transmission: Mapped[TransmissionType] = mapped_column(
        Enum(TransmissionType, native_enum=True), nullable=False
    )
    drivetrain: Mapped[DrivetrainType | None] = mapped_column(
        Enum(DrivetrainType, native_enum=True), nullable=True
    )
    seating_capacity: Mapped[int] = mapped_column(nullable=False)
    doors: Mapped[int | None] = mapped_column(nullable=True)
    price_ex_showroom: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    price_on_road: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)

    # Relationships
    brand: Mapped["Brand"] = relationship(
        "Brand",
        back_populates="vehicles",
        lazy="selectin",
    )
    engine_spec: Mapped["EngineSpec"] = relationship(
        "EngineSpec",
        back_populates="vehicle",
        cascade="all, delete-orphan",
        lazy="selectin",
        uselist=False,
    )
    dimension_spec: Mapped["DimensionSpec"] = relationship(
        "DimensionSpec",
        back_populates="vehicle",
        cascade="all, delete-orphan",
        lazy="selectin",
        uselist=False,
    )
    safety_spec: Mapped["SafetySpec"] = relationship(
        "SafetySpec",
        back_populates="vehicle",
        cascade="all, delete-orphan",
        lazy="selectin",
        uselist=False,
    )
    feature_spec: Mapped["FeatureSpec"] = relationship(
        "FeatureSpec",
        back_populates="vehicle",
        cascade="all, delete-orphan",
        lazy="selectin",
        uselist=False,
    )
    ownership_spec: Mapped["OwnershipSpec"] = relationship(
        "OwnershipSpec",
        back_populates="vehicle",
        cascade="all, delete-orphan",
        lazy="selectin",
        uselist=False,
    )
    availability_spec: Mapped["AvailabilitySpec"] = relationship(
        "AvailabilitySpec",
        back_populates="vehicle",
        cascade="all, delete-orphan",
        lazy="selectin",
        uselist=False,
    )
    environmental_spec: Mapped["EnvironmentalSpec"] = relationship(
        "EnvironmentalSpec",
        back_populates="vehicle",
        cascade="all, delete-orphan",
        lazy="selectin",
        uselist=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "brand_id",
            "model",
            "variant",
            "year",
            name="uq_vehicles_brand_model_variant_year",
        ),
        CheckConstraint(
            "year >= 1990 AND year <= 2035", name="chk_vehicles_year_range"
        ),
        CheckConstraint(
            "seating_capacity >= 1 AND seating_capacity <= 10",
            name="chk_vehicles_seating_capacity",
        ),
        CheckConstraint(
            "doors IS NULL OR (doors >= 2 AND doors <= 6)",
            name="chk_vehicles_doors",
        ),
        CheckConstraint(
            "price_ex_showroom > 0",
            name="chk_vehicles_price_ex_showroom_positive",
        ),
        CheckConstraint(
            "price_on_road IS NULL OR price_on_road > 0",
            name="chk_vehicles_price_on_road_positive",
        ),
        Index("ix_vehicles_model", "model"),
        Index("ix_vehicles_price_ex_showroom", "price_ex_showroom"),
        Index("ix_vehicles_fuel_type", "fuel_type"),
        Index("ix_vehicles_transmission", "transmission"),
        Index("ix_vehicles_body_type", "body_type"),
        Index("ix_vehicles_segment", "segment"),
        Index("ix_vehicles_year", "year"),
        Index("ix_vehicles_seating_capacity", "seating_capacity"),
    )

    def __repr__(self) -> str:
        return (
            f"<Vehicle(id={self.id}, model={self.model!r}, variant={self.variant!r})>"
        )
