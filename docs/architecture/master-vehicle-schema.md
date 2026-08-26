# Catalogue schema

Status: implemented baseline

The database stores only the latest current vehicle catalogue. A stable
`catalogue_id` identifies each variant across updates; variants missing from a
future authoritative catalogue are marked inactive rather than deleted.

## Relationships

```text
brands ──< vehicle_models ──< variants
                               ├──< variant_prices
                               ├─── variant_powertrain_specs
                               ├──< variant_charging_options
                               ├──< variant_terrain_modes
                               ├─── variant_physical_specs
                               ├─── variant_safety_specs
                               ├─── variant_comfort_specs
                               ├─── variant_infotainment_specs
                               ├─── variant_lighting_specs
                               └─── variant_connected_specs
```

Specification tables are optional one-to-one children of `variants`.
Charging options, terrain modes, and city prices are one-to-many children.

## Core tables

### `brands`

Identity `BIGINT` primary key, case-insensitively unique nonblank name, and
creation/update timestamps.

### `vehicle_models`

Identity primary key, restricted brand foreign key, case-insensitively unique
name per brand, and timestamps.

### `variants`

Identity primary key, unique nonblank `catalogue_id`, restricted model foreign
key, trim, variant name, model year, active flag, and timestamps.

### `variant_prices`

Composite primary key `(variant_id, city)`, positive `NUMERIC(12,2)` ex-showroom
price, optional positive on-road price, and timestamps. Only current prices are
stored.

## Specification tables

- `variant_powertrain_specs`: fuel, transmission, drivetrain, mileage, engine,
  motor, battery, range, emissions, and battery warranty facts.
- `variant_charging_options`: typed AC/DC power, percentage window, and duration.
- `variant_terrain_modes`: one normalized mode per row.
- `variant_physical_specs`: chassis, suspension, dimensions, capacity, wheels,
  tyres, spare wheel, roof rails, and exterior tone.
- `variant_safety_specs`: ADAS, braking, airbags, parking, child protection, and
  warning equipment.
- `variant_comfort_specs`: climate, access, mirrors, windows, seating, cabin, and
  steering equipment.
- `variant_infotainment_specs`: media, phone integration, audio, ports,
  instruments, and driver displays.
- `variant_lighting_specs`: headlamps, fog lamps, DRLs, automatic lighting, and
  ambient lighting.
- `variant_connected_specs`: connected services, remote controls, tracking, and
  geofencing.

## Rules

- Internal relations use PostgreSQL identity `BIGINT` keys.
- Categories use lowercase `TEXT` codes with named `CHECK` constraints.
- Exact quantities use `NUMERIC`; counts and whole-unit measurements use integer
  types.
- Feature booleans are nullable, preserving true, false, and unknown.
- Brand/model deletion is restricted; variant-owned data cascades on deletion.
- No native enums, UUIDs, JSONB, EAV, history, user, AI, or recommendation tables.
- Deterministic values such as `four_wheel_drive`, `fast_charging`, and
  `curtain_airbags` are derived by the API rather than stored.

The clean baseline is revision `20260827_0001`.
