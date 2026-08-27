"""Assemble the SVPC LangGraph workflow and its shared model clients."""

from typing import Any

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from app.agentic.nodes import make_nodes
from app.agentic.research_agent import build_research_agent
from app.agentic.sql_agent import build_sql_agent
from app.agentic.state import ConsultationState, RuntimeContext
from app.core.config import Settings


def build_graph(
    checkpointer: Any,
    session_factory: sessionmaker,
    settings: Settings,
) -> tuple[Any, Engine]:
    """Compile one durable graph and return its disposable SQL-agent engine."""
    model = ChatGoogleGenerativeAI(
        model=settings.GEMINI_CHAT_MODEL,
        api_key=settings.GEMINI_API_KEY,
        request_timeout=settings.AGENT_TIMEOUT_SECONDS,
        retries=2,
    )
    sql_agent, sql_engine = build_sql_agent(
        model,
        settings.catalogue_agent_database_url,
        settings.AGENT_TOP_K_PRELIMINARY,
        settings.CATALOGUE_STATEMENT_TIMEOUT_MS,
    )
    rag_agent, _ = build_research_agent(
        model,
        settings.database_url,
        settings.GEMINI_API_KEY,
        settings.GEMINI_EMBEDDING_MODEL,
        settings.RAG_COLLECTION_NAME,
    )
    nodes = make_nodes(model, sql_agent, rag_agent, session_factory, settings)
    workflow = StateGraph(ConsultationState, context_schema=RuntimeContext)
    for name, node in nodes.items():
        workflow.add_node(name, node)
    workflow.add_edge(START, "parse_request")
    workflow.add_edge("synthesize", END)
    return workflow.compile(checkpointer=checkpointer), sql_engine
