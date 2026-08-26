"""Variant comfort specifications."""

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


class VariantComfortSpec(Base):
    """Canonical cabin, seating, mirror, window, and steering facts."""

    __tablename__ = "variant_comfort_specs"

    variant_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("variants.id", ondelete="CASCADE"), primary_key=True
    )
    air_conditioner: Mapped[bool | None] = mapped_column(Boolean)
    climate_control_type: Mapped[str | None] = mapped_column(Text)
    rear_ac: Mapped[bool | None] = mapped_column(Boolean)
    rear_ac_vents: Mapped[bool | None] = mapped_column(Boolean)
    heater: Mapped[bool | None] = mapped_column(Boolean)
    air_purifier: Mapped[bool | None] = mapped_column(Boolean)
    central_locking: Mapped[bool | None] = mapped_column(Boolean)
    keyless_entry: Mapped[bool | None] = mapped_column(Boolean)
    boot_opener: Mapped[str | None] = mapped_column(Text)
    irvm: Mapped[str | None] = mapped_column(Text)
    auto_dimming_irvm: Mapped[bool | None] = mapped_column(Boolean)
    orvm_adjustment: Mapped[str | None] = mapped_column(Text)
    orvm_folding: Mapped[str | None] = mapped_column(Text)
    reverse_tilt_orvm: Mapped[bool | None] = mapped_column(Boolean)
    rear_defogger: Mapped[bool | None] = mapped_column(Boolean)
    rear_wiper: Mapped[bool | None] = mapped_column(Boolean)
    rear_washer: Mapped[bool | None] = mapped_column(Boolean)
    sunroof: Mapped[bool | None] = mapped_column(Boolean)
    sunroof_type: Mapped[str | None] = mapped_column(Text)
    power_windows: Mapped[bool | None] = mapped_column(Boolean)
    front_power_windows: Mapped[bool | None] = mapped_column(Boolean)
    rear_power_windows: Mapped[bool | None] = mapped_column(Boolean)
    one_touch_windows: Mapped[str | None] = mapped_column(Text)
    window_sunshade: Mapped[bool | None] = mapped_column(Boolean)
    push_button_start: Mapped[bool | None] = mapped_column(Boolean)
    cruise_control: Mapped[bool | None] = mapped_column(Boolean)
    cooled_glovebox: Mapped[bool | None] = mapped_column(Boolean)
    driver_seat_adjustment: Mapped[str | None] = mapped_column(Text)
    driver_seat_height_adjustment: Mapped[bool | None] = mapped_column(Boolean)
    front_passenger_seat_adjustment: Mapped[str | None] = mapped_column(Text)
    rear_seat_adjustment: Mapped[str | None] = mapped_column(Text)
    front_headrests: Mapped[bool | None] = mapped_column(Boolean)
    rear_headrests: Mapped[bool | None] = mapped_column(Boolean)
    ventilated_front_seats: Mapped[bool | None] = mapped_column(Boolean)
    ventilated_rear_seats: Mapped[bool | None] = mapped_column(Boolean)
    split_rear_seat: Mapped[bool | None] = mapped_column(Boolean)
    rear_seat_split_left_percent: Mapped[int | None] = mapped_column(SmallInteger)
    rear_seat_split_center_percent: Mapped[int | None] = mapped_column(SmallInteger)
    rear_seat_split_right_percent: Mapped[int | None] = mapped_column(SmallInteger)
    driver_armrest: Mapped[bool | None] = mapped_column(Boolean)
    rear_armrest: Mapped[bool | None] = mapped_column(Boolean)
    dead_pedal: Mapped[bool | None] = mapped_column(Boolean)
    height_adjustable_seatbelts: Mapped[bool | None] = mapped_column(Boolean)
    foldable_seatback_table: Mapped[bool | None] = mapped_column(Boolean)
    power_steering: Mapped[bool | None] = mapped_column(Boolean)
    power_steering_type: Mapped[str | None] = mapped_column(Text)
    tilt_steering: Mapped[bool | None] = mapped_column(Boolean)
    telescopic_steering: Mapped[bool | None] = mapped_column(Boolean)
    steering_mounted_controls: Mapped[bool | None] = mapped_column(Boolean)

    __table_args__ = (
        CheckConstraint(
            "(rear_seat_split_left_percent IS NULL OR "
            "rear_seat_split_left_percent BETWEEN 0 AND 100) AND "
            "(rear_seat_split_center_percent IS NULL OR "
            "rear_seat_split_center_percent BETWEEN 0 AND 100) AND "
            "(rear_seat_split_right_percent IS NULL OR "
            "rear_seat_split_right_percent BETWEEN 0 AND 100)",
            name="rear_seat_split_range",
        ),
    )
