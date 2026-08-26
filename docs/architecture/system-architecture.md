# System architecture

SVPC is a small monorepo with three runtime boundaries:

```text
React + TypeScript ──HTTP──> FastAPI ──SQLAlchemy/Psycopg──> PostgreSQL
      bun                         uv                         Docker Compose
```

Docker Compose owns only the local PostgreSQL service and named volume. Alembic
migrations are deliberately manual. The initial database contains catalogue
tables only; ingestion, recommendations, users, and AI persistence are outside
the current implementation.
