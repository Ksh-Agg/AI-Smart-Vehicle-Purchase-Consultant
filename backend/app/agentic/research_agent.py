"""Official-document RAG and Gemini Google Search agents."""

from __future__ import annotations

import json
from typing import Any
from urllib.parse import urlparse

from langchain.agents import create_agent
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector
from pydantic import ValidationError

from app.agentic.prompts import prompt
from app.agentic.state import Evidence, PreferenceProfile, WebResearchResult


def build_research_agent(
    model: BaseChatModel,
    database_url: str,
    api_key: str,
    embedding_model: str,
    collection_name: str,
) -> tuple[Any, PGVector]:
    """Build a ReAct agent around a narrow PGVector retrieval tool."""
    embeddings = GoogleGenerativeAIEmbeddings(
        model=embedding_model,
        api_key=api_key,
    )
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=collection_name,
        connection=database_url,
        use_jsonb=True,
    )

    @tool("search_official_documents")
    def search_official_documents(query: str) -> str:
        """Search indexed official Maruti Suzuki and Bharat NCAP documents."""
        documents = vector_store.similarity_search(query, k=5)
        chunks = [
            {
                "statement": document.page_content,
                "source_url": str(document.metadata.get("source_url", "")),
                "title": str(document.metadata.get("title", "")),
                "page": document.metadata.get("page"),
                "effective_date": document.metadata.get("effective_date"),
                "model": document.metadata.get("model"),
            }
            for document in documents
        ]
        return json.dumps(chunks, default=str)

    return (
        create_agent(
            model,
            [search_official_documents],
            system_prompt=prompt("rag_agent.system"),
        ),
        vector_store,
    )


async def retrieve_official_evidence(
    agent: Any,
    candidates: list[dict[str, object]],
    research_questions: list[str],
) -> list[Evidence]:
    shortlist = [
        {
            "variant_id": row["variant_id"],
            "model": row["model"],
            "variant_name": row["variant_name"],
            "fuel_type": row.get("fuel_type"),
            "model_year": row["model_year"],
        }
        for row in candidates
    ]
    response = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": json.dumps(
                        {
                            "shortlist": shortlist,
                            "questions": research_questions
                            or [
                                "warranty and exclusions",
                                "service schedule",
                                "safety applicability",
                            ],
                        }
                    ),
                }
            ]
        },
        config={"recursion_limit": 12},
    )
    evidence: list[Evidence] = []
    for message in response.get("messages", []):
        if not isinstance(message, ToolMessage) or message.name != "search_official_documents":
            continue
        try:
            chunks = json.loads(str(message.content))
        except (TypeError, json.JSONDecodeError):
            continue
        for chunk in chunks if isinstance(chunks, list) else []:
            if not chunk.get("source_url"):
                continue
            evidence.append(
                Evidence(
                    dimension="official_document",
                    statement=str(chunk.get("statement", "")),
                    source_url=str(chunk["source_url"]),
                    title=str(chunk.get("title", "")),
                    page=chunk.get("page"),
                    effective_date=chunk.get("effective_date"),
                    model=chunk.get("model"),
                    confidence=0.9,
                )
            )
    return evidence


def _allowed(url: str, domains: tuple[str, ...]) -> bool:
    hostname = (urlparse(url).hostname or "").lower()
    return any(hostname == domain or hostname.endswith(f".{domain}") for domain in domains)


async def research_current_costs(
    model: BaseChatModel,
    profile: PreferenceProfile,
    candidates: list[dict[str, object]],
    allowed_domains: tuple[str, ...],
) -> WebResearchResult:
    """Use Gemini native Google Search and native JSON-schema output together."""
    search_model = model.bind(
        tools=[{"google_search": {}}],
        response_mime_type="application/json",
        response_schema=WebResearchResult.model_json_schema(),
    )
    request = {
        "profile": profile.model_dump(exclude_none=True),
        "shortlist": [
            {
                "variant_id": row["variant_id"],
                "model": row["model"],
                "variant_name": row["variant_name"],
                "fuel_type": row.get("fuel_type"),
            }
            for row in candidates
        ],
        "required_dimensions": [
            "fuel_price_petrol/cng/electric as applicable",
            "maintenance_cost",
            "insurance_cost",
            "resale_value",
            "warranty",
            "service_network",
            "safety_rating",
        ],
        "allowed_domains": list(allowed_domains),
    }
    response = await search_model.ainvoke(
        [
            {"role": "system", "content": prompt("web_agent.system")},
            {"role": "user", "content": json.dumps(request)},
        ]
    )
    try:
        result = WebResearchResult.model_validate_json(response.text)
    except ValidationError:
        return WebResearchResult(gaps=["Google Search returned an invalid evidence schema."])
    accepted = [fact for fact in result.facts if _allowed(fact.source_url, allowed_domains)]
    rejected = len(result.facts) - len(accepted)
    gaps = list(result.gaps)
    if rejected:
        gaps.append(f"Rejected {rejected} fact(s) from unapproved source domains.")
    return WebResearchResult(facts=accepted, gaps=gaps)
