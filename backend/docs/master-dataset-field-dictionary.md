# SVPC Master Dataset Field Dictionary v1.1

**Project:** Smart Vehicle Purchase Consultant (SVPC)  
**Version:** 1.1  
**Purpose:** This document defines the canonical data model for the SVPC Master Dataset. All external datasets (Kaggle, manufacturer brochures, APIs, etc.) must be transformed into this schema before being imported into PostgreSQL.

---

# Design Principles

- The Master Dataset is the **single source of truth**.
- Raw datasets must never be modified directly.
- Every external source must be mapped into this schema.
- Missing values should be stored as `NULL`.
- Units must be standardized before import.
- Enum values should follow the project's predefined enums.

## Derived Fields

The following values are intentionally **not stored** in the database because they are fully derivable at runtime from stored columns:

| Derived Value | Derived From | Where Computed |
|---|---|---|
| `price_category` | `price_ex_showroom` | Service / API layer |
| `vehicle_type` | `fuel_type` | Service / API layer |

Storing derived values introduces redundancy and risks data inconsistency (e.g., a vehicle with `fuel_type = EV` assigned `vehicle_type = ICE`). These values must always be computed on demand, never persisted.

---

# Category 1 — Vehicle Identity

| Field | Data Type | Required | Description | Database Table |
|--------|-----------|----------|-------------|----------------|
| brand | String | ✅ | Manufacturer name | brands |
| model | String | ✅ | Vehicle model | vehicles |
| variant | String | ✅ | Variant/Trim name | vehicles |
| year | Integer | ✅ | Model year | vehicles |
| body_type | Enum | ✅ | Hatchback, Sedan, SUV, MUV, Coupe, Convertible, Pickup | vehicles |
| segment | Enum | ✅ | A, B, C, D, Premium, Luxury | vehicles |
| fuel_type | Enum | ✅ | Petrol, Diesel, CNG, Electric, Hybrid, Plugin Hybrid | vehicles |

> **Note on `fuel_type` placement:** Although fuel type is technically an engine characteristic, it is one of the primary filtering attributes used in recommendation queries. Retaining it on the `vehicles` table avoids an extra JOIN on every common filter and improves query performance. This is an intentional, documented denormalization.

---

# Category 2 — Pricing

| Field | Data Type | Required | Description | Database Table |
|--------|-----------|----------|-------------|----------------|
| price_ex_showroom | Decimal | ✅ | Ex-showroom price (₹) | vehicles |
| price_on_road | Decimal | Optional | On-road price (₹) | vehicles |

---

# Category 3 — Engine & Performance

| Field | Data Type | Required | Description | Database Table |
|--------|-----------|----------|-------------|----------------|
| engine_cc | Integer | Optional | Engine displacement (cc) | engine_specs |
| cylinders | Integer | Optional | Number of cylinders | engine_specs |
| power_bhp | Float | Optional | Maximum power (bhp) | engine_specs |
| torque_nm | Float | Optional | Maximum torque (Nm) | engine_specs |
| mileage_kmpl | Float | Optional | Certified mileage | engine_specs |
| top_speed_kmph | Integer | Optional | Maximum speed | engine_specs |
| acceleration_0_100_sec | Float | Optional | 0–100 km/h acceleration time | engine_specs |
| fuel_tank_capacity_l | Float | Optional | Fuel tank capacity (litres) | engine_specs |
| transmission | Enum | ✅ | Manual, Automatic, AMT, CVT, DCT | vehicles |
| drivetrain | Enum | Optional | FWD, RWD, AWD, 4WD | vehicles |

> **Note on `fuel_tank_capacity_l` placement:** Fuel tank capacity is a manufacturer-published engine specification and is consistently reported alongside engine data in public datasets. It is retained in `engine_specs` rather than `ownership_specs`.

---

# Category 4 — Dimensions

| Field | Data Type | Required | Description | Database Table |
|--------|-----------|----------|-------------|----------------|
| length_mm | Integer | Optional | Vehicle length | dimension_specs |
| width_mm | Integer | Optional | Vehicle width | dimension_specs |
| height_mm | Integer | Optional | Vehicle height | dimension_specs |
| wheelbase_mm | Integer | Optional | Wheelbase | dimension_specs |
| ground_clearance_mm | Integer | Optional | Ground clearance | dimension_specs |
| boot_space_l | Integer | Optional | Boot capacity | dimension_specs |
| kerb_weight_kg | Integer | Optional | Vehicle kerb weight | dimension_specs |
| turning_radius_m | Float | Optional | Minimum turning radius | dimension_specs |
| seating_capacity | Integer | ✅ | Number of seats | vehicles |
| doors | Integer | Optional | Number of doors | vehicles |

---

# Category 5 — Safety

| Field | Data Type | Required | Description | Database Table |
|--------|-----------|----------|-------------|----------------|
| airbags | Integer | Optional | Number of airbags | safety_specs |
| abs | Boolean | Optional | Anti-lock Braking System | safety_specs |
| esc | Boolean | Optional | Electronic Stability Control | safety_specs |
| traction_control | Boolean | Optional | Traction Control | safety_specs |
| hill_hold_control | Boolean | Optional | Hill Hold Assist | safety_specs |
| hill_descent_control | Boolean | Optional | Hill Descent Control | safety_specs |
| isofix | Boolean | Optional | ISOFIX child seat mounts | safety_specs |
| tpms | Boolean | Optional | Tyre Pressure Monitoring System | safety_specs |
| blind_spot_monitor | Boolean | Optional | Blind Spot Monitoring | safety_specs |
| lane_keep_assist | Boolean | Optional | Lane Keep Assist | safety_specs |
| adaptive_cruise_control | Boolean | Optional | Adaptive Cruise Control | safety_specs |
| autonomous_emergency_braking | Boolean | Optional | Automatic Emergency Braking | safety_specs |
| adas_level | Integer | Optional | ADAS capability level | safety_specs |
| safety_rating | Float | Optional | NCAP safety rating | safety_specs |

---

# Category 6 — Features & Comfort

| Field | Data Type | Required | Description | Database Table |
|--------|-----------|----------|-------------|----------------|
| android_auto | Boolean | Optional | Android Auto support (wired) | feature_specs |
| apple_carplay | Boolean | Optional | Apple CarPlay support (wired) | feature_specs |
| wireless_android_auto | Boolean | Optional | Wireless Android Auto | feature_specs |
| wireless_apple_carplay | Boolean | Optional | Wireless Apple CarPlay | feature_specs |
| touchscreen_size_in | Float | Optional | Infotainment screen size (inches) | feature_specs |
| digital_instrument_cluster | Boolean | Optional | Digital instrument cluster | feature_specs |
| climate_control | Boolean | Optional | Automatic climate control | feature_specs |
| ventilated_seats | Boolean | Optional | Ventilated seats | feature_specs |
| powered_driver_seat | Boolean | Optional | Powered driver seat | feature_specs |
| sunroof | Boolean | Optional | Sunroof | feature_specs |
| panoramic_sunroof | Boolean | Optional | Panoramic sunroof | feature_specs |
| wireless_charging | Boolean | Optional | Wireless charging | feature_specs |
| keyless_entry | Boolean | Optional | Keyless entry | feature_specs |
| push_button_start | Boolean | Optional | Push-button start | feature_specs |
| cruise_control | Boolean | Optional | Cruise control | feature_specs |
| parking_camera | Boolean | Optional | Reverse camera | feature_specs |
| camera_360 | Boolean | Optional | 360° surround camera | feature_specs |
| parking_sensors | Boolean | Optional | Parking sensors | feature_specs |

---

# Category 7 — Ownership & Maintenance

| Field | Data Type | Required | Description | Database Table |
|--------|-----------|----------|-------------|----------------|
| warranty_years | Integer | Optional | Standard warranty (years) | ownership_specs |
| warranty_km | Integer | Optional | Standard warranty (km) | ownership_specs |
| extended_warranty_available | Boolean | Optional | Extended warranty option | ownership_specs |
| service_interval_km | Integer | Optional | Recommended service interval | ownership_specs |
| roadside_assistance | Boolean | Optional | RSA availability | ownership_specs |
| estimated_service_cost_per_year | Decimal | Optional | Approximate annual maintenance cost (₹) | ownership_specs |

---

# Category 8 — Availability

| Field | Data Type | Required | Description | Database Table (Future) |
|--------|-----------|----------|-------------|-------------------------|
| launch_year | Integer | Optional | Official launch year | availability_specs |
| current_status | Enum | Optional | Active / Discontinued | availability_specs |
| booking_open | Boolean | Optional | Booking availability | availability_specs |
| waiting_period_weeks | Integer | Optional | Approximate waiting period | availability_specs |

---

# Category 9 — Environmental

| Field | Data Type | Required | Description | Database Table (Future) |
|--------|-----------|----------|-------------|-------------------------|
| emission_standard | Enum | Optional | BS6, BS6 Phase 2, etc. | environmental_specs |
| co2_emissions_gkm | Float | Optional | CO₂ emissions (g/km) | environmental_specs |
| battery_capacity_kwh | Float | Optional | Battery capacity (kWh) | environmental_specs |
| electric_range_km | Integer | Optional | Certified EV range (km) | environmental_specs |
| charging_time_ac_hr | Float | Optional | AC charging time (hours) | environmental_specs |
| charging_time_dc_min | Integer | Optional | DC fast charging time (minutes) | environmental_specs |

---

# Data Quality Standards

## Missing Values

- Store missing values as `NULL`.
- Never use `"N/A"`, `"-"`, `"Unknown"` or empty strings.

## Units

| Measurement | Standard Unit |
|------------|---------------|
| Price | ₹ |
| Engine | cc |
| Power | bhp |
| Torque | Nm |
| Mileage | km/l |
| Length | mm |
| Weight | kg |
| Fuel Tank | litres |
| Battery | kWh |

## Canonical Formatting

Brand names should be standardized:

- `TATA`
- `tata`
- ` Tata `

↓

`Tata`

Fuel types:

- Petrol
- Diesel
- CNG
- Electric
- Hybrid
- Plugin Hybrid

Transmission:

- Manual
- Automatic
- AMT
- CVT
- DCT

Drivetrain:

- FWD
- RWD
- AWD
- 4WD

Boolean values:

- TRUE
- FALSE

---

# Version History

| Version | Description |
|----------|-------------|
| v1.0 | Initial Master Dataset Field Dictionary |
| v1.1 | Removed `price_category` and `vehicle_type` (derived fields). Moved `fuel_type` to Category 1 (Vehicle Identity) with note on intentional denormalization. Retained `fuel_tank_capacity_l` in Category 3 (Engine & Performance). Added Derived Fields section to Design Principles. Added `Drivetrain` to Canonical Formatting. Updated `Plugin Hybrid` in fuel type list. |