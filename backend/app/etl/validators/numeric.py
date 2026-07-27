"""Numeric ranges and boundary validator rule."""

from app.etl.models.dataset import CanonicalVehicleDataset
from app.etl.validators.models import ValidationReport


def validate_numeric_ranges(
    dataset: CanonicalVehicleDataset, row_index: int, report: ValidationReport
) -> None:
    """Verifies that numeric specifications fall within valid ranges mapped to database constraints."""

    # 1. Vehicle boundaries
    v = dataset.vehicle
    if not (1990 <= v.year <= 2035):
        report.add_error(
            row_index,
            "vehicle.year",
            "value_out_of_range",
            f"Vehicle year ({v.year}) must be between 1990 and 2035.",
        )
    if not (1 <= v.seating_capacity <= 10):
        report.add_error(
            row_index,
            "vehicle.seating_capacity",
            "value_out_of_range",
            f"Seating capacity ({v.seating_capacity}) must be between 1 and 10.",
        )
    if v.doors is not None and not (2 <= v.doors <= 6):
        report.add_error(
            row_index,
            "vehicle.doors",
            "value_out_of_range",
            f"Doors count ({v.doors}) must be between 2 and 6.",
        )
    if v.price_ex_showroom <= 0:
        report.add_error(
            row_index,
            "vehicle.price_ex_showroom",
            "invalid_price",
            "Price ex-showroom must be positive.",
        )
    if v.price_on_road is not None and v.price_on_road <= 0:
        report.add_error(
            row_index,
            "vehicle.price_on_road",
            "invalid_price",
            "Price on-road must be positive.",
        )

    # 2. Engine Spec boundaries
    eng = dataset.engine_spec
    if eng.engine_cc is not None and eng.engine_cc <= 0:
        report.add_error(
            row_index,
            "engine_spec.engine_cc",
            "invalid_cc",
            "Engine displacement must be positive.",
        )
    if eng.power_bhp is not None and eng.power_bhp <= 0:
        report.add_error(
            row_index,
            "engine_spec.power_bhp",
            "invalid_power",
            "Power (bhp) must be positive.",
        )
    if eng.torque_nm is not None and eng.torque_nm <= 0:
        report.add_error(
            row_index,
            "engine_spec.torque_nm",
            "invalid_torque",
            "Torque (Nm) must be positive.",
        )
    if eng.mileage_kmpl is not None and eng.mileage_kmpl <= 0:
        report.add_error(
            row_index,
            "engine_spec.mileage_kmpl",
            "invalid_mileage",
            "Mileage must be positive.",
        )
    if eng.fuel_tank_capacity_l is not None and eng.fuel_tank_capacity_l <= 0:
        report.add_error(
            row_index,
            "engine_spec.fuel_tank_capacity_l",
            "invalid_fuel_tank",
            "Fuel tank capacity must be positive.",
        )

    # 3. Dimension Spec boundaries
    dim = dataset.dimension_spec
    if dim.kerb_weight_kg is not None and dim.kerb_weight_kg <= 0:
        report.add_error(
            row_index,
            "dimension_spec.kerb_weight_kg",
            "invalid_weight",
            "Kerb weight must be positive.",
        )
    if dim.turning_radius_m is not None and dim.turning_radius_m <= 0:
        report.add_error(
            row_index,
            "dimension_spec.turning_radius_m",
            "invalid_turning_radius",
            "Turning radius must be positive.",
        )

    # 4. Safety Spec boundaries
    saf = dataset.safety_spec
    if saf.airbags is not None and saf.airbags < 0:
        report.add_error(
            row_index,
            "safety_spec.airbags",
            "invalid_airbags",
            "Airbags count cannot be negative.",
        )
    if saf.safety_rating is not None and not (0.0 <= saf.safety_rating <= 5.0):
        report.add_error(
            row_index,
            "safety_spec.safety_rating",
            "value_out_of_range",
            f"Safety rating ({saf.safety_rating}) must be between 0.0 and 5.0.",
        )
    if saf.adas_level is not None and not (0 <= saf.adas_level <= 5):
        report.add_error(
            row_index,
            "safety_spec.adas_level",
            "value_out_of_range",
            f"ADAS level ({saf.adas_level}) must be between 0 and 5.",
        )

    # 5. Ownership Spec boundaries
    own = dataset.ownership_spec
    if own.warranty_years is not None and own.warranty_years <= 0:
        report.add_error(
            row_index,
            "ownership_spec.warranty_years",
            "invalid_warranty",
            "Warranty years must be positive.",
        )
    if own.warranty_km is not None and own.warranty_km <= 0:
        report.add_error(
            row_index,
            "ownership_spec.warranty_km",
            "invalid_warranty",
            "Warranty kilometers must be positive.",
        )
    if own.service_interval_km is not None and own.service_interval_km <= 0:
        report.add_error(
            row_index,
            "ownership_spec.service_interval_km",
            "invalid_service_interval",
            "Service interval must be positive.",
        )
    if (
        own.estimated_service_cost_per_year is not None
        and own.estimated_service_cost_per_year < 0
    ):
        report.add_error(
            row_index,
            "ownership_spec.estimated_service_cost_per_year",
            "invalid_service_cost",
            "Service cost per year cannot be negative.",
        )

    # 6. Availability Spec boundaries
    avail = dataset.availability_spec
    if avail.launch_year is not None and not (1990 <= avail.launch_year <= 2035):
        report.add_error(
            row_index,
            "availability_spec.launch_year",
            "value_out_of_range",
            f"Launch year ({avail.launch_year}) must be between 1990 and 2035.",
        )
    if avail.waiting_period_weeks is not None and avail.waiting_period_weeks < 0:
        report.add_error(
            row_index,
            "availability_spec.waiting_period_weeks",
            "invalid_waiting_period",
            "Waiting period weeks cannot be negative.",
        )

    # 7. Environmental Spec boundaries
    env = dataset.environmental_spec
    if env.co2_emissions_gkm is not None and env.co2_emissions_gkm < 0:
        report.add_error(
            row_index,
            "environmental_spec.co2_emissions_gkm",
            "invalid_co2",
            "CO2 emissions cannot be negative.",
        )
    if env.battery_capacity_kwh is not None and env.battery_capacity_kwh <= 0:
        report.add_error(
            row_index,
            "environmental_spec.battery_capacity_kwh",
            "invalid_battery",
            "Battery capacity must be positive.",
        )
    if env.electric_range_km is not None and env.electric_range_km <= 0:
        report.add_error(
            row_index,
            "environmental_spec.electric_range_km",
            "invalid_range",
            "Electric range must be positive.",
        )
    if env.charging_time_ac_hr is not None and env.charging_time_ac_hr <= 0:
        report.add_error(
            row_index,
            "environmental_spec.charging_time_ac_hr",
            "invalid_charging_time",
            "AC charging time must be positive.",
        )
    if env.charging_time_dc_min is not None and env.charging_time_dc_min <= 0:
        report.add_error(
            row_index,
            "environmental_spec.charging_time_dc_min",
            "invalid_charging_time",
            "DC charging time must be positive.",
        )
