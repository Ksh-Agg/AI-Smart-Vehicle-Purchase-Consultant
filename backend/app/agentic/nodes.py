"""LangGraph node implementations and explicit routing."""

from __future__ import annotations

import json
from typing import Any

from google.genai.errors import APIError
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.types import Command, interrupt
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from app.agentic.prompts import prompt
from app.agentic.research_agent import (
    research_current_costs as run_web_research,
)
from app.agentic.research_agent import retrieve_official_evidence
from app.agentic.sql_agent import query_candidates
from app.agentic.state import (
    ConsultationState,
    Evidence,
    IntakeResult,
    OwnershipCost,
    PreferenceProfile,
    RecommendationNarrative,
    Scorecard,
    SynthesisResult,
)
from app.agentic.tools import (
    FEATURE_FIELDS,
    calculate_ownership_costs,
    fallback_candidate_ids,
    final_rank,
    score_catalogue,
    validate_candidate_ids,
)
from app.core.config import Settings


def _latest_user_text(state: ConsultationState) -> str:
    for message in reversed(state.get("messages", [])):
        if isinstance(message, HumanMessage):
            return message.text
        if isinstance(message, dict) and message.get("role") == "user":
            return str(message.get("content", ""))
    return ""


def _profile(state: ConsultationState) -> PreferenceProfile:
    return PreferenceProfile.model_validate(state.get("profile", {}))


def _features(row: dict[str, object]) -> list[str]:
    labels = {
        "rear_ac_vents": "Rear AC vents",
        "keyless_entry": "Keyless entry",
        "push_button_start": "Push-button start",
        "cruise_control": "Cruise control",
        "touchscreen": "Touchscreen infotainment",
        "android_auto": "Android Auto",
        "apple_carplay": "Apple CarPlay",
        "wireless_charging": "Wireless charging",
        "hud": "Head-up display",
    }
    return [labels[field] for field in FEATURE_FIELDS if row.get(field) is True and field in labels]


def _fallback_narrative(card: Scorecard) -> RecommendationNarrative:
    ordered = sorted(card.dimensions.items(), key=lambda item: item[1], reverse=True)
    return RecommendationNarrative(
        variant_id=card.variant_id,
        pros=[f"Strong {name.replace('_', ' ')} fit ({value:.0f}/100)" for name, value in ordered[:2]],
        cons=[f"Lower {name.replace('_', ' ')} fit ({value:.0f}/100)" for name, value in ordered[-2:]],
    )


def make_nodes(
    model: BaseChatModel,
    sql_agent: Any,
    rag_agent: Any,
    session_factory: sessionmaker,
    settings: Settings,
) -> dict[str, Any]:
    intake_model = model.with_structured_output(IntakeResult, method="json_schema")
    synthesis_model = model.with_structured_output(SynthesisResult, method="json_schema")

    async def parse_request(state: ConsultationState) -> Command:
        existing = _profile(state)
        result = await intake_model.ainvoke(
            [
                {"role": "system", "content": prompt("intake.system")},
                {
                    "role": "user",
                    "content": json.dumps(
                        {
                            "existing_profile": existing.model_dump(exclude_none=True),
                            "latest_message": _latest_user_text(state),
                        }
                    ),
                },
            ]
        )
        profile = result.profile
        missing = [
            name
            for name, value in (("city", profile.city), ("max_budget", profile.max_budget))
            if value in (None, "")
        ]
        return Command(
            update={
                "intent": result.intent,
                "profile": profile.model_dump(mode="json"),
                "profile_missing": missing,
                "research_questions": result.research_questions,
                "recoverable_error": "",
            },
            goto="clarify_preferences" if missing else "query_catalogue",
        )

    def clarify_preferences(state: ConsultationState) -> Command:
        answer = interrupt(
            {
                "type": "missing_preferences",
                "title": "A little more information is needed",
                "description": "Please provide the missing values before catalogue search.",
                "missing_fields": state.get("profile_missing", []),
            }
        )
        content = (
            answer.get("message")
            if isinstance(answer, dict) and answer.get("message")
            else json.dumps(answer) if isinstance(answer, dict) else str(answer)
        )
        return Command(update={"messages": [HumanMessage(content=content)]}, goto="parse_request")

    async def query_catalogue(state: ConsultationState) -> Command:
        profile = _profile(state)
        try:
            query, ids, summary = await query_candidates(sql_agent, profile)
            return Command(
                update={
                    "catalogue_query": query,
                    "proposed_candidate_ids": ids,
                    "recoverable_error": "" if query else summary,
                },
                goto="validate_candidates",
            )
        except (APIError, SQLAlchemyError, ValidationError) as exc:
            with session_factory() as session:
                ids = fallback_candidate_ids(
                    session, profile, settings.AGENT_TOP_K_PRELIMINARY
                )
            return Command(
                update={
                    "catalogue_query": "deterministic fallback after SQL-agent failure",
                    "proposed_candidate_ids": ids,
                    "recoverable_error": str(exc),
                },
                goto="validate_candidates",
            )

    def validate_candidates(state: ConsultationState) -> Command:
        profile = _profile(state)
        with session_factory() as session:
            candidates = validate_candidate_ids(
                session,
                state.get("proposed_candidate_ids", []),
                profile,
                settings.AGENT_TOP_K_PRELIMINARY,
            )
        return Command(
            update={"candidates": candidates},
            goto="score_catalogue_fit" if candidates else "request_relaxation",
        )

    def request_relaxation(state: ConsultationState) -> Command:
        profile = _profile(state)
        answer = interrupt(
            {
                "type": "criteria_relaxation",
                "title": "No variants satisfy every hard constraint",
                "description": "Approve a 10% budget increase, modify the profile, or stop.",
                "current_budget": profile.max_budget,
                "suggested_budget": round((profile.max_budget or 0) * 1.1),
            }
        )
        decision = answer.get("decision", "rejected") if isinstance(answer, dict) else "rejected"
        if decision == "rejected":
            return Command(goto="synthesize")
        if decision == "modified" and isinstance(answer, dict) and answer.get("message"):
            return Command(
                update={"messages": [HumanMessage(content=str(answer["message"]))]},
                goto="parse_request",
            )
        patch = answer.get("profile_patch", {}) if isinstance(answer, dict) else {}
        if decision == "approved" and profile.max_budget:
            patch = {**patch, "max_budget": round(profile.max_budget * 1.1)}
        updated = PreferenceProfile.model_validate({**profile.model_dump(), **patch})
        return Command(
            update={"profile": updated.model_dump(mode="json")}, goto="query_catalogue"
        )

    def score_catalogue_fit(state: ConsultationState) -> Command:
        cards = score_catalogue(state.get("candidates", []), _profile(state))
        ordered = {card.variant_id: index for index, card in enumerate(cards)}
        candidates = sorted(
            state.get("candidates", []),
            key=lambda row: ordered.get(int(row["variant_id"]), len(ordered)),
        )
        return Command(
            update={
                "catalogue_scorecards": [card.model_dump(mode="json") for card in cards],
                "candidates": candidates,
            },
            goto="retrieve_official_documents",
        )

    async def retrieve_official_documents(state: ConsultationState) -> Command:
        try:
            evidence = await retrieve_official_evidence(
                rag_agent,
                state.get("candidates", []),
                state.get("research_questions", []),
            )
            update = {"document_evidence": [item.model_dump(mode="json") for item in evidence]}
        except (APIError, SQLAlchemyError, ValidationError) as exc:
            update = {
                "document_evidence": [],
                "evidence_gaps": [f"Official document retrieval unavailable: {exc}"],
            }
        return Command(update=update, goto="research_current_costs")

    async def research_current_costs(state: ConsultationState) -> Command:
        try:
            result = await run_web_research(
                model,
                _profile(state),
                state.get("candidates", []),
                settings.allowed_research_domains,
            )
            update = {
                "web_evidence": [item.model_dump(mode="json") for item in result.facts],
                "evidence_gaps": [*state.get("evidence_gaps", []), *result.gaps],
            }
        except (APIError, ValidationError) as exc:
            update = {
                "web_evidence": [],
                "evidence_gaps": [
                    *state.get("evidence_gaps", []),
                    f"Live research unavailable: {exc}",
                ],
            }
        return Command(update=update, goto="calculate_ownership_cost")

    def calculate_ownership_cost(state: ConsultationState) -> Command:
        profile = _profile(state)
        candidates = state.get("candidates", [])
        cards = [Scorecard.model_validate(item) for item in state.get("catalogue_scorecards", [])]
        gaps = list(state.get("evidence_gaps", []))
        if profile.minimum_safety_rating is not None:
            safety_facts = [
                Evidence.model_validate(item)
                for item in state.get("web_evidence", [])
                if item.get("dimension") == "safety_rating"
                and item.get("value") is not None
            ]
            eligible: set[int] = set()
            for row in candidates:
                variant_id = int(row["variant_id"])
                model_name = str(row["model"]).lower()
                if any(
                    fact.value is not None
                    and fact.value >= profile.minimum_safety_rating
                    and (
                        fact.variant_id == variant_id
                        or (fact.variant_id is None and (fact.model or "").lower() == model_name)
                    )
                    for fact in safety_facts
                ):
                    eligible.add(variant_id)
            candidates = [row for row in candidates if int(row["variant_id"]) in eligible]
            cards = [card for card in cards if card.variant_id in eligible]
            if not eligible:
                gaps.append("No candidate had a verified safety rating meeting the hard minimum.")
        costs = calculate_ownership_costs(
            candidates,
            profile,
            state.get("web_evidence", []),
        )
        return Command(
            update={
                "candidates": candidates,
                "catalogue_scorecards": [card.model_dump(mode="json") for card in cards],
                "ownership_costs": [cost.model_dump(mode="json") for cost in costs],
                "evidence_gaps": gaps,
            },
            goto="final_rank",
        )

    def rank_finalists(state: ConsultationState) -> Command:
        cards = final_rank(
            [Scorecard.model_validate(item) for item in state.get("catalogue_scorecards", [])],
            [OwnershipCost.model_validate(item) for item in state.get("ownership_costs", [])],
        )[: settings.AGENT_TOP_K_FINAL]
        return Command(
            update={
                "scorecards": [card.model_dump(mode="json") for card in cards],
                "ranked_variant_ids": [card.variant_id for card in cards],
            },
            goto="synthesize",
        )

    async def synthesize(state: ConsultationState) -> dict[str, object]:
        cards = [Scorecard.model_validate(item) for item in state.get("scorecards", [])]
        if not cards:
            answer = (
                "No current Maruti Suzuki variant matched the confirmed city and hard budget. "
                "The constraints were left unchanged."
            )
            return {"answer": answer, "recommendations": [], "messages": [AIMessage(content=answer)]}
        ranked_ids = [card.variant_id for card in cards]
        candidate_by_id = {
            int(row["variant_id"]): row for row in state.get("candidates", [])
        }
        cost_by_id = {
            int(cost["variant_id"]): cost for cost in state.get("ownership_costs", [])
        }
        payload = {
            "profile": state.get("profile", {}),
            "ranked_scorecards": [card.model_dump() for card in cards],
            "vehicles": [candidate_by_id[item] for item in ranked_ids],
            "ownership_costs": [cost_by_id[item] for item in ranked_ids],
            "document_evidence": [
                {**item, "statement": str(item.get("statement", ""))[:800]}
                for item in state.get("document_evidence", [])[:12]
            ],
            "web_evidence": state.get("web_evidence", [])[:20],
            "evidence_gaps": state.get("evidence_gaps", []),
        }
        try:
            synthesis = await synthesis_model.ainvoke(
                [
                    {"role": "system", "content": prompt("synthesis.system")},
                    {"role": "user", "content": json.dumps(payload, default=str)},
                ]
            )
        except (APIError, ValidationError):
            synthesis = SynthesisResult(
                answer="Here are the highest-ranked matches based on the confirmed profile and available evidence.",
                narratives=[_fallback_narrative(card) for card in cards],
            )
        narrative_by_id = {item.variant_id: item for item in synthesis.narratives}
        recommendations: list[dict[str, object]] = []
        for card in cards:
            row = candidate_by_id[card.variant_id]
            cost = cost_by_id[card.variant_id]
            narrative = narrative_by_id.get(card.variant_id) or _fallback_narrative(card)
            recommendations.append(
                {
                    "variant_id": card.variant_id,
                    "catalogue_id": row["catalogue_id"],
                    "brand": row["brand"],
                    "model": row["model"],
                    "variant_name": row["variant_name"],
                    "trim": row["trim"],
                    "model_year": row["model_year"],
                    "city": row["city"],
                    "price": row.get("on_road_price") or row["ex_showroom_price"],
                    "price_basis": "on_road" if row.get("on_road_price") else "provisional_ex_showroom",
                    "fuel_type": row.get("fuel_type"),
                    "transmission_type": row.get("transmission_type"),
                    "mileage_arai_kmpl": row.get("mileage_arai_kmpl"),
                    "mileage_arai_kmkg": row.get("mileage_arai_kmkg"),
                    "driving_range_km": row.get("driving_range_km"),
                    "max_power_bhp": row.get("max_power_bhp"),
                    "bootspace_litres": row.get("bootspace_litres"),
                    "seating_capacity": row.get("seating_capacity"),
                    "airbag_count": row.get("airbag_count"),
                    "score": card.total,
                    "confidence": card.confidence,
                    "score_breakdown": card.dimensions,
                    "ownership_cost": cost,
                    "pros": narrative.pros,
                    "cons": narrative.cons,
                    "key_features": narrative.key_features or _features(row),
                    "evidence_urls": list(
                        dict.fromkeys(
                            str(item["source_url"])
                            for item in [
                                *state.get("document_evidence", []),
                                *state.get("web_evidence", []),
                            ]
                            if item.get("source_url")
                            and (
                                item.get("variant_id") in (None, card.variant_id)
                                or not item.get("variant_id")
                            )
                        )
                    )[:8],
                }
            )
        return {
            "answer": synthesis.answer,
            "recommendations": recommendations,
            "messages": [AIMessage(content=synthesis.answer)],
        }

    return {
        "parse_request": parse_request,
        "clarify_preferences": clarify_preferences,
        "query_catalogue": query_catalogue,
        "validate_candidates": validate_candidates,
        "request_relaxation": request_relaxation,
        "score_catalogue_fit": score_catalogue_fit,
        "retrieve_official_documents": retrieve_official_documents,
        "research_current_costs": research_current_costs,
        "calculate_ownership_cost": calculate_ownership_cost,
        "final_rank": rank_finalists,
        "synthesize": synthesize,
    }
