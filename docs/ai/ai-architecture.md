# SVPC agent backend implementation plan

Status: implementation-ready; both grilling rounds are resolved.

## 1. Goal and first release boundary

Build a guided-first, Maruti-only consultation workflow that:

1. converts a user's message into a validated preference profile;
2. retrieves matching variants from the existing normalized PostgreSQL catalogue;
3. produces a preliminary catalogue-fit shortlist with deterministic Python scoring;
4. enriches that shortlist with maintenance, fuel, insurance, finance, warranty,
   resale, and service-network evidence;
5. calculates ownership cost and the final rank in deterministic Python;
6. explains the ranked result with traceable evidence; and
7. persists consultations, preferences, shortlists, and interrupt/resume state
   across application restarts.

The LLM may interpret preferences, choose specialist tools, generate read-only
catalogue queries, research, and explain. It must not invent catalogue facts,
calculate the final rank, or write SQL-backed catalogue data.

## 2. Documentation-driven decisions

The design follows these LangChain/LangGraph recommendations:

- Break the process into nodes with one responsibility, store raw data in state,
  format prompts inside nodes, route explicitly, retry transient failures, use
  `interrupt()` for user-fixable gaps, and let unexpected errors surface:
  [Thinking in LangGraph](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph).
- Use `create_agent` only where a ReAct tool loop is useful. A deterministic query,
  calculation, or route remains a Python function:
  [Agents](https://docs.langchain.com/oss/python/langchain/agents).
- Keep generated SQL read-only, limited, schema-aware, and error-correctable:
  [SQL agent](https://docs.langchain.com/oss/python/langchain/sql-agent).
- Use a checkpointer for thread-scoped state and a Store only for information that
  must cross threads:
  [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence) and
  [Memory](https://docs.langchain.com/oss/python/langgraph/add-memory).
- Keep structured catalogue facts in SQL. Reserve RAG for brochures, warranty
  documents, manuals, policies, and other unstructured material. RAG indexing is
  load, split, embed, and store; retrieval output is treated as untrusted data:
  [RAG with Deep Agents](https://docs.langchain.com/oss/python/deepagents/rag).
- Do not add a second LLM supervisor over the LangGraph workflow. The supervisor
  pattern is useful for distinct domains with substantial toolsets, while a single
  agent is preferred for a few tools:
  [Subagent personal assistant](https://docs.langchain.com/oss/python/langchain/multi-agent/subagents-personal-assistant).
- Do not add `deepagents` to the first release. Its sandbox, filesystem, planning,
  and artifact workflow is useful for open-ended file analysis, but the vehicle
  ranker does not execute user-authored code or create analysis artifacts:
  [Data analysis agent](https://docs.langchain.com/oss/python/deepagents/data-analysis).

## 3. Implemented repository baseline

- FastAPI, SQLAlchemy, Psycopg, Alembic, and the normalized catalogue models exist.
- The catalogue schema has brands, models, variants, city prices, powertrain,
  physical, safety, comfort, infotainment, lighting, and connected specifications.
- The idempotent catalogue importer is implemented; loading the supplied workbook
  requires an explicit reviewed source-header mapping and a configured database.
- Consultation/shortlist persistence, the PGVector indexing command, LangGraph
  checkpoint setup, and the agent API are implemented.
- The frontend uses the real SSE consultation contract and Maruti/India fields;
  the simulated event source has been removed.
- Deployment still requires real database/Gemini credentials, applying migrations,
  checkpoint setup, catalogue import, and an approved official-document manifest.

## 4. Proposed graph

```text
START
  -> parse_request [structured LLM call]
      -> clarify_preferences [interrupt] -> parse_request
      -> query_catalogue [SQL ReAct agent]
          -> validate_candidates [Python + parameterized SQL]
              -> request_relaxation [interrupt] -> query_catalogue
              -> score_catalogue_fit [Python]
                  -> retrieve_official_documents [RAG ReAct agent]
                  -> research_current_costs [Gemini Google Search agent]
                      -> calculate_ownership_cost [Python]
                          -> final_rank [Python]
                              -> synthesize [structured LLM call] -> END
```

The graph is the orchestrator. It does not need a separate supervisor agent.
Routing nodes return `Command` values so destinations and state updates stay
explicit. Only essential static edges are added in `graph.py`.

### Node contracts

| Node | Kind | Reads | Writes / routes |
| --- | --- | --- | --- |
| `parse_request` | structured LLM | latest message, saved profile | raw intent, profile patch, missing fields, research needs |
| `clarify_preferences` | Python + `interrupt()` | missing fields | resumed user values, then `parse_request` |
| `query_catalogue` | SQL ReAct agent | validated profile, city | successful read-only query payload and proposed variant IDs |
| `validate_candidates` | Python/data | proposed IDs, validated profile, city | authoritative candidate rows; rejects invalid IDs/facts and routes to relaxation if none |
| `request_relaxation` | Python + `interrupt()` | failed constraints | approved/edited constraints or `END` |
| `score_catalogue_fit` | Python | profile, candidate rows | preliminary scorecards and shortlist IDs |
| `retrieve_official_documents` | ReAct retrieval agent | shortlist and ownership questions | cited brochure/manual/warranty evidence |
| `research_current_costs` | Gemini with Google Search | city, shortlist, ownership inputs | current cited cost evidence and explicit gaps |
| `calculate_ownership_cost` | Python | usage assumptions and cost evidence | cost components, five-year total, confidence |
| `final_rank` | Python | fit scores, cost scores, evidence coverage | final scorecards and ordered recommendation IDs |
| `synthesize` | structured LLM | profile, scorecards, cost breakdowns, evidence | recommendation payload and user-facing answer |

`interrupt()` must be the first side-effecting operation in its node because a
resumed node restarts from its beginning.

## 5. State design

`ConsultationState` extends message state and contains only values that must cross
node boundaries:

```text
messages               append-only conversation messages
intent                 recommendation | compare | catalogue_question | follow_up
profile                raw validated preference values
profile_missing        unresolved required fields
ownership_inputs       annual distance, tenure, finance, insurance, and fuel assumptions
catalogue_query        checked SQL text and non-sensitive execution metadata
proposed_candidate_ids IDs emitted by the last successful SQL query tool call
candidates             raw database result dictionaries
catalogue_scorecards   per-variant preliminary fit scores
ownership_costs        component estimates, five-year total, and confidence
scorecards             final dimension scores, evidence coverage, and total score
ranked_variant_ids     ordered identifiers
document_evidence      retrieved chunks plus document metadata
web_evidence           URLs, citations, source type, and retrieval timestamps
recommendations        structured final recommendation objects
recoverable_error      error intended for a retrying agent or the user
```

Do not put prompts, formatted prompt text, database sessions, model clients,
`thread_id`, `kshagg_id`, or duplicate derivable values in graph state. `thread_id`
belongs in `configurable`; identity/locale/request metadata belongs in a typed
runtime context, while the user-editable city remains in `profile`. The SQL agent
receives the validated typed profile, never the raw user message, which reduces
prompt-injection and accidental query-scope expansion.

## 6. Ranking boundary

Ranking is deterministic Python, not an LLM judgment.

1. Require a city and budget for each consultation. Apply Maruti brand, active
   variant, the user-provided budget ceiling, and explicitly mandatory seating as
   hard constraints. Fuel type and transmission are soft preferences.
2. Convert `Low`, `Medium`, and `High` priorities into numeric weights and normalize
   them to sum to one.
3. Score only dimensions backed by database columns. Initial dimensions should be
   budget fit, efficiency, safety, space/utility, performance, and features.
4. Score SQL `NULL` as the neutral midpoint (`0.5`) and expose a separate evidence
   coverage/confidence value. Never turn unknown into `False` or zero.
5. Return every dimension score, source fields, weight, and exclusion reason so the
   LLM can explain the result without reconstructing it.
6. Select a small preliminary shortlist, enrich it with ownership evidence, then
   calculate TCO and rerank. The final response must fit within 120 seconds.

No fuzzy-logic package is needed initially. Small monotonic or piecewise scoring
functions cover the first release and are easier to audit. Add fuzzy membership
functions only when product rules require gradual preference bands that the simple
functions cannot express.

## 7. Tools and agent boundaries

### Catalogue tools

- `get_variant_details(variant_ids, city)` fetches only columns needed downstream.
- `compare_variants(variant_ids, dimensions, city)` returns aligned raw values.
- `validate_candidate_ids(variant_ids, profile, city)` reapplies brand, active,
  city, price, seating, and row-limit rules with SQLAlchemy bound parameters.

These Python tools hydrate and validate facts after the SQL agent has identified
candidates. They are the authority for scoring input.

### SQL ReAct agent

`sql_agent.py` builds a LangChain ReAct agent with the standard SQL toolkit and the
shared `ChatGoogleGenerativeAI` model. It gets the four documented capabilities:
list allowed tables, inspect schema, check a query, and execute a query. It is
restricted to one migration-defined `agent_vehicle_catalogue` view that flattens
the current normalized Maruti catalogue for retrieval; checkpoint, consultation,
RAG, and PostgreSQL system tables are invisible.

The database connection uses a `catalogue_agent_readonly` role with `SELECT` only,
a transaction set to read-only, a statement timeout, and a row limit. The system
prompt also forbids DML/DDL and requires query checking, but database permissions
remain the actual security boundary. Query errors are returned to the agent for the
documented correction loop.

The agent's final structured result contains proposed variant IDs, its query, and
any unresolved filter. It does not supply authoritative values directly to scoring:
`validate_candidates` re-fetches those IDs and reapplies hard constraints through
parameterized SQLAlchemy expressions. A fabricated or stale ID therefore produces
no candidate rather than a fabricated recommendation.

### RAG research agent

RAG searches only an approved unstructured corpus. Each chunk retains document
title, canonical URL/file ID, publication/effective date, vehicle/model metadata,
and page/section. The agent must cite retrieved sources and treat chunk content as
data, not instructions. Database catalogue values win if a document disagrees with
the current structured catalogue; the disagreement is surfaced rather than hidden.

### Web research agent

Use the native Google Search tool exposed by `ChatGoogleGenerativeAI` and bind it
with `model.bind(tools=[{"google_search": {}}], ...)` so the native JSON response
schema can be supplied alongside search. It uses the existing
`langchain-google-genai` package and API key, performs live search, and returns
citations. No Tavily, Google CSE, or separate search dependency is needed. The
integration follows the official
[Gemini Google Search](https://ai.google.dev/gemini-api/docs/google-search)
contract.

Queries use `site:` qualifiers for the approved domains below, and returned citation
URLs are validated before their facts enter state. Unsupported or unapproved sources
may be shown as secondary reading but cannot supply ranking inputs. Every accepted
fact stores its retrieval time and applicable city/model/variant.

## 8. Holistic data-source policy

| Dimension | Primary source | Treatment in the engine |
| --- | --- | --- |
| Variant, equipment, dimensions, ARAI efficiency | populated catalogue plus current Maruti model/brochure pages | Structured database facts win; documents explain them. |
| City price and offers | Maruti price list/dealer quote pages | Use stored city price; live offers are timestamped and never assumed guaranteed. |
| Warranty and service schedule | [Maruti warranty](https://www.marutisuzuki.com/corporate/media/press-releases/2024/july/maruti-suzuki-announces-enhanced-warranty-programmes) and [owner manuals](https://www.marutisuzuki.com/arena/car-manuals) | RAG evidence keyed by model, fuel type, model year, and effective date. |
| Periodic maintenance | [Maruti Service Cost Calculator](https://www.marutisuzuki.com/arena/service/service-cost-summary) | Store itemized indicative estimates by city, model, odometer, and service interval. |
| Safety | [Bharat NCAP fact sheets](https://www.bncap.in/vehicle-safety-rating/), then official manufacturer material | Store rating, tested variant, year, and applicability; never copy a rating to unlisted variants. |
| Finance | [Maruti Suzuki Smart Finance](https://www.marutisuzuki.com/arena/arena-finance) or a user-provided sanctioned quote | Calculate EMI from principal, rate, and term; do not invent a rate when no quote is available. |
| Insurance | User/dealer quote through [Maruti Insurance](https://www.marutisuzuki.com/more-from-us/insurance) | Personalized quote is authoritative; otherwise return a clearly labeled estimate/range. |
| Fuel/energy | user-entered local price, then an approved official price source | Calculate from annual distance and database efficiency; record price date and city. |
| Resale/depreciation | [Maruti True Value](https://www.marutisuzukitruevalue.com/truevaluehub/a-word-of-trust/ai-based-scientific-pricing-engine) live comparables | Estimate from comparable model/year/city/mileage cohorts; label it non-guaranteed. |
| Service accessibility | [Maruti service locator](https://www.marutisuzuki.com/service) | Use count/distance for the user's location, not marketing claims. |

Approved web domains begin with `marutisuzuki.com`, `marutisuzukitruevalue.com`,
and `bncap.in`. Additional government or financier domains must be added explicitly
to configuration and documented with the fact type they are allowed to supply.

“Everything” does not mean silently fabricating unavailable inputs. If a personalized
finance, insurance, or resale value cannot be obtained, the engine returns an
assumption or range, lowers confidence, and shows the unresolved input.

## 9. Files to add

First implementation slice:

```text
backend/app/agentic/
  __init__.py          # export the compiled graph entrypoint only
  state.py             # ConsultationState, runtime context, structured LLM outputs
  prompts.py           # load and validate YAML once
  prompts.yaml         # all system prompts keyed by node/agent
  tools.py             # constrained DB tools and tool result schemas
  sql_agent.py         # read-only SQL ReAct agent over the catalogue view
  research_agent.py    # RAG and native Gemini Google Search agent factories
  nodes.py             # node functions and Command routing
  graph.py             # StateGraph assembly and compilation

backend/app/schemas/consultation.py
                       # request, resume, event, and recommendation API models
backend/app/api/v1/routes/consultations.py
                       # thread creation, message stream, and interrupt resume routes
backend/app/db/models/consultation.py
                       # durable session metadata, profile, and shortlist records
backend/alembic/versions/<revision>_consultations_and_rag.py
                       # app/RAG tables, vector extension, and catalogue agent view
backend/scripts/ingest_catalogue.py
                       # idempotent XLSX-to-catalogue ingestion command
backend/scripts/index_maruti_documents.py
                       # explicit offline official-document indexing command
```

RAG construction stays in `tools.py` initially; a separate `retrieval.py` is added
only if indexing and runtime retrieval make that file unwieldy. Files intentionally
not added: `supervisor.py`, a provider abstraction, one file per node, a custom agent
base class, custom memory wrappers, custom retry wrappers, or a new
service/repository layer. Existing config, SQLAlchemy session, and models are reused
directly.

## 10. Prompt layout

Start with one `prompts.yaml` rather than one YAML file per prompt:

```text
intake.system
sql_agent.system
rag_agent.system
web_agent.system
synthesis.system
```

`intake.system` extracts a typed preference patch and asks no questions itself.
`sql_agent.system` contains the documented SQL-agent sequence and the catalogue
view/limit/read-only rules; it never contains credentials or user values.
`rag_agent.system` restricts retrieval to the indexed official corpus and requires
page-level citations. `web_agent.system` restricts live facts to the configured
domains, date/city/model scope, and a typed evidence result. `synthesis.system`
explains the deterministic scorecards and is forbidden to change their ordering.

`prompts.py` loads the file with `yaml.safe_load`, verifies these five keys at
startup, and returns strings. Dynamic user/state values are passed as messages or
structured context at invocation time. They are not stored in YAML or interpolated
into the system prompt. Split the YAML only when independent ownership or size
makes the single file painful.

## 11. Persistence and memory

- Use `AsyncPostgresSaver` because FastAPI and graph streaming are asynchronous.
- Compile the graph once during application lifespan with the live checkpointer.
- Run `checkpointer.setup()` as an explicit deployment/migration step, not on every
  request.
- Use a UUID `thread_id` (well below the documented 255-character limit) and reuse
  it for every turn and resume call in one consultation.
- Add an application-owned `consultations` table keyed by `thread_id`, indexed by
  `kshagg_id`, with title, status, latest profile snapshot, last-message summary,
  timestamps, and latest recommended variant IDs. LangGraph checkpoint tables are
  execution history; they are not the query model for the frontend sidebar.
- Add a `consultation_shortlist_items` table keyed by consultation and variant so a
  user's compare shortlist survives restarts independently of graph checkpoints.
- Keep score/evidence snapshots in the checkpointed state for the first slice.
  Normalize recommendation-run history only when the UI needs multiple historical
  result sets within one consultation.
- Use the catalogue connection with read-only credentials for agent tools and a
  separate write-capable connection for checkpoint tables.
- Define checkpoint retention before production; checkpoints otherwise accumulate.
- Do not add a cross-thread LangGraph Store until the meaning and ownership of
  `kshagg_id` are confirmed. Durable consultations do not require cross-thread
  preference memory.

## 12. API and frontend event contract

Minimal endpoints:

```text
POST /api/v1/consultations
GET  /api/v1/consultations?kshagg_id=...
GET  /api/v1/consultations/{thread_id}
POST /api/v1/consultations/{thread_id}/messages
POST /api/v1/consultations/{thread_id}/resume
PUT  /api/v1/consultations/{thread_id}/shortlist/{variant_id}
DELETE /api/v1/consultations/{thread_id}/shortlist/{variant_id}
```

Creation returns the server-created `thread_id`; history queries are scoped to the
resolved `kshagg_id`. The detail endpoint rebuilds the workspace from the app-owned
session metadata plus the latest LangGraph checkpoint. Shortlist writes are simple
idempotent HTTP operations and do not run the graph.

The message and resume endpoints return an SSE stream from FastAPI
`StreamingResponse`. The frontend uses `fetch` plus the native readable stream; no
new streaming dependency is needed. Map LangGraph events into a small stable API:

```text
node_start, node_end
tool_start, tool_end
message_delta
interrupt
final
error
```

Do not stream hidden chain-of-thought. The current Thinking UI receives curated
progress summaries such as node names, tool calls, counts, durations, and retry
status. The `interrupt` event carries the checkpoint/thread identifiers and typed
approval payload; `/resume` invokes the graph with `Command(resume=...)`.

The frontend integration replaces `simulateLangGraphConsultationStream`, changes
vehicle types to the backend schema, uses INR/city pricing and Maruti fuel types,
loads persisted consultations/shortlists, and sends approval decisions to `/resume`
instead of updating local state only.

## 13. Dependencies and configuration

Add only the first-slice packages:

```text
langchain
langgraph
langchain-google-genai        # ChatGoogleGenerativeAI + Gemini embeddings
langchain-community           # documented SQLDatabaseToolkit implementation
langgraph-checkpoint-postgres
langchain-postgres            # PGVector integration
langchain-text-splitters
pyyaml
openpyxl                      # catalogue XLSX ingestion only
pypdf                         # official PDF text extraction only
```

The SQL agent uses `SQLDatabaseToolkit` from `langchain-community`; query execution
still uses the installed SQLAlchemy/Psycopg stack. Native Gemini Google Search needs
no second search SDK or API key. Do not add `deepagents` in the first slice.

Replace the Compose database image with an official PGVector PostgreSQL 18 image
and enable `CREATE EXTENSION IF NOT EXISTS vector` in the migration. Use
`GoogleGenerativeAIEmbeddings` for text embeddings; start with the stable text-only
embedding model unless image-based brochure retrieval becomes a real requirement.

Add these settings to `app/core/config.py`:

```text
GEMINI_CHAT_MODEL
GEMINI_EMBEDDING_MODEL
AGENT_TOP_K_PRELIMINARY
AGENT_TOP_K_FINAL
AGENT_TIMEOUT_SECONDS=120
CATALOGUE_STATEMENT_TIMEOUT_MS
RAG_COLLECTION_NAME
CHECKPOINT_DATABASE_URL          # optional override; defaults to the app database
ALLOWED_RESEARCH_DOMAINS
```

Keep `ChatGoogleGenerativeAI` as the only chat model integration. `graph.py` creates
one configured chat model and passes it to node/agent factories; do not add a
provider interface for one provider. Accepted initial defaults are
`gemini-3.7-flash` for chat and `gemini-embedding-001` for text embeddings, pinned
in configuration rather than scattered through code. There is no separate monetary
request cap in development; top-K, tool-call limits, and the 120-second deadline
bound usage.

## 14. Error policy

- Retry transient database/network/rate-limit failures at the node with LangGraph
  `RetryPolicy` and a timeout.
- Return tool/schema/query errors to the ReAct agent so it can correct its action.
- Pause with `interrupt()` for missing user information or proposed relaxation.
- End with an honest partial answer when optional RAG/web evidence is unavailable.
- At 120 seconds, return the deterministic catalogue ranking plus any completed
  enrichment, mark missing dimensions, and allow the user to request a refresh.
- Let programming errors and unknown exceptions bubble to FastAPI logging.
- Never catch broad exceptions merely to turn them into a recommendation.

## 15. Implementation sequence

1. Inspect the source workbook, write a column-to-table mapping, decide how rows
   acquire the stable `catalogue_id`, and document rejected/unknown columns.
2. Add an idempotent ingestion command using natural-key upserts; load a small
   manually inspected sample and then the complete current Maruti catalogue.
3. Freeze the preference, ownership-input, scorecard, evidence, recommendation,
   interrupt, and SSE schemas, including price basis and top-K.
4. Add the dependencies/settings above, change Compose to PGVector, and add one
   migration for consultation/shortlist/RAG tables, the vector extension, the
   flattened catalogue view, and its read-only grants.
5. Run LangGraph checkpoint setup as a deployment step and attach one
   `AsyncPostgresSaver` for the FastAPI application lifespan.
6. Implement `state.py`, `prompts.yaml`, and `prompts.py`, using typed structured
   output from `ChatGoogleGenerativeAI` for intake and synthesis.
7. Implement `sql_agent.py` with the standard SQL toolkit over the single allowed
   view, then implement parameterized candidate hydration/validation, hard filters,
   neutral-null handling, and deterministic preliminary scoring.
8. Index the approved official Maruti/Bharat NCAP corpus with source, page,
   effective-date, and applicability metadata; implement the narrow RAG agent.
9. Implement the native Gemini Google Search agent and validate returned citations
   against the allowed domain/fact-type policy.
10. Implement deterministic ownership calculations and final reranking, then
    assemble the graph and its interrupt/retry/partial-result routes.
11. Add consultation history, message/resume streaming, and shortlist API routes.
12. Replace frontend mock data/streaming with the real India/Maruti API contract and
    restore sessions/shortlists from the backend.
13. Manually verify ingestion totals, a streamed guided consultation, restart
    recovery, criteria relaxation, shortlist persistence, citations, and the
    120-second partial-result path.

Per request, this plan contains no automated-test phase. Verification will be
manual through database inspection, streamed API calls, interrupt/resume flows, and
the connected frontend.

## 16. Accepted product defaults

- The first release is guided-first and includes a read-only SQL ReAct agent for
  dynamic catalogue queries.
- The catalogue database is empty, so ingestion is phase zero.
- `kshagg_id` is spelled exactly that way and begins as a backend-issued opaque UUID
  in a first-party cookie. It identifies browser-local history; it does not create
  cross-thread preference memory or promise cross-device identity.
- City and the hard budget are supplied per consultation. The budget applies to a
  current on-road city price; a missing on-road value uses a labeled estimate and
  provisional affordability. Fuel and transmission are soft preferences.
- Only city and maximum budget block the graph. Seats are hard only when explicitly
  mandatory. Missing annual distance and ownership horizon use visible assumptions
  of 10,000 km/year and five years; finance, insurance, and fuel-price inputs remain
  optional.
- Missing specification values contribute a neutral score and lower confidence.
- “Holistic” covers the full purchase/ownership set in section 8. Affordability is a
  hard gate; other weights follow user priorities, and safety is hard only when the
  user sets a minimum.
- Official public Maruti/Bharat NCAP documents may be downloaded and indexed. Do not
  scrape OTP/session-protected calculators; use a user/dealer value or official API.
- Live research uses Gemini's native Google Search with useful sources documented
  and constrained by fact type.
- Every chat/agent call uses `ChatGoogleGenerativeAI`.
- Enrich the top five catalogue matches and return the final top three.
- Consultations, checkpoints, and shortlists survive restarts. Development retains
  them until explicit deletion; production retention remains a deployment policy.
- Corpus refresh starts as a manual checksummed indexing command.
- The end-to-end deadline is 120 seconds. A timeout returns completed evidence and
  the deterministic catalogue ranking as an explicitly partial result.
- Criteria relaxation is the only approval action. Test-drive booking is deferred
  until an actual booking provider exists.

No product decision currently blocks phase-zero ingestion or backend implementation.
