# Smart Vehicle Purchase Consultant

SVPC currently provides a React/TypeScript frontend, a FastAPI backend, and a
normalized PostgreSQL catalogue schema. Catalogue ingestion and recommendation
features will be added after their workflows are specified.

## Stack

- PostgreSQL 18 via Docker Compose
- FastAPI, SQLAlchemy 2, Psycopg 3, and Alembic managed with `uv`
- React 19, TypeScript, and Vite managed with `bun`

## Database

Create the local environment and start PostgreSQL:

```bash
cp .env.example .env
docker compose up -d
```

The Compose project starts PostgreSQL only. Apply migrations manually:

```bash
cd backend
uv run alembic upgrade head
```

To discard a local development database and rebuild the clean baseline:

```bash
docker compose down --volumes
docker compose up -d
cd backend && uv run alembic upgrade head
```

Removing the volume permanently deletes its local database contents.

## Backend

```bash
cd backend
uv sync
uv run fastapi dev app/main.py
```

## Frontend

```bash
cd frontend
bun install
bun run dev
```

## Checks

```bash
cd backend
uv run ruff check .
uv run mypy app
uv run pytest
```

See [the catalogue schema](docs/architecture/master-vehicle-schema.md) for the
approved table boundaries and database rules.
