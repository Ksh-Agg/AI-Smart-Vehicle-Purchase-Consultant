# Data Acquisition Strategy

## Purpose

This document defines how the SVPC master dataset is populated, validated, and maintained.

---

# Source Priority

Priority 1
Manufacturer Official Website

Priority 2
Official Brochure / PDF

Priority 3
ARAI

Priority 4
Bharat NCAP / Global NCAP

Priority 5
CarDekho

Priority 6
CarWale

Priority 7
ZigWheels

Priority 8
Autocar India

Priority 9
Manual Research

---

# Field Source Mapping

| Field | Primary Source | Secondary Source |
|--------|----------------|------------------|
| brand | Manufacturer | CarDekho |
| model | Manufacturer | CarDekho |
| variant | Manufacturer | Brochure |
| price_ex_showroom | Manufacturer | CarDekho |
| engine_cc | Manufacturer | Brochure |
| mileage_kmpl | ARAI | Manufacturer |
| power_bhp | Manufacturer | Brochure |
| torque_nm | Manufacturer | Brochure |
| airbags | Manufacturer | Brochure |
| adas_level | Manufacturer | CarDekho |
| safety_rating | Bharat NCAP | Global NCAP |
| battery_capacity_kwh | Manufacturer | Brochure |
| charging_time_ac_hr | Manufacturer | CarDekho |

---

# Conflict Resolution

Manufacturer wins.

If unavailable:

Manufacturer Brochure wins.

If unavailable:

ARAI / NCAP.

Only then use automotive portals.

---

# Missing Data

Never invent values.

Unknown fields remain empty.

---

# Manual Verification

Fields requiring manual verification:

- waiting_period_weeks
- service_cost
- resale_score
- maintenance_score

---

# Data Refresh

Price
Monthly

Waiting Period
Weekly

Safety Ratings
When updated

Specifications
Quarterly

---

# Dataset Versioning

master-dataset-v1.csv

master-dataset-v2.csv

master-dataset-v3.csv

Older datasets remain archived.