"""Read-only ReAct SQL agent for dynamic catalogue retrieval."""

from __future__ import annotations

import json
import re
from typing import Any

from langchain.agents import create_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import tool
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from app.agentic.prompts import prompt
from app.agentic.state import PreferenceProfile

VIEW_NAME = "agent_vehicle_catalogue"
FORBIDDEN_SQL = re.compile(
    r"\b(insert|update|delete|drop|alter|truncate|create|grant|revoke|copy|call|do|vacuum|analyze|refresh)\b",
    re.IGNORECASE,
)


def _sqlalchemy_url(url: str) -> str:
    return (
        url.replace("postgresql://", "postgresql+psycopg://", 1)
        if url.startswith("postgresql://")
        else url
    )


def build_sql_agent(
    model: BaseChatModel,
    database_url: str,
    top_k: int,
    statement_timeout_ms: int,
) -> tuple[Any, Engine]:
    """Build the documented four-tool SQL agent with guarded execution."""
    engine = create_engine(_sqlalchemy_url(database_url), pool_pre_ping=True)
    database = SQLDatabase(
        engine,
        include_tables=[VIEW_NAME],
        sample_rows_in_table_info=0,
        view_support=True,
    )
    toolkit = SQLDatabaseToolkit(db=database, llm=model)

    @tool("sql_db_query")
    def sql_db_query(query: str) -> str:
        """Execute one checked, read-only query against agent_vehicle_catalogue."""
        cleaned = query.strip().rstrip(";")
        if not re.match(r"^(select|with)\b", cleaned, re.IGNORECASE):
            return "Error: only SELECT or WITH queries are allowed."
        if FORBIDDEN_SQL.search(cleaned) or ";" in cleaned or "--" in cleaned or "/*" in cleaned:
            return "Error: mutating, multi-statement, and commented SQL is forbidden."
        if VIEW_NAME not in cleaned.lower():
            return f"Error: queries must use only {VIEW_NAME}."
        guarded = text(
            f"SELECT * FROM ({cleaned}) AS guarded_catalogue_query LIMIT {int(top_k)}"
        )
        try:
            with engine.connect() as connection, connection.begin():
                connection.execute(text("SET TRANSACTION READ ONLY"))
                connection.execute(
                    text("SELECT set_config('statement_timeout', :timeout, true)"),
                    {"timeout": f"{statement_timeout_ms}ms"},
                )
                result = connection.execute(guarded)
                payload = {
                    "query": cleaned,
                    "columns": list(result.keys()),
                    "rows": [list(row) for row in result.fetchall()],
                }
                return json.dumps(payload, default=str)
        except Exception as exc:  # returned to ReAct so the model can correct its query
            return f"Error: {exc}"

    tools = [
        sql_db_query if item.name == "sql_db_query" else item
        for item in toolkit.get_tools()
    ]
    agent = create_agent(
        model,
        tools,
        system_prompt=prompt(
            "sql_agent.system", view_name=VIEW_NAME, top_k=top_k
        ),
    )
    return agent, engine


async def query_candidates(
    agent: Any, profile: PreferenceProfile
) -> tuple[str, list[int], str]:
    """Run the agent and extract IDs only from its successful SQL tool payload."""
    response = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Find candidate variants for this validated profile:\n"
                        + profile.model_dump_json(exclude_none=True)
                    ),
                }
            ]
        },
        config={"recursion_limit": 16},
    )
    query = ""
    candidate_ids: list[int] = []
    summary = ""
    for message in response.get("messages", []):
        if isinstance(message, ToolMessage) and message.name == "sql_db_query":
            try:
                payload = json.loads(str(message.content))
            except (TypeError, json.JSONDecodeError):
                continue
            if not isinstance(payload, dict) or "rows" not in payload:
                continue
            query = str(payload.get("query", ""))
            for row in payload.get("rows", []):
                if isinstance(row, list) and row:
                    try:
                        candidate_ids.append(int(row[0]))
                    except (TypeError, ValueError):
                        continue
        elif isinstance(message, AIMessage) and not message.tool_calls:
            summary = message.text
    return query, list(dict.fromkeys(candidate_ids)), summary
