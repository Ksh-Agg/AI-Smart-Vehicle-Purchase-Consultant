"""Dimension specification ORM model."""

from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.db.models.vehicle import Vehicle


class DimensionSpec(Base, TimestampMixin):
    """DimensionSpec model representing vehicle physical dimensions."""

    __tablename__ = "dimension_specs"

    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicles.id", ondelete="CASCADE"), primary_key=True
    )
    length_mm: Mapped[int | None] = mapped_column(Integer, nullable=True)
    width_mm: Mapped[int | None] = mapped_column(Integer, nullable=True)
    height_mm: Mapped[int | None] = mapped_column(Integer, nullable=True)
    wheelbase_mm: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ground_clearance_mm: Mapped[int | None] = mapped_column(Integer, nullable=True)
    boot_space_l: Mapped[int | None] = mapped_column(Integer, nullable=True)
    kerb_weight_kg: Mapped[int | None] = mapped_column(Integer, nullable=True)
    turning_radius_m: Mapped[float | None] = mapped_column(Float, nullable=True)

    __table_args__ = (
        CheckConstraint(
            "kerb_weight_kg IS NULL OR kerb_weight_kg > 0",
            name="chk_dimension_specs_kerb_weight_positive",
        ),
        CheckConstraint(
            "turning_radius_m IS NULL OR turning_radius_m > 0",
            name="chk_dimension_specs_turning_radius_positive",
        ),
    )

    # Relationships
    vehicle: Mapped["Vehicle"] = relationship(
        "Vehicle",
        back_populates="dimension_spec",
        lazy="selectin",
        uselist=False,
    )

    def __repr__(self) -> str:
        return (
            f"<DimensionSpec(vehicle_id={self.vehicle_id}, "
            f"length_mm={self.length_mm}, width_mm={self.width_mm})>"
        )
