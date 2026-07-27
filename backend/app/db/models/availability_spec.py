"""Availability specification ORM model."""

from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Enum, ForeignKey, Integer
from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.db.models.enums import VehicleStatus

if TYPE_CHECKING:
    from app.db.models.vehicle import Vehicle


class AvailabilitySpec(Base, TimestampMixin):
    """AvailabilitySpec model representing vehicle market availability status."""

    __tablename__ = "availability_specs"

    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicles.id", ondelete="CASCADE"), primary_key=True
    )
    launch_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    current_status: Mapped[VehicleStatus | None] = mapped_column(
        Enum(VehicleStatus, native_enum=True), nullable=True
    )
    booking_open: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    waiting_period_weeks: Mapped[int | None] = mapped_column(Integer, nullable=True)

    __table_args__ = (
        CheckConstraint(
            "launch_year IS NULL OR (launch_year >= 1990 AND launch_year <= 2035)",
            name="chk_availability_specs_launch_year_range",
        ),
        CheckConstraint(
            "waiting_period_weeks IS NULL OR waiting_period_weeks >= 0",
            name="chk_availability_specs_waiting_period_non_negative",
        ),
    )

    # Relationships
    vehicle: Mapped["Vehicle"] = relationship(
        "Vehicle",
        back_populates="availability_spec",
        lazy="selectin",
        uselist=False,
    )

    def __repr__(self) -> str:
        return (
            f"<AvailabilitySpec(vehicle_id={self.vehicle_id}, "
            f"current_status={self.current_status!r})>"
        )
