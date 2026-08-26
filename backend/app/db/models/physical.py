"""Variant physical and chassis specifications."""

from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    ForeignKey,
    Integer,
    Numeric,
    SmallInteger,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class VariantPhysicalSpec(Base):
    """Canonical dimensions, chassis, wheels, and capacity facts."""

    __tablename__ = "variant_physical_specs"

    variant_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("variants.id", ondelete="CASCADE"), primary_key=True
    )
    chassis_type: Mapped[str | None] = mapped_column(Text)
    front_suspension: Mapped[str | None] = mapped_column(Text)
    rear_suspension: Mapped[str | None] = mapped_column(Text)
    length_mm: Mapped[int | None] = mapped_column(Integer)
    width_mm: Mapped[int | None] = mapped_column(Integer)
    height_mm: Mapped[int | None] = mapped_column(Integer)
    wheelbase_mm: Mapped[int | None] = mapped_column(Integer)
    ground_clearance_mm: Mapped[int | None] = mapped_column(Integer)
    kerb_weight_kg: Mapped[int | None] = mapped_column(Integer)
    bootspace_litres: Mapped[int | None] = mapped_column(Integer)
    seating_capacity: Mapped[int | None] = mapped_column(SmallInteger)
    number_of_rows: Mapped[int | None] = mapped_column(SmallInteger)
    fuel_tank_capacity_litres: Mapped[Decimal | None] = mapped_column(Numeric(6, 2))
    cng_cylinder_water_capacity_litres: Mapped[Decimal | None] = mapped_column(
        Numeric(6, 2)
    )
    number_of_doors: Mapped[int | None] = mapped_column(SmallInteger)
    wheel_type: Mapped[str | None] = mapped_column(Text)
    wheel_size_inches: Mapped[Decimal | None] = mapped_column(Numeric(4, 1))
    tyre_size: Mapped[str | None] = mapped_column(Text)
    spare_wheel: Mapped[bool | None] = mapped_column(Boolean)
    roof_rails: Mapped[bool | None] = mapped_column(Boolean)
    dual_tone_exterior: Mapped[bool | None] = mapped_column(Boolean)

    __table_args__ = (
        CheckConstraint(
            "(length_mm IS NULL OR length_mm > 0) AND "
            "(width_mm IS NULL OR width_mm > 0) AND "
            "(height_mm IS NULL OR height_mm > 0) AND "
            "(wheelbase_mm IS NULL OR wheelbase_mm > 0) AND "
            "(ground_clearance_mm IS NULL OR ground_clearance_mm > 0) AND "
            "(kerb_weight_kg IS NULL OR kerb_weight_kg > 0) AND "
            "(bootspace_litres IS NULL OR bootspace_litres > 0)",
            name="positive_dimensions",
        ),
        CheckConstraint(
            "seating_capacity IS NULL OR seating_capacity BETWEEN 1 AND 20",
            name="seating_capacity_range",
        ),
        CheckConstraint(
            "number_of_rows IS NULL OR number_of_rows BETWEEN 1 AND 5",
            name="row_count_range",
        ),
        CheckConstraint(
            "number_of_doors IS NULL OR number_of_doors BETWEEN 1 AND 10",
            name="door_count_range",
        ),
        CheckConstraint(
            "(fuel_tank_capacity_litres IS NULL OR fuel_tank_capacity_litres > 0) "
            "AND (cng_cylinder_water_capacity_litres IS NULL OR "
            "cng_cylinder_water_capacity_litres > 0) AND "
            "(wheel_size_inches IS NULL OR wheel_size_inches > 0)",
            name="positive_capacities",
        ),
    )
