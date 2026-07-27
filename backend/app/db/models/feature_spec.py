"""Feature specification ORM model."""

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.db.models.vehicle import Vehicle


class FeatureSpec(Base, TimestampMixin):
    """FeatureSpec model representing vehicle tech and comfort features."""

    __tablename__ = "feature_specs"

    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicles.id", ondelete="CASCADE"), primary_key=True
    )
    android_auto: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    apple_carplay: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    wireless_android_auto: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    wireless_apple_carplay: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    touchscreen_size_in: Mapped[float | None] = mapped_column(Float, nullable=True)
    digital_instrument_cluster: Mapped[bool | None] = mapped_column(
        Boolean, nullable=True
    )
    climate_control: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    ventilated_seats: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    powered_driver_seat: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    sunroof: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    panoramic_sunroof: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    wireless_charging: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    keyless_entry: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    push_button_start: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    cruise_control: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    parking_camera: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    camera_360: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    parking_sensors: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    # Relationships
    vehicle: Mapped["Vehicle"] = relationship(
        "Vehicle",
        back_populates="feature_spec",
        lazy="selectin",
        uselist=False,
    )

    def __repr__(self) -> str:
        return f"<FeatureSpec(vehicle_id={self.vehicle_id}, sunroof={self.sunroof})>"
