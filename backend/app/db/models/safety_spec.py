"""Safety specification ORM model."""

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, CheckConstraint, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.db.models.vehicle import Vehicle


class SafetySpec(Base, TimestampMixin):
    """SafetySpec model representing vehicle safety configurations."""

    __tablename__ = "safety_specs"

    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicles.id", ondelete="CASCADE"), primary_key=True
    )
    airbags: Mapped[int | None] = mapped_column(Integer, nullable=True)
    abs: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    esc: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    traction_control: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    hill_hold_control: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    hill_descent_control: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    isofix: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    tpms: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    blind_spot_monitor: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    lane_keep_assist: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    adaptive_cruise_control: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    autonomous_emergency_braking: Mapped[bool | None] = mapped_column(
        Boolean, nullable=True
    )
    adas_level: Mapped[int | None] = mapped_column(Integer, nullable=True)
    safety_rating: Mapped[float | None] = mapped_column(Float, nullable=True)

    __table_args__ = (
        CheckConstraint(
            "airbags IS NULL OR airbags >= 0",
            name="chk_safety_specs_airbags_non_negative",
        ),
        CheckConstraint(
            "safety_rating IS NULL OR (safety_rating >= 0 AND safety_rating <= 5)",
            name="chk_safety_specs_safety_rating_range",
        ),
        CheckConstraint(
            "adas_level IS NULL OR (adas_level >= 0 AND adas_level <= 5)",
            name="chk_safety_specs_adas_level_range",
        ),
    )

    # Relationships
    vehicle: Mapped["Vehicle"] = relationship(
        "Vehicle",
        back_populates="safety_spec",
        lazy="selectin",
        uselist=False,
    )

    def __repr__(self) -> str:
        return f"<SafetySpec(vehicle_id={self.vehicle_id}, airbags={self.airbags})>"
