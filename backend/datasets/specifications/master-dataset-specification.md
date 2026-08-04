# Master Dataset Specification

**Project:** Smart Vehicle Purchase Consultant (SVPC)  
**Status:** Ingestion Reference  
**Location:** `/datasets/`  

---

## 1. Directory Structure Purpose

The `datasets/` folder is dedicated to version-controlled dataset templates, samples, reference tables, and manual imports. It is strictly separated from the runtime `data/` folder, which holds temporary state and processing artifacts from ETL pipelines.

```
datasets/
├── specifications/
│   └── master-dataset-specification.md      # This file
├── templates/
│   └── master-vehicle-template.csv          # Reusable template matching all canonical attributes
├── samples/
│   ├── sample-vehicles.csv                  # Valid sample data for testing
│   └── sample-invalid-vehicles.csv          # Purposely malformed rows to check error reports
├── reference/
│   ├── brand-reference.csv                  # Standard list of manufacturers and countries
│   ├── vehicle-segments.csv                 # Allowed market segment labels
│   ├── fuel-types.csv                       # Standard fuel types
│   ├── body-types.csv                       # Body styles enums
│   └── transmission-types.csv               # Transmission configurations
└── imports/                                 # Manually curated sources ready for pipeline run
```

---

## 2. Ingestion Template Specification

The canonical CSV template under `templates/master-vehicle-template.csv` contains all fields defined in the [Master Dataset Field Dictionary](../../docs/etl/master-dataset-field-dictionary.md) in flat format. 

### Core Rules:
1. **Formatting:** Columns should not contain unit suffixes (e.g. use `1497` instead of `"1497 cc"`, and `16.8` instead of `"16.8 kmpl"`).
2. **Missing values:** Represent missing or inapplicable values with empty cells (which translate to database `NULL`).
3. **Boolean values:** Use `TRUE` or `FALSE` (case-insensitive) for feature flags.
4. **Enum values:** Values must match the predefined choices listed in [Master Vehicle Schema Canonical Enumerations](../../docs/architecture/master-vehicle-schema.md#canonical-enumerations).

---

## Related Documentation
- [System Architecture Specification](../../docs/architecture/system-architecture.md)
- [Master Dataset Field Dictionary](../../docs/etl/master-dataset-field-dictionary.md)
- [Master Vehicle Database Schema](../../docs/architecture/master-vehicle-schema.md)
