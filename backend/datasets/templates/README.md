# Master Vehicle Template

This directory contains the canonical CSV template used for importing vehicle data into the SVPC ETL pipeline.

## Purpose

The template defines the standard column layout expected by the ETL framework.

All external datasets (CSV, Excel, scraped data, OEM exports) should be transformed into this format before ingestion.

## Rules

- UTF-8 encoding
- Comma-separated values (CSV)
- One row per vehicle variant
- Do not rename column headers
- Leave optional fields blank if unknown
- Mandatory fields are validated during ETL

## Related Documents

- `docs/architecture/master-vehicle-schema.md`
- `docs/etl/master-dataset-field-dictionary.md`
- `datasets/specifications/master-dataset-specification.md`