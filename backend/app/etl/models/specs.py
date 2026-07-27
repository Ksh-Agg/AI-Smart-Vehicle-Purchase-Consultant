"""Canonical Specifications Pydantic Models."""

from decimal import Decimal
from pydantic import BaseModel, Field

from app.db.models.enums import EmissionStandard, VehicleStatus


class CanonicalEngineSpec(BaseModel):
    """Canonical model for EngineSpec."""

    engine_cc: int | None = Field(None, gt=0)
    cylinders: int | None = Field(None, gt=0)
    power_bhp: float | None = Field(None, gt=0.0)
    torque_nm: float | None = Field(None, gt=0.0)
    mileage_kmpl: float | None = Field(None, gt=0.0)
    top_speed_kmph: int | None = Field(None, gt=0)
    acceleration_0_100_sec: float | None = Field(None, gt=0.0)
    fuel_tank_capacity_l: float | None = Field(None, gt=0.0)
    emission_norm: str | None = Field(None, max_length=30)

    class Config:
        frozen = True


class CanonicalDimensionSpec(BaseModel):
    """Canonical model for DimensionSpec."""

    length_mm: int | None = Field(None, gt=0)
    width_mm: int | None = Field(None, gt=0)
    height_mm: int | None = Field(None, gt=0)
    wheelbase_mm: int | None = Field(None, gt=0)
    ground_clearance_mm: int | None = Field(None, gt=0)
    boot_space_l: int | None = Field(None, gt=0)
    kerb_weight_kg: int | None = Field(None, gt=0)
    turning_radius_m: float | None = Field(None, gt=0.0)

    class Config:
        frozen = True


class CanonicalSafetySpec(BaseModel):
    """Canonical model for SafetySpec."""

    airbags: int | None = Field(None, ge=0)
    abs: bool | None = None
    esc: bool | None = None
    traction_control: bool | None = None
    hill_hold_control: bool | None = None
    hill_descent_control: bool | None = None
    isofix: bool | None = None
    tpms: bool | None = None
    blind_spot_monitor: bool | None = None
    lane_keep_assist: bool | None = None
    adaptive_cruise_control: bool | None = None
    autonomous_emergency_braking: bool | None = None
    adas_level: int | None = Field(None, ge=0, le=5)
    safety_rating: float | None = Field(None, ge=0.0, le=5.0)

    class Config:
        frozen = True


class CanonicalFeatureSpec(BaseModel):
    """Canonical model for FeatureSpec."""

    android_auto: bool | None = None
    apple_carplay: bool | None = None
    wireless_android_auto: bool | None = None
    wireless_apple_carplay: bool | None = None
    touchscreen_size_in: float | None = Field(None, gt=0.0)
    digital_instrument_cluster: bool | None = None
    climate_control: bool | None = None
    ventilated_seats: bool | None = None
    powered_driver_seat: bool | None = None
    sunroof: bool | None = None
    panoramic_sunroof: bool | None = None
    wireless_charging: bool | None = None
    keyless_entry: bool | None = None
    push_button_start: bool | None = None
    cruise_control: bool | None = None
    parking_camera: bool | None = None
    camera_360: bool | None = None
    parking_sensors: bool | None = None

    class Config:
        frozen = True


class CanonicalOwnershipSpec(BaseModel):
    """Canonical model for OwnershipSpec."""

    warranty_years: int | None = Field(None, gt=0)
    warranty_km: int | None = Field(None, gt=0)
    extended_warranty_available: bool | None = None
    service_interval_km: int | None = Field(None, gt=0)
    roadside_assistance: bool | None = None
    estimated_service_cost_per_year: Decimal | None = Field(None, ge=Decimal("0.0"))

    class Config:
        frozen = True


class CanonicalAvailabilitySpec(BaseModel):
    """Canonical model for AvailabilitySpec."""

    launch_year: int | None = Field(None, ge=1990, le=2035)
    current_status: VehicleStatus | None = None
    booking_open: bool | None = None
    waiting_period_weeks: int | None = Field(None, ge=0)

    class Config:
        frozen = True
        use_enum_values = False


class CanonicalEnvironmentalSpec(BaseModel):
    """Canonical model for EnvironmentalSpec."""

    emission_standard: EmissionStandard | None = None
    co2_emissions_gkm: float | None = Field(None, ge=0.0)
    battery_capacity_kwh: float | None = Field(None, gt=0.0)
    electric_range_km: int | None = Field(None, gt=0)
    charging_time_ac_hr: float | None = Field(None, gt=0.0)
    charging_time_dc_min: int | None = Field(None, gt=0)

    class Config:
        frozen = True
        use_enum_values = False
