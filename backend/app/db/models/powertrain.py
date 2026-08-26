"""Variant powertrain, charging, and terrain models."""

from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    ForeignKey,
    Identity,
    Integer,
    Numeric,
    SmallInteger,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class VariantPowertrainSpec(Base):
    """Canonical powertrain facts for one variant."""

    __tablename__ = "variant_powertrain_specs"

    variant_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("variants.id", ondelete="CASCADE"), primary_key=True
    )
    fuel_type: Mapped[str] = mapped_column(Text, nullable=False)
    transmission_type: Mapped[str] = mapped_column(Text, nullable=False)
    drivetrain: Mapped[str] = mapped_column(Text, nullable=False)
    mileage_arai_kmpl: Mapped[Decimal | None] = mapped_column(Numeric(6, 2))
    mileage_arai_kmkg: Mapped[Decimal | None] = mapped_column(Numeric(6, 2))
    mileage_user_reported: Mapped[Decimal | None] = mapped_column(Numeric(6, 2))
    engine_type: Mapped[str | None] = mapped_column(Text)
    engine_displacement_cc: Mapped[int | None] = mapped_column(Integer)
    cylinders: Mapped[int | None] = mapped_column(SmallInteger)
    max_power_bhp: Mapped[Decimal | None] = mapped_column(Numeric(7, 2))
    max_power_rpm: Mapped[int | None] = mapped_column(Integer)
    max_torque_nm: Mapped[Decimal | None] = mapped_column(Numeric(7, 2))
    max_torque_rpm_min: Mapped[int | None] = mapped_column(Integer)
    max_torque_rpm_max: Mapped[int | None] = mapped_column(Integer)
    forced_induction: Mapped[bool | None] = mapped_column(Boolean)
    idle_start_stop: Mapped[bool | None] = mapped_column(Boolean)
    emission_standard: Mapped[str | None] = mapped_column(Text)
    fuel_change_over_switch: Mapped[bool | None] = mapped_column(Boolean)
    direct_start_in_cng: Mapped[bool | None] = mapped_column(Boolean)
    driving_range_km: Mapped[int | None] = mapped_column(Integer)
    battery_capacity_kwh: Mapped[Decimal | None] = mapped_column(Numeric(7, 2))
    battery_type: Mapped[str | None] = mapped_column(Text)
    motor_type: Mapped[str | None] = mapped_column(Text)
    motor_power_kw: Mapped[Decimal | None] = mapped_column(Numeric(7, 2))
    motor_torque_nm: Mapped[Decimal | None] = mapped_column(Numeric(7, 2))
    pure_electric_driving_mode: Mapped[bool | None] = mapped_column(Boolean)
    number_of_gears: Mapped[int | None] = mapped_column(SmallInteger)
    differential_lock: Mapped[bool | None] = mapped_column(Boolean)
    battery_warranty_years: Mapped[int | None] = mapped_column(SmallInteger)
    battery_warranty_km: Mapped[int | None] = mapped_column(Integer)

    __table_args__ = (
        CheckConstraint(
            "fuel_type IN ('petrol','cng','hybrid','electric')",
            name="fuel_type_values",
        ),
        CheckConstraint(
            "transmission_type IN "
            "('manual','automatic','amt','torque_converter','e_cvt')",
            name="transmission_type_values",
        ),
        CheckConstraint(
            "drivetrain IN ('fwd','rwd','awd','4wd')",
            name="drivetrain_values",
        ),
        CheckConstraint(
            "emission_standard IS NULL OR emission_standard IN "
            "('bs6_phase_2','zero_tailpipe')",
            name="emission_standard_values",
        ),
        CheckConstraint(
            "max_torque_rpm_min IS NULL OR max_torque_rpm_max IS NULL OR "
            "max_torque_rpm_min <= max_torque_rpm_max",
            name="torque_rpm_order",
        ),
        CheckConstraint(
            "(engine_displacement_cc IS NULL OR engine_displacement_cc > 0) AND "
            "(cylinders IS NULL OR cylinders > 0) AND "
            "(max_power_bhp IS NULL OR max_power_bhp > 0) AND "
            "(max_torque_nm IS NULL OR max_torque_nm > 0) AND "
            "(battery_capacity_kwh IS NULL OR battery_capacity_kwh > 0) AND "
            "(driving_range_km IS NULL OR driving_range_km > 0)",
            name="positive_values",
        ),
    )


class VariantChargingOption(Base):
    """One AC or DC charging configuration for an electric variant."""

    __tablename__ = "variant_charging_options"

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)
    variant_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("variants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    current_type: Mapped[str] = mapped_column(Text, nullable=False)
    power_kw: Mapped[Decimal | None] = mapped_column(Numeric(6, 2))
    start_percent: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    end_percent: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "variant_id",
            "current_type",
            "power_kw",
            "start_percent",
            "end_percent",
            "duration_minutes",
            name="uq_variant_charging_options_configuration",
            postgresql_nulls_not_distinct=True,
        ),
        CheckConstraint("current_type IN ('ac','dc')", name="current_type_values"),
        CheckConstraint(
            "start_percent BETWEEN 0 AND 100 AND "
            "end_percent BETWEEN 0 AND 100 AND start_percent < end_percent",
            name="percentage_range",
        ),
        CheckConstraint("duration_minutes > 0", name="duration_positive"),
        CheckConstraint("power_kw IS NULL OR power_kw > 0", name="power_positive"),
    )


class VariantTerrainMode(Base):
    """One supported terrain mode for a variant."""

    __tablename__ = "variant_terrain_modes"

    variant_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("variants.id", ondelete="CASCADE"), primary_key=True
    )
    mode: Mapped[str] = mapped_column(Text, primary_key=True)

    __table_args__ = (CheckConstraint("btrim(mode) <> ''", name="mode_not_blank"),)
