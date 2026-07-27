# ADR 002: ETL Architecture Design

## Status
Proposed & Approved

## Context
In Phase 4 of the Smart Vehicle Purchase Consultant (SVPC) project, we require a robust, modular, and extensible ETL (Extract, Transform, Load) framework. The framework must ingest raw automotive specifications from varying sources (e.g. Kaggle datasets, manufacturer brochures, web scrapers) in formats like CSV, JSON, and Excel, and load them into a normalized PostgreSQL database schema.

To support rapid source onboarding and prevent high code maintenance overhead, the ETL pipeline needs to be source-agnostic. Hardcoding column names, schema relationships, or validation logic on a per-source basis is not acceptable.

---

## Design Decisions

### 1. Strongly Typed Canonical Models
- **Decision:** We use strongly typed Pydantic models (`CanonicalBrand`, `CanonicalVehicle`, and various specification models grouped under `CanonicalVehicleDataset`) as intermediate data transfer objects (DTOs) between the transform, validation, and load layers, instead of passing around raw untyped dictionaries.
- **Rationale:** 
  - Catches typing and structural mismatches early (Stage 1 validation).
  - Guarantees downstream pipeline stages (validators and loaders) interact with a consistent, self-documenting data contract.
  - Prevents silent errors caused by key typos or missing nested properties.

### 2. Registry-Based Mapping Architecture
- **Decision:** Each incoming data source registers a declarative configuration mapping raw keys to canonical target attributes (`mapping_registry.register()`).
- **Rationale:** 
  - Prevents the ETL pipeline from hardcoding field mappings.
  - Onboarding a new vehicle data source does not require writing custom pipeline scripts or altering core load/validation logic; it is a simple configuration task.

### 3. Two-Stage Validation Pipeline
- **Decision:** Validation is separated into:
  - **Stage 1 (Pydantic Validation):** Enforces data types, constraint boundaries, and schema structures.
  - **Stage 2 (Business Validation):** Executes semantic business rules such as duplicate detection in batch, validation of database-level numeric ranges, and foreign key existence.
- **Rationale:** 
  - Decoupling validation from parsing ensures type validation and logic checks remain independent.
  - Standardized, batch-level validation accumulates structured validation diagnostics in a `ValidationReport` rather than failing the execution on the first exception. This allows developers to inspect all data import issues in a single log report.

### 4. Dependency-Ordered Database Loading
- **Decision:** A centralized `LoaderOrchestrator` coordinates writing validated records using SQLAlchemy ORM, explicitly enforcing entity loading order (Brand -> Vehicle -> Specification Tables).
- **Rationale:** 
  - Resolves foreign key dependency constraints at runtime.
  - Bundles operations into transactional batch chunks, enabling automatic commits on success and complete rollbacks on failure to avoid database pollution or partial state corruption.

---

## Design Consequences & Trade-offs

### Pros
- **High Extensibility:** Adding a source only requires writing a flat configuration schema mapping.
- **Excellent Maintainability:** Changing schema constraints or validation rules in the future only requires editing single, isolated modules (e.g., `validators/numeric.py`).
- **Robust Telemetry:** Pipeline logs execution reports containing exact processed, skipped, validation failures, load counts, and throughput metrics.

### Cons
- **Slight Memory Overhead:** Instantiating Pydantic objects for every row in a batch chunk takes slightly more memory than iterating over flat dictionaries. However, this is mitigated by configured batch sizes (default 100 records).
