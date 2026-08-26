"""Create the normalized catalogue schema.

Revision ID: 20260827_0001
Revises:
"""

# fmt: off
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260827_0001"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _nullable(type_: sa.types.TypeEngine[object], names: str) -> list[sa.Column]:
    return [sa.Column(name, type_, nullable=True) for name in names.split()]


def _timestamps() -> list[sa.Column]:
    return [sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False)]


def _variant_table(name: str, *items: object, primary_key: tuple[str, ...] = ("variant_id",)) -> None:
    op.create_table(name, sa.Column("variant_id", sa.BigInteger(), nullable=False), *items, sa.ForeignKeyConstraint(["variant_id"], ["variants.id"], ondelete="CASCADE"), sa.PrimaryKeyConstraint(*primary_key))


def upgrade() -> None:
    """Create all catalogue tables."""
    op.create_table("brands", sa.Column("id", sa.BigInteger(), sa.Identity(), nullable=False), sa.Column("name", sa.Text(), nullable=False), *_timestamps(), sa.CheckConstraint("btrim(name) <> ''", name="name_not_blank"), sa.PrimaryKeyConstraint("id"))
    op.create_index("uq_brands_name_ci", "brands", [sa.text("lower(name)")], unique=True)
    op.create_table("vehicle_models", sa.Column("id", sa.BigInteger(), sa.Identity(), nullable=False), sa.Column("brand_id", sa.BigInteger(), nullable=False), sa.Column("name", sa.Text(), nullable=False), *_timestamps(), sa.CheckConstraint("btrim(name) <> ''", name="name_not_blank"), sa.ForeignKeyConstraint(["brand_id"], ["brands.id"], ondelete="RESTRICT"), sa.PrimaryKeyConstraint("id"))
    op.create_index("ix_vehicle_models_brand_id", "vehicle_models", ["brand_id"])
    op.create_index("uq_vehicle_models_brand_name_ci", "vehicle_models", ["brand_id", sa.text("lower(name)")], unique=True)
    op.create_table("variants", sa.Column("id", sa.BigInteger(), sa.Identity(), nullable=False), sa.Column("catalogue_id", sa.Text(), nullable=False), sa.Column("model_id", sa.BigInteger(), nullable=False), sa.Column("trim", sa.Text(), nullable=False), sa.Column("variant_name", sa.Text(), nullable=False), sa.Column("model_year", sa.Integer(), nullable=False), sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False), *_timestamps(), sa.CheckConstraint("btrim(catalogue_id) <> ''", name="catalogue_id_not_blank"), sa.CheckConstraint("btrim(trim) <> ''", name="trim_not_blank"), sa.CheckConstraint("btrim(variant_name) <> ''", name="variant_name_not_blank"), sa.CheckConstraint("model_year BETWEEN 1886 AND 2100", name="model_year_range"), sa.ForeignKeyConstraint(["model_id"], ["vehicle_models.id"], ondelete="RESTRICT"), sa.PrimaryKeyConstraint("id"), sa.UniqueConstraint("catalogue_id"))
    op.create_index("ix_variants_model_id", "variants", ["model_id"])
    op.create_table("variant_prices", sa.Column("variant_id", sa.BigInteger(), nullable=False), sa.Column("city", sa.Text(), nullable=False), sa.Column("ex_showroom_price", sa.Numeric(12, 2), nullable=False), sa.Column("on_road_price", sa.Numeric(12, 2)), *_timestamps(), sa.CheckConstraint("btrim(city) <> ''", name="city_not_blank"), sa.CheckConstraint("ex_showroom_price > 0", name="ex_showroom_price_positive"), sa.CheckConstraint("on_road_price IS NULL OR on_road_price > 0", name="on_road_price_positive"), sa.ForeignKeyConstraint(["variant_id"], ["variants.id"], ondelete="CASCADE"), sa.PrimaryKeyConstraint("variant_id", "city"))
    _create_powertrain_tables()
    _create_specification_tables()
    _create_feature_tables()


def _create_powertrain_tables() -> None:
    _variant_table("variant_powertrain_specs", sa.Column("fuel_type", sa.Text(), nullable=False), sa.Column("transmission_type", sa.Text(), nullable=False), sa.Column("drivetrain", sa.Text(), nullable=False), *_nullable(sa.Numeric(6, 2), "mileage_arai_kmpl mileage_arai_kmkg mileage_user_reported"), *_nullable(sa.Text(), "engine_type emission_standard battery_type motor_type"), *_nullable(sa.Integer(), "engine_displacement_cc max_power_rpm max_torque_rpm_min max_torque_rpm_max driving_range_km battery_warranty_km"), *_nullable(sa.SmallInteger(), "cylinders number_of_gears battery_warranty_years"), *_nullable(sa.Numeric(7, 2), "max_power_bhp max_torque_nm battery_capacity_kwh motor_power_kw motor_torque_nm"), *_nullable(sa.Boolean(), "forced_induction idle_start_stop fuel_change_over_switch direct_start_in_cng pure_electric_driving_mode differential_lock"), sa.CheckConstraint("fuel_type IN ('petrol','cng','hybrid','electric')", name="fuel_type_values"), sa.CheckConstraint("transmission_type IN ('manual','automatic','amt','torque_converter','e_cvt')", name="transmission_type_values"), sa.CheckConstraint("drivetrain IN ('fwd','rwd','awd','4wd')", name="drivetrain_values"), sa.CheckConstraint("emission_standard IS NULL OR emission_standard IN ('bs6_phase_2','zero_tailpipe')", name="emission_standard_values"), sa.CheckConstraint("max_torque_rpm_min IS NULL OR max_torque_rpm_max IS NULL OR max_torque_rpm_min <= max_torque_rpm_max", name="torque_rpm_order"), sa.CheckConstraint("(engine_displacement_cc IS NULL OR engine_displacement_cc > 0) AND (cylinders IS NULL OR cylinders > 0) AND (max_power_bhp IS NULL OR max_power_bhp > 0) AND (max_torque_nm IS NULL OR max_torque_nm > 0) AND (battery_capacity_kwh IS NULL OR battery_capacity_kwh > 0) AND (driving_range_km IS NULL OR driving_range_km > 0)", name="positive_values"))
    op.create_table("variant_charging_options", sa.Column("id", sa.BigInteger(), sa.Identity(), nullable=False), sa.Column("variant_id", sa.BigInteger(), nullable=False), sa.Column("current_type", sa.Text(), nullable=False), sa.Column("power_kw", sa.Numeric(6, 2)), sa.Column("start_percent", sa.SmallInteger(), nullable=False), sa.Column("end_percent", sa.SmallInteger(), nullable=False), sa.Column("duration_minutes", sa.Integer(), nullable=False), sa.CheckConstraint("current_type IN ('ac','dc')", name="current_type_values"), sa.CheckConstraint("start_percent BETWEEN 0 AND 100 AND end_percent BETWEEN 0 AND 100 AND start_percent < end_percent", name="percentage_range"), sa.CheckConstraint("duration_minutes > 0", name="duration_positive"), sa.CheckConstraint("power_kw IS NULL OR power_kw > 0", name="power_positive"), sa.ForeignKeyConstraint(["variant_id"], ["variants.id"], ondelete="CASCADE"), sa.PrimaryKeyConstraint("id"), sa.UniqueConstraint("variant_id", "current_type", "power_kw", "start_percent", "end_percent", "duration_minutes", name="uq_variant_charging_options_configuration", postgresql_nulls_not_distinct=True))
    op.create_index("ix_variant_charging_options_variant_id", "variant_charging_options", ["variant_id"])
    _variant_table("variant_terrain_modes", sa.Column("mode", sa.Text(), nullable=False), sa.CheckConstraint("btrim(mode) <> ''", name="mode_not_blank"), primary_key=("variant_id", "mode"))


def _create_specification_tables() -> None:
    _variant_table("variant_physical_specs", *_nullable(sa.Text(), "chassis_type front_suspension rear_suspension wheel_type tyre_size"), *_nullable(sa.Integer(), "length_mm width_mm height_mm wheelbase_mm ground_clearance_mm kerb_weight_kg bootspace_litres"), *_nullable(sa.SmallInteger(), "seating_capacity number_of_rows number_of_doors"), *_nullable(sa.Numeric(6, 2), "fuel_tank_capacity_litres cng_cylinder_water_capacity_litres"), sa.Column("wheel_size_inches", sa.Numeric(4, 1)), *_nullable(sa.Boolean(), "spare_wheel roof_rails dual_tone_exterior"), sa.CheckConstraint("(length_mm IS NULL OR length_mm > 0) AND (width_mm IS NULL OR width_mm > 0) AND (height_mm IS NULL OR height_mm > 0) AND (wheelbase_mm IS NULL OR wheelbase_mm > 0) AND (ground_clearance_mm IS NULL OR ground_clearance_mm > 0) AND (kerb_weight_kg IS NULL OR kerb_weight_kg > 0) AND (bootspace_litres IS NULL OR bootspace_litres > 0)", name="positive_dimensions"), sa.CheckConstraint("seating_capacity IS NULL OR seating_capacity BETWEEN 1 AND 20", name="seating_capacity_range"), sa.CheckConstraint("number_of_rows IS NULL OR number_of_rows BETWEEN 1 AND 5", name="row_count_range"), sa.CheckConstraint("number_of_doors IS NULL OR number_of_doors BETWEEN 1 AND 10", name="door_count_range"), sa.CheckConstraint("(fuel_tank_capacity_litres IS NULL OR fuel_tank_capacity_litres > 0) AND (cng_cylinder_water_capacity_litres IS NULL OR cng_cylinder_water_capacity_litres > 0) AND (wheel_size_inches IS NULL OR wheel_size_inches > 0)", name="positive_capacities"))
    safety = "forward_collision_warning automatic_emergency_braking lane_departure_warning lane_keep_assist rear_collision_assist rear_cross_traffic_alert blind_spot_monitor high_beam_assist safe_exit_warning tpms automatic_park_lock emergency_brake_light_flashing avas cng_leak_detection video_recording driver_airbag front_passenger_airbag driver_side_airbag front_passenger_side_airbag knee_airbag rear_middle_three_point_seatbelt isofix_child_seat_anchors child_safety_lock engine_immobiliser puncture_repair_kit dashcam abs ebd brake_assist esp traction_control hill_hold_control hill_descent_control torque_vectoring_brake_assist adaptive_cruise_control electronic_parking_brake front_parking_sensors rear_parking_sensors parking_camera overspeed_warning door_ajar_warning seatbelt_warning boot_open_warning low_fuel_warning tow_away_alert"
    _variant_table("variant_safety_specs", *_nullable(sa.SmallInteger(), "adas_level airbag_count curtain_airbag_count"), *_nullable(sa.Text(), "seatbelt_pretensioner front_brake rear_brake"), *_nullable(sa.Boolean(), safety), sa.CheckConstraint("adas_level IS NULL OR adas_level BETWEEN 0 AND 5", name="adas_level_range"), sa.CheckConstraint("airbag_count IS NULL OR airbag_count BETWEEN 0 AND 20", name="airbag_count_range"), sa.CheckConstraint("curtain_airbag_count IS NULL OR curtain_airbag_count BETWEEN 0 AND 10", name="curtain_airbag_count_range"))
    comfort = "air_conditioner rear_ac rear_ac_vents heater air_purifier central_locking keyless_entry auto_dimming_irvm reverse_tilt_orvm rear_defogger rear_wiper rear_washer sunroof power_windows front_power_windows rear_power_windows window_sunshade push_button_start cruise_control cooled_glovebox driver_seat_height_adjustment front_headrests rear_headrests ventilated_front_seats ventilated_rear_seats split_rear_seat driver_armrest rear_armrest dead_pedal height_adjustable_seatbelts foldable_seatback_table power_steering tilt_steering telescopic_steering steering_mounted_controls"
    _variant_table("variant_comfort_specs", *_nullable(sa.Text(), "climate_control_type boot_opener irvm orvm_adjustment orvm_folding sunroof_type one_touch_windows driver_seat_adjustment front_passenger_seat_adjustment rear_seat_adjustment power_steering_type"), *_nullable(sa.SmallInteger(), "rear_seat_split_left_percent rear_seat_split_center_percent rear_seat_split_right_percent"), *_nullable(sa.Boolean(), comfort), sa.CheckConstraint("(rear_seat_split_left_percent IS NULL OR rear_seat_split_left_percent BETWEEN 0 AND 100) AND (rear_seat_split_center_percent IS NULL OR rear_seat_split_center_percent BETWEEN 0 AND 100) AND (rear_seat_split_right_percent IS NULL OR rear_seat_split_right_percent BETWEEN 0 AND 100)", name="rear_seat_split_range"))


def _create_feature_tables() -> None:
    infotainment = "touchscreen android_auto apple_carplay bluetooth navigation wireless_charging digital_speedometer gear_indicator gear_shift_indicator hud average_fuel_consumption_display distance_to_empty instantaneous_fuel_consumption"
    _variant_table("variant_infotainment_specs", *_nullable(sa.Text(), "infotainment_system android_auto_type apple_carplay_type audio_system usb_ports charging_ports instrument_cluster tachometer"), *_nullable(sa.Numeric(4, 1), "infotainment_screen_size_inches instrument_cluster_size_inches"), *_nullable(sa.SmallInteger(), "number_of_speakers tweeters"), *_nullable(sa.Boolean(), infotainment), sa.CheckConstraint("infotainment_screen_size_inches IS NULL OR infotainment_screen_size_inches > 0", name="screen_size_positive"), sa.CheckConstraint("instrument_cluster_size_inches IS NULL OR instrument_cluster_size_inches > 0", name="cluster_size_positive"), sa.CheckConstraint("number_of_speakers IS NULL OR number_of_speakers >= 0", name="speaker_count_non_negative"), sa.CheckConstraint("tweeters IS NULL OR tweeters >= 0", name="tweeter_count_non_negative"))
    _variant_table("variant_lighting_specs", *_nullable(sa.Text(), "headlamp_type drl_type"), *_nullable(sa.Boolean(), "projector_headlamps led_headlamps fog_lights front_fog_lights rear_fog_lights drl follow_me_home_headlamps automatic_headlamps ambient_interior_lighting"))
    _variant_table("variant_connected_specs", *_nullable(sa.Text(), "remote_ac remote_lock_unlock"), *_nullable(sa.Boolean(), "connected_car_technology ota_updates alexa_compatibility remote_engine_start vehicle_tracking geo_fencing"))


def downgrade() -> None:
    """Drop the complete catalogue schema."""
    for table in "variant_connected_specs variant_lighting_specs variant_infotainment_specs variant_comfort_specs variant_safety_specs variant_physical_specs variant_terrain_modes variant_charging_options variant_powertrain_specs variant_prices variants vehicle_models brands".split():
        op.drop_table(table)
