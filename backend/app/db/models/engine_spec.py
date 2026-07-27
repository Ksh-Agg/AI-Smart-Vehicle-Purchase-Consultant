"""Engine specification ORM model."""

from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.db.models.vehicle import Vehicle


class EngineSpec(Base, TimestampMixin):
    """EngineSpec model representing vehicle engine technical details."""

    __tablename__ = "engine_specs"

    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicles.id", ondelete="CASCADE"), primary_key=True
    )
    engine_cc: Mapped[int | None] = mapped_column(Integer, nullable=True)
    cylinders: Mapped[int | None] = mapped_column(Integer, nullable=True)
    power_bhp: Mapped[float | None] = mapped_column(Float, nullable=True)
    torque_nm: Mapped[float | None] = mapped_column(Float, nullable=True)
    mileage_kmpl: Mapped[float | None] = mapped_column(Float, nullable=True)
    top_speed_kmph: Mapped[int | None] = mapped_column(Integer, nullable=True)
    acceleration_0_100_sec: Mapped[float | None] = mapped_column(Float, nullable=True)
    fuel_tank_capacity_l: Mapped[float | None] = mapped_column(Float, nullable=True)
    emission_norm: Mapped[str | None] = mapped_column(String(30), nullable=True)

    __table_args__ = (
        CheckConstraint(
            "engine_cc IS NULL OR engine_cc > 0",
            name="chk_engine_specs_engine_cc_positive",
        ),
        CheckConstraint(
            "power_bhp IS NULL OR power_bhp > 0",
            name="chk_engine_specs_power_bhp_positive",
        ),
        CheckConstraint(
            "torque_nm IS NULL OR torque_nm > 0",
            name="chk_engine_specs_torque_nm_positive",
        ),
        CheckConstraint(
            "mileage_kmpl IS NULL OR mileage_kmpl > 0",
            name="chk_engine_specs_mileage_positive",
        ),
        CheckConstraint(
            "top_speed_kmph IS NULL OR top_speed_kmph > 0",
            name="chk_engine_specs_top_speed_positive",
        ),
        CheckConstraint(
            "acceleration_0_100_sec IS NULL OR acceleration_0_100_sec > 0",
            name="chk_engine_specs_acceleration_positive",
        ),
        CheckConstraint(
            "fuel_tank_capacity_l IS NULL OR fuel_tank_capacity_l > 0",
            name="chk_engine_specs_fuel_tank_positive",
        ),
    )

    # Relationships
    vehicle: Mapped["Vehicle"] = relationship(
        "Vehicle",
        back_populates="engine_spec",
        lazy="selectin",
        uselist=False,
    )

    def __repr__(self) -> str:
        return f"<EngineSpec(vehicle_id={self.vehicle_id}, engine_cc={self.engine_cc})>"
