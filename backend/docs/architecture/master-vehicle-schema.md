# Master Vehicle Schema v1.0
**Project:** AI Smart Vehicle Purchase Consultant (SVPC)  
**Version:** 1.0  
**Status:** Draft (Phase 4.2)  
**Purpose:** Define the canonical vehicle data model used throughout the ETL pipeline, recommendation engine, and AI explanation layer.

---

# Overview

The Master Vehicle Schema serves as the **single source of truth** for all vehicle information within the Smart Vehicle Purchase Consultant.

Every external data source—whether CSV, Excel, CarDekho, CarWale, OEM APIs, or dealer management systems—must ultimately be transformed into this canonical schema before entering the PostgreSQL database.

This schema is intentionally **manufacturer-neutral**.

No business-specific logic (such as preferring Maruti Suzuki) should be stored here. Business strategies belong in the Recommendation Engine and Competition Intelligence modules.

---

# Design Principles

- Canonical representation of vehicle information
- Independent of data source
- Highly normalized
- Extensible for future vehicle technologies
- Suitable for recommendation systems
- Suitable for AI/RAG retrieval
- Suitable for analytics
- Suitable for comparison engines

---

# Entity Relationship Overview

```
Brand
   │
   │ 1:N
   ▼
Vehicle
   │
   ├────────────── Engine Specs
   ├────────────── Dimension Specs
   ├────────────── Safety Specs
   ├────────────── Feature Specs
   ├────────────── Ownership Specs
   ├────────────── Availability Specs
   └────────────── Environmental Specs
```

---

# 1. Brand

**Table:** `brands`

Represents the vehicle manufacturer.

| Field | Type | Description |
|--------|------|-------------|
| id | UUID | Primary Key |
| name | String | Brand name |
| slug | String | URL-friendly identifier |
| country | String | Country of origin |
| parent_company | String | Parent organization |
| founded_year | Integer | Brand establishment year |
| logo_url | String | Brand logo |
| website | String | Official website |
| is_active | Boolean | Soft delete flag |
| created_at | Timestamp | Record creation |
| updated_at | Timestamp | Last update |

---

# 2. Vehicle

**Table:** `vehicles`

Represents a specific vehicle variant.

## Identity

| Field | Type |
|---------|------|
| id | UUID |
| brand_id | UUID (FK) |
| model | String |
| variant | String |
| slug | String |

## Market Information

| Field | Type |
|---------|------|
| launch_year | Integer |
| discontinued | Boolean |
| price_ex_showroom | Decimal |
| segment | Enum |
| body_type | Enum |

## Configuration

| Field | Type |
|---------|------|
| seating_capacity | Integer |
| doors | Integer |
| drive_type | Enum |

## Powertrain

| Field | Type |
|---------|------|
| fuel_type | Enum |
| transmission | Enum |
| hybrid | Boolean |
| electric | Boolean |

## Performance Summary

| Field | Type |
|---------|------|
| power_bhp | Decimal |
| torque_nm | Decimal |
| mileage_kmpl | Decimal |
| boot_space_l | Decimal |

---

# 3. Engine Specifications

**Table:** `engine_specs`

Contains detailed engine and drivetrain information.

| Field | Type |
|---------|------|
| vehicle_id | UUID |
| engine_cc | Integer |
| cylinders | Integer |
| aspiration | Enum |
| engine_type | String |
| battery_capacity_kwh | Decimal |
| motor_power_kw | Decimal |
| charging_time_hours | Decimal |
| top_speed_kmph | Decimal |
| acceleration_0_100 | Decimal |
| emission_norm | Enum |

---

# 4. Dimension Specifications

**Table:** `dimension_specs`

Contains physical dimensions.

| Field | Type |
|---------|------|
| vehicle_id | UUID |
| length_mm | Decimal |
| width_mm | Decimal |
| height_mm | Decimal |
| wheelbase_mm | Decimal |
| ground_clearance_mm | Decimal |
| turning_radius_m | Decimal |
| kerb_weight_kg | Decimal |
| fuel_tank_capacity_l | Decimal |

---

# 5. Safety Specifications

**Table:** `safety_specs`

Contains passive and active safety features.

| Field | Type |
|---------|------|
| vehicle_id | UUID |
| airbags | Integer |
| abs | Boolean |
| ebd | Boolean |
| esc | Boolean |
| traction_control | Boolean |
| hill_hold | Boolean |
| hill_descent_control | Boolean |
| tpms | Boolean |
| iso_fix | Boolean |
| adas_level | Enum |
| camera_360 | Boolean |
| parking_sensors | Boolean |
| ncap_rating | Decimal |

---

# 6. Feature Specifications

**Table:** `feature_specs`

Contains comfort and infotainment features.

| Field | Type |
|---------|------|
| vehicle_id | UUID |
| sunroof | Boolean |
| panoramic_sunroof | Boolean |
| ventilated_seats | Boolean |
| wireless_android_auto | Boolean |
| wireless_apple_carplay | Boolean |
| connected_car | Boolean |
| cruise_control | Boolean |
| adaptive_cruise | Boolean |
| wireless_charger | Boolean |
| ambient_lighting | Boolean |
| hud | Boolean |
| digital_cluster | Boolean |
| premium_audio | Boolean |

---

# 7. Ownership Specifications

**Table:** `ownership_specs`

Captures ownership-related metrics.

| Field | Type |
|---------|------|
| vehicle_id | UUID |
| warranty_years | Integer |
| warranty_km | Integer |
| service_interval_km | Integer |
| annual_service_cost | Decimal |
| maintenance_score | Decimal |
| resale_score | Decimal |
| spare_parts_cost | Decimal |

---

# 8. Availability Specifications

**Table:** `availability_specs`

Stores market availability.

| Field | Type |
|---------|------|
| vehicle_id | UUID |
| waiting_period_days | Integer |
| cities_available | JSON |
| sales_channel | Enum |
| booking_open | Boolean |

---

# 9. Environmental Specifications

**Table:** `environmental_specs`

Stores environmental compliance information.

| Field | Type |
|---------|------|
| vehicle_id | UUID |
| co2_emission | Decimal |
| emission_norm | Enum |
| recyclable_material_percent | Decimal |

---

# Canonical Enumerations

## Fuel Type

- Petrol
- Diesel
- CNG
- Petrol + CNG
- Hybrid
- Strong Hybrid
- Electric

---

## Transmission

- Manual
- AMT
- CVT
- DCT
- Torque Converter
- e-CVT
- Single Speed

---

## Drive Type

- FWD
- RWD
- AWD
- 4WD

---

## Body Type

- Hatchback
- Sedan
- SUV
- Compact SUV
- Coupe SUV
- MPV
- MUV
- Pickup
- Van

---

## Vehicle Segment

- Entry Hatchback
- Premium Hatchback
- Compact Sedan
- Mid Sedan
- Premium Sedan
- Compact SUV
- Mid SUV
- Full Size SUV
- MPV
- Premium MPV
- EV

---

## ADAS Level

- None
- Level 1
- Level 2
- Level 2+
- Level 3

---

## Sales Channel

- Arena
- Nexa
- Dealer
- Online
- OEM Direct

---

# Data Flow

```
External Sources
   │
   ▼
Extract
   │
   ▼
Mapping
   │
   ▼
Transformation
   │
   ▼
Canonical Vehicle Schema
   │
   ▼
Validation
   │
   ▼
PostgreSQL
   │
   ▼
Recommendation Engine
   │
   ▼
LLM Explanation Layer
```

---

# Future Extensions

The schema is designed to support future enhancements without breaking compatibility.

Possible additions include:

- Insurance data
- Financing offers
- Dealer inventory
- Real-time pricing
- Crash test reports
- User reviews
- Ownership history
- Recall information
- Connected vehicle telemetry
- EV charging infrastructure
- AI-generated vehicle scores
- Market trend analytics

---

# Notes

- This schema intentionally remains **manufacturer-agnostic**.
- Manufacturer-specific business rules (e.g., Maruti Suzuki recommendation strategies) should be implemented in the Recommendation Engine, **not** in the database schema.
- All ETL connectors must map their source data into this canonical model before validation and persistence.
- The schema should evolve through versioned migrations as new vehicle technologies and business requirements emerge.

---

## Related Documentation
- [System Architecture Specification](system-architecture.md)
- [Master Dataset Field Dictionary](../etl/master-dataset-field-dictionary.md)
