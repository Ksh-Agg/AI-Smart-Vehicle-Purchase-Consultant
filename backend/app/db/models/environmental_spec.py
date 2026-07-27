"""Environmental specification ORM model."""

from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Enum, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.db.models.enums import EmissionStandard

if TYPE_CHECKING:
    from app.db.models.vehicle import Vehicle


class EnvironmentalSpec(Base, TimestampMixin):
    """EnvironmentalSpec model representing emission and EV-specific environmental data."""

    __tablename__ = "environmental_specs"

    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicles.id", ondelete="CASCADE"), primary_key=True
    )
    emission_standard: Mapped[EmissionStandard | None] = mapped_column(
        Enum(EmissionStandard, native_enum=True), nullable=True
    )
    co2_emissions_gkm: Mapped[float | None] = mapped_column(Float, nullable=True)
    battery_capacity_kwh: Mapped[float | None] = mapped_column(Float, nullable=True)
    electric_range_km: Mapped[int | None] = mapped_column(Integer, nullable=True)
    charging_time_ac_hr: Mapped[float | None] = mapped_column(Float, nullable=True)
    charging_time_dc_min: Mapped[int | None] = mapped_column(Integer, nullable=True)

    __table_args__ = (
        CheckConstraint(
            "co2_emissions_gkm IS NULL OR co2_emissions_gkm >= 0",
            name="chk_environmental_specs_co2_non_negative",
        ),
        CheckConstraint(
            "battery_capacity_kwh IS NULL OR battery_capacity_kwh > 0",
            name="chk_environmental_specs_battery_positive",
        ),
        CheckConstraint(
            "electric_range_km IS NULL OR electric_range_km > 0",
            name="chk_environmental_specs_electric_range_positive",
        ),
        CheckConstraint(
            "charging_time_ac_hr IS NULL OR charging_time_ac_hr > 0",
            name="chk_environmental_specs_charging_ac_positive",
        ),
        CheckConstraint(
            "charging_time_dc_min IS NULL OR charging_time_dc_min > 0",
            name="chk_environmental_specs_charging_dc_positive",
        ),
    )

    # Relationships
    vehicle: Mapped["Vehicle"] = relationship(
        "Vehicle",
        back_populates="environmental_spec",
        lazy="selectin",
        uselist=False,
    )

    def __repr__(self) -> str:
        return (
            f"<EnvironmentalSpec(vehicle_id={self.vehicle_id}, "
            f"emission_standard={self.emission_standard!r})>"
        )
