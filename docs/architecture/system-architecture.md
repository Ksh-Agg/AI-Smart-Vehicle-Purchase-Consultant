# SVPC Backend Architecture Specification

## 1. System Overview
The Smart Vehicle Purchase Consultant (SVPC) backend is built with FastAPI, SQLAlchemy 2.0, Alembic, and PostgreSQL, designed to run recommendation engines and LLM-based query explanation layers.

## 2. High-Level Component Diagram
Refer to the [ETL Architecture Diagram](etl-architecture.md#2-execution-flow-diagram) for the ingestion component data flow.

## 3. Core Modules & Responsibilities
### 3.1 API & Routing Layer (`app/api`)
Handles REST requests and API routers.
### 3.2 Core Infrastructure (`app/core`, `app/config`)
Manages Pydantic Settings configuration, security tokens, and database engines.
### 3.3 Data Layer & Persistence (`app/models`, `app/repositories`)
SQLAlchemy declarative mapping ORM models. See the [Master Vehicle Schema Specification](master-vehicle-schema.md) for full details on tables, columns, and relations.
### 3.4 Business Logic (`app/services`)
Execution pipelines for recommendation queries and preference bound scoring.
### 3.5 AI & Inference Engine (`app/ai`)
Refer to the [AI Recommendation Engine Specification](../ai/ai-architecture.md) for details on feature scaling, preference inference, and RAG prompt generation.

## 4. Cross-Cutting Concerns
### 4.1 Exception Handling (`app/exceptions`)
### 4.2 Middleware (`app/middleware`)
### 4.3 Lifespan Management (`app/lifecycle`)
### 4.4 Observability & Monitoring (`app/monitoring`)

## 5. Security & Authentication Protocol
---
## Related Documentation
- [ETL Ingestion Architecture Specification](etl-architecture.md)
- [Master Vehicle Database Schema](master-vehicle-schema.md)
