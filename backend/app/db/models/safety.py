"""Variant safety specifications."""

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    ForeignKey,
    SmallInteger,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class VariantSafetySpec(Base):
    """Canonical active, passive, parking, and warning safety facts."""

    __tablename__ = "variant_safety_specs"

    variant_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("variants.id", ondelete="CASCADE"), primary_key=True
    )
    adas_level: Mapped[int | None] = mapped_column(SmallInteger)
    forward_collision_warning: Mapped[bool | None] = mapped_column(Boolean)
    automatic_emergency_braking: Mapped[bool | None] = mapped_column(Boolean)
    lane_departure_warning: Mapped[bool | None] = mapped_column(Boolean)
    lane_keep_assist: Mapped[bool | None] = mapped_column(Boolean)
    rear_collision_assist: Mapped[bool | None] = mapped_column(Boolean)
    rear_cross_traffic_alert: Mapped[bool | None] = mapped_column(Boolean)
    blind_spot_monitor: Mapped[bool | None] = mapped_column(Boolean)
    high_beam_assist: Mapped[bool | None] = mapped_column(Boolean)
    safe_exit_warning: Mapped[bool | None] = mapped_column(Boolean)
    tpms: Mapped[bool | None] = mapped_column(Boolean)
    automatic_park_lock: Mapped[bool | None] = mapped_column(Boolean)
    emergency_brake_light_flashing: Mapped[bool | None] = mapped_column(Boolean)
    avas: Mapped[bool | None] = mapped_column(Boolean)
    cng_leak_detection: Mapped[bool | None] = mapped_column(Boolean)
    video_recording: Mapped[bool | None] = mapped_column(Boolean)
    airbag_count: Mapped[int | None] = mapped_column(SmallInteger)
    driver_airbag: Mapped[bool | None] = mapped_column(Boolean)
    front_passenger_airbag: Mapped[bool | None] = mapped_column(Boolean)
    driver_side_airbag: Mapped[bool | None] = mapped_column(Boolean)
    front_passenger_side_airbag: Mapped[bool | None] = mapped_column(Boolean)
    curtain_airbag_count: Mapped[int | None] = mapped_column(SmallInteger)
    knee_airbag: Mapped[bool | None] = mapped_column(Boolean)
    seatbelt_pretensioner: Mapped[str | None] = mapped_column(Text)
    rear_middle_three_point_seatbelt: Mapped[bool | None] = mapped_column(Boolean)
    isofix_child_seat_anchors: Mapped[bool | None] = mapped_column(Boolean)
    child_safety_lock: Mapped[bool | None] = mapped_column(Boolean)
    engine_immobiliser: Mapped[bool | None] = mapped_column(Boolean)
    puncture_repair_kit: Mapped[bool | None] = mapped_column(Boolean)
    dashcam: Mapped[bool | None] = mapped_column(Boolean)
    front_brake: Mapped[str | None] = mapped_column(Text)
    rear_brake: Mapped[str | None] = mapped_column(Text)
    abs: Mapped[bool | None] = mapped_column(Boolean)
    ebd: Mapped[bool | None] = mapped_column(Boolean)
    brake_assist: Mapped[bool | None] = mapped_column(Boolean)
    esp: Mapped[bool | None] = mapped_column(Boolean)
    traction_control: Mapped[bool | None] = mapped_column(Boolean)
    hill_hold_control: Mapped[bool | None] = mapped_column(Boolean)
    hill_descent_control: Mapped[bool | None] = mapped_column(Boolean)
    torque_vectoring_brake_assist: Mapped[bool | None] = mapped_column(Boolean)
    adaptive_cruise_control: Mapped[bool | None] = mapped_column(Boolean)
    electronic_parking_brake: Mapped[bool | None] = mapped_column(Boolean)
    front_parking_sensors: Mapped[bool | None] = mapped_column(Boolean)
    rear_parking_sensors: Mapped[bool | None] = mapped_column(Boolean)
    parking_camera: Mapped[bool | None] = mapped_column(Boolean)
    overspeed_warning: Mapped[bool | None] = mapped_column(Boolean)
    door_ajar_warning: Mapped[bool | None] = mapped_column(Boolean)
    seatbelt_warning: Mapped[bool | None] = mapped_column(Boolean)
    boot_open_warning: Mapped[bool | None] = mapped_column(Boolean)
    low_fuel_warning: Mapped[bool | None] = mapped_column(Boolean)
    tow_away_alert: Mapped[bool | None] = mapped_column(Boolean)

    __table_args__ = (
        CheckConstraint(
            "adas_level IS NULL OR adas_level BETWEEN 0 AND 5",
            name="adas_level_range",
        ),
        CheckConstraint(
            "airbag_count IS NULL OR airbag_count BETWEEN 0 AND 20",
            name="airbag_count_range",
        ),
        CheckConstraint(
            "curtain_airbag_count IS NULL OR curtain_airbag_count BETWEEN 0 AND 10",
            name="curtain_airbag_count_range",
        ),
    )
