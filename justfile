# Set dotenv loading
set dotenv-load := true

# List available recipes
default:
    @just --list

# Setup database, migrations, checkpoint storage, and dependencies
# ponytail: assumes docker and bun are available locally; upgrades DB directly without lock checks
setup:
    @test -f .env || cp .env.example .env
    docker compose up -d postgres
    cd backend && uv run alembic upgrade head
    cd backend && uv run python -m scripts.setup_agent_storage
    cd frontend && bun install

# Automatically setup and run frontend and backend together
dev: setup
    @just run-servers

# Run frontend and backend concurrently
[parallel]
run-servers: backend frontend

# Start FastAPI backend
backend:
    cd backend && uv run uvicorn app.main:app --reload

# Start Vite React frontend
frontend:
    cd frontend && bun run dev
