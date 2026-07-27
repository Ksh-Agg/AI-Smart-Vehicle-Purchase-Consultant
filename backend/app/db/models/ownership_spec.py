"""Ownership specification ORM model."""

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.db.models.vehicle import Vehicle


class OwnershipSpec(Base, TimestampMixin):
    """OwnershipSpec model representing warranty and service specifications."""

    __tablename__ = "ownership_specs"

    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicles.id", ondelete="CASCADE"), primary_key=True
    )
    warranty_years: Mapped[int | None] = mapped_column(Integer, nullable=True)
    warranty_km: Mapped[int | None] = mapped_column(Integer, nullable=True)
    extended_warranty_available: Mapped[bool | None] = mapped_column(
        Boolean, nullable=True
    )
    service_interval_km: Mapped[int | None] = mapped_column(Integer, nullable=True)
    roadside_assistance: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    estimated_service_cost_per_year: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2), nullable=True
    )

    __table_args__ = (
        CheckConstraint(
            "warranty_years IS NULL OR warranty_years > 0",
            name="chk_ownership_specs_warranty_years_positive",
        ),
        CheckConstraint(
            "warranty_km IS NULL OR warranty_km > 0",
            name="chk_ownership_specs_warranty_km_positive",
        ),
        CheckConstraint(
            "service_interval_km IS NULL OR service_interval_km > 0",
            name="chk_ownership_specs_service_interval_positive",
        ),
        CheckConstraint(
            "estimated_service_cost_per_year IS NULL OR estimated_service_cost_per_year >= 0",
            name="chk_ownership_specs_service_cost_non_negative",
        ),
    )

    # Relationships
    vehicle: Mapped["Vehicle"] = relationship(
        "Vehicle",
        back_populates="ownership_spec",
        lazy="selectin",
        uselist=False,
    )

    def __repr__(self) -> str:
        return (
            f"<OwnershipSpec(vehicle_id={self.vehicle_id}, "
            f"warranty_years={self.warranty_years})>"
        )
