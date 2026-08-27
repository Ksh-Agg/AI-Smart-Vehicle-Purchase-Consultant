## SVPC backend

The backend is a FastAPI application with a durable LangGraph consultation workflow.
It uses `ChatGoogleGenerativeAI` for intake, the SQL/RAG agents, live Google Search,
and final synthesis. Catalogue and ownership scoring remain deterministic Python.

### Local setup

1. Copy the repository `.env.example` to `.env` and set `DATABASE_PASSWORD` and
   `GEMINI_API_KEY`.
2. Start PostgreSQL with `docker compose up -d postgres` from the repository root.
3. From `backend/`, run `uv run alembic upgrade head`.
4. Run `uv run python -m scripts.setup_agent_storage` once to create the LangGraph
   checkpoint tables.
5. Start the API with `uv run uvicorn app.main:app --reload`.

Production should set `CATALOGUE_AGENT_DATABASE_URL` to a PostgreSQL login that has
membership in the migration-created `catalogue_agent_readonly` role. The SQL agent
can see only `agent_vehicle_catalogue`; Python validates its returned variant IDs
before scoring.

### Catalogue ingestion

The importer never guesses workbook headers. First inspect them:

```bash
uv run python -m scripts.ingest_catalogue "../database/SVPC_master_dataset (1).xlsx" --headers
```

Create a JSON object mapping each printed source header to its canonical database
column, then run:

```bash
uv run python -m scripts.ingest_catalogue "../database/SVPC_master_dataset (1).xlsx" --mapping catalogue-mapping.json
```

Use `--deactivate-missing` only when the workbook is an authoritative full snapshot.

### Official-document RAG

Create a reviewed JSON manifest containing local official PDFs:

```json
[
  {
    "path": "../database/documents/example.pdf",
    "source_url": "https://www.marutisuzuki.com/example.pdf",
    "title": "Document title",
    "effective_date": "2026-08-27",
    "model": "Dzire"
  }
]
```

Then run `uv run python -m scripts.index_maruti_documents manifest.json`. Only the
domains configured in `ALLOWED_RESEARCH_DOMAINS` are accepted.

Implementation references:

- [Thinking in LangGraph](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph)
- [LangGraph memory and Postgres checkpointers](https://docs.langchain.com/oss/python/langgraph/add-memory)
- [LangChain SQL agent](https://docs.langchain.com/oss/python/langchain/sql-agent)
- [ChatGoogleGenerativeAI](https://docs.langchain.com/oss/python/integrations/chat/google_generative_ai)
- [LangChain PGVector](https://docs.langchain.com/oss/python/integrations/vectorstores/pgvector)
- [Gemini Google Search](https://ai.google.dev/gemini-api/docs/google-search)
