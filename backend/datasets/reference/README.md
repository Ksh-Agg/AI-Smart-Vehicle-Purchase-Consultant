# Reference Dataset

Purpose

This directory contains all canonical lookup tables used by the ETL pipeline.

These datasets define the allowed values throughout the system.

Rules

- Never modify IDs
- Never reuse IDs
- Append only
- Deprecated values remain for backwards compatibility
- Canonical names are immutable
- Display names may change

Consumers

- ETL
- PostgreSQL seeders
- FastAPI
- Recommendation Engine
- Frontend Dropdowns