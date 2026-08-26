"""Variant infotainment and instrument specifications."""

from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    ForeignKey,
    Numeric,
    SmallInteger,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class VariantInfotainmentSpec(Base):
    """Canonical media, connectivity, charging, and driver-display facts."""

    __tablename__ = "variant_infotainment_specs"

    variant_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("variants.id", ondelete="CASCADE"), primary_key=True
    )
    infotainment_system: Mapped[str | None] = mapped_column(Text)
    infotainment_screen_size_inches: Mapped[Decimal | None] = mapped_column(
        Numeric(4, 1)
    )
    touchscreen: Mapped[bool | None] = mapped_column(Boolean)
    android_auto: Mapped[bool | None] = mapped_column(Boolean)
    android_auto_type: Mapped[str | None] = mapped_column(Text)
    apple_carplay: Mapped[bool | None] = mapped_column(Boolean)
    apple_carplay_type: Mapped[str | None] = mapped_column(Text)
    bluetooth: Mapped[bool | None] = mapped_column(Boolean)
    navigation: Mapped[bool | None] = mapped_column(Boolean)
    audio_system: Mapped[str | None] = mapped_column(Text)
    number_of_speakers: Mapped[int | None] = mapped_column(SmallInteger)
    tweeters: Mapped[int | None] = mapped_column(SmallInteger)
    usb_ports: Mapped[str | None] = mapped_column(Text)
    charging_ports: Mapped[str | None] = mapped_column(Text)
    wireless_charging: Mapped[bool | None] = mapped_column(Boolean)
    instrument_cluster: Mapped[str | None] = mapped_column(Text)
    instrument_cluster_size_inches: Mapped[Decimal | None] = mapped_column(
        Numeric(4, 1)
    )
    digital_speedometer: Mapped[bool | None] = mapped_column(Boolean)
    tachometer: Mapped[str | None] = mapped_column(Text)
    gear_indicator: Mapped[bool | None] = mapped_column(Boolean)
    gear_shift_indicator: Mapped[bool | None] = mapped_column(Boolean)
    hud: Mapped[bool | None] = mapped_column(Boolean)
    average_fuel_consumption_display: Mapped[bool | None] = mapped_column(Boolean)
    distance_to_empty: Mapped[bool | None] = mapped_column(Boolean)
    instantaneous_fuel_consumption: Mapped[bool | None] = mapped_column(Boolean)

    __table_args__ = (
        CheckConstraint(
            "infotainment_screen_size_inches IS NULL OR "
            "infotainment_screen_size_inches > 0",
            name="screen_size_positive",
        ),
        CheckConstraint(
            "instrument_cluster_size_inches IS NULL OR "
            "instrument_cluster_size_inches > 0",
            name="cluster_size_positive",
        ),
        CheckConstraint(
            "number_of_speakers IS NULL OR number_of_speakers >= 0",
            name="speaker_count_non_negative",
        ),
        CheckConstraint(
            "tweeters IS NULL OR tweeters >= 0",
            name="tweeter_count_non_negative",
        ),
    )
