"""Durable consultation, streaming, resume, and shortlist endpoints."""

from __future__ import annotations

import asyncio
import json
from time import monotonic
from typing import Any, AsyncIterator
from uuid import UUID, uuid4

from fastapi import APIRouter, Cookie, HTTPException, Request, Response, status
from fastapi.responses import StreamingResponse
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.types import Command
from sqlalchemy import delete, select

from app.agentic.state import PreferenceProfile, RuntimeContext
from app.api.dependencies.providers import SessionDep, SettingsDep
from app.db.models import Consultation, ConsultationShortlistItem, Variant
from app.db.session import SessionLocal
from app.schemas.consultation import (
    ConsultationCreated,
    ConsultationDetail,
    ConsultationSummary,
    CreateConsultationRequest,
    MessageRequest,
    ResumeRequest,
)

router = APIRouter(prefix="/consultations", tags=["Consultations"])
COOKIE_NAME = "kshagg_id"
NODE_NAMES = {
    "parse_request",
    "clarify_preferences",
    "query_catalogue",
    "validate_candidates",
    "request_relaxation",
    "score_catalogue_fit",
    "retrieve_official_documents",
    "research_current_costs",
    "calculate_ownership_cost",
    "final_rank",
    "synthesize",
}


def _identity(
    response: Response,
    settings: SettingsDep,
    raw: str | None,
) -> UUID:
    try:
        identity = UUID(raw) if raw else uuid4()
    except ValueError:
        identity = uuid4()
    response.set_cookie(
        COOKIE_NAME,
        str(identity),
        httponly=True,
        samesite="lax",
        secure=settings.ENVIRONMENT.value == "production",
        max_age=60 * 60 * 24 * 365,
    )
    return identity


def _owned_consultation(session: SessionDep, thread_id: UUID, identity: UUID) -> Consultation:
    consultation = session.get(Consultation, thread_id)
    if not consultation or consultation.kshagg_id != identity:
        raise HTTPException(status_code=404, detail="Consultation not found")
    return consultation


def _message_dict(message: object) -> dict[str, str]:
    if isinstance(message, BaseMessage):
        role = {"human": "user", "ai": "assistant"}.get(message.type, message.type)
        return {"role": role, "content": message.text}
    if isinstance(message, dict):
        return {
            "role": str(message.get("role", "system")),
            "content": str(message.get("content", "")),
        }
    return {"role": "system", "content": str(message)}


def _sse(event: str, payload: dict[str, object]) -> str:
    return f"event: {event}\ndata: {json.dumps({'type': event, **payload}, default=str)}\n\n"


async def _stream_graph(
    request: Request,
    thread_id: UUID,
    identity: UUID,
    graph_input: dict[str, object] | Command,
    timeout_seconds: int,
) -> AsyncIterator[str]:
    graph = request.app.state.graph
    config = {"configurable": {"thread_id": str(thread_id)}}
    timings: dict[str, float] = {}
    timed_out = False
    try:
        async with asyncio.timeout(timeout_seconds):
            async for event in graph.astream_events(
                graph_input,
                config=config,
                context=RuntimeContext(kshagg_id=str(identity)),
                version="v2",
            ):
                name = str(event.get("name", ""))
                kind = event.get("event")
                run_id = str(event.get("run_id", ""))
                if kind == "on_chain_start" and name in NODE_NAMES:
                    timings[run_id] = monotonic()
                    yield _sse("node_start", {"node": name})
                elif kind == "on_chain_end" and name in NODE_NAMES:
                    started = timings.pop(run_id, monotonic())
                    yield _sse(
                        "node_end",
                        {"node": name, "duration_ms": round((monotonic() - started) * 1000)},
                    )
                elif kind == "on_tool_start":
                    timings[run_id] = monotonic()
                    yield _sse("tool_start", {"tool": name, "run_id": run_id})
                elif kind == "on_tool_end":
                    started = timings.pop(run_id, monotonic())
                    yield _sse(
                        "tool_end",
                        {
                            "tool": name,
                            "run_id": run_id,
                            "duration_ms": round((monotonic() - started) * 1000),
                        },
                    )
    except TimeoutError:
        timed_out = True

    snapshot = await graph.aget_state(config)
    values = dict(snapshot.values or {})
    interrupts = list(getattr(snapshot, "interrupts", ()) or ())
    if interrupts:
        yield _sse(
            "interrupt",
            {"thread_id": str(thread_id), "payload": interrupts[0].value},
        )
        return

    recommendations = values.get("recommendations", [])
    answer = str(values.get("answer", ""))
    if timed_out:
        answer = answer or (
            "The 120-second research window ended. Here is the completed "
            "database-backed result; missing enrichment is marked as unavailable."
        )
    with SessionLocal() as session:
        consultation = session.get(Consultation, thread_id)
        if consultation:
            consultation.profile = dict(values.get("profile", consultation.profile))
            consultation.latest_recommended_variant_ids = [
                int(item["variant_id"]) for item in recommendations
            ]
            consultation.last_message_summary = answer[:240]
            consultation.status = "completed" if recommendations else "active"
            session.commit()
    yield _sse(
        "final",
        {
            "thread_id": str(thread_id),
            "answer": answer,
            "profile": values.get("profile", {}),
            "recommendations": recommendations,
            "evidence_gaps": values.get("evidence_gaps", []),
            "partial": timed_out,
        },
    )


@router.post("", response_model=ConsultationCreated, status_code=status.HTTP_201_CREATED)
def create_consultation(
    body: CreateConsultationRequest,
    response: Response,
    session: SessionDep,
    settings: SettingsDep,
    kshagg_id: str | None = Cookie(default=None),
) -> ConsultationCreated:
    identity = _identity(response, settings, kshagg_id)
    consultation = Consultation(
        thread_id=uuid4(),
        kshagg_id=identity,
        title=body.title,
        status="active",
        profile=body.profile.model_dump(mode="json"),
        last_message_summary="Session started",
        latest_recommended_variant_ids=[],
    )
    session.add(consultation)
    session.commit()
    return ConsultationCreated(thread_id=consultation.thread_id, profile=body.profile)


@router.get("", response_model=list[ConsultationSummary])
def list_consultations(
    response: Response,
    session: SessionDep,
    settings: SettingsDep,
    kshagg_id: str | None = Cookie(default=None),
) -> list[ConsultationSummary]:
    identity = _identity(response, settings, kshagg_id)
    rows = session.scalars(
        select(Consultation)
        .where(Consultation.kshagg_id == identity)
        .order_by(Consultation.updated_at.desc())
    )
    return [
        ConsultationSummary(
            thread_id=row.thread_id,
            title=row.title,
            status=row.status,
            last_message_summary=row.last_message_summary,
            vehicle_count=len(row.latest_recommended_variant_ids),
            updated_at=row.updated_at,
        )
        for row in rows
    ]


@router.get("/{thread_id}", response_model=ConsultationDetail)
async def get_consultation(
    thread_id: UUID,
    request: Request,
    response: Response,
    session: SessionDep,
    settings: SettingsDep,
    kshagg_id: str | None = Cookie(default=None),
) -> ConsultationDetail:
    identity = _identity(response, settings, kshagg_id)
    consultation = _owned_consultation(session, thread_id, identity)
    snapshot = await request.app.state.graph.aget_state(
        {"configurable": {"thread_id": str(thread_id)}}
    )
    values = dict(snapshot.values or {})
    shortlist = session.scalars(
        select(ConsultationShortlistItem.variant_id).where(
            ConsultationShortlistItem.consultation_thread_id == thread_id
        )
    ).all()
    return ConsultationDetail(
        thread_id=consultation.thread_id,
        title=consultation.title,
        status=consultation.status,
        last_message_summary=consultation.last_message_summary,
        vehicle_count=len(consultation.latest_recommended_variant_ids),
        updated_at=consultation.updated_at,
        profile=PreferenceProfile.model_validate(
            values.get("profile", consultation.profile)
        ),
        messages=[_message_dict(item) for item in values.get("messages", [])],
        recommendations=list(values.get("recommendations", [])),
        shortlisted_variant_ids=list(shortlist),
    )


@router.post("/{thread_id}/messages")
def post_message(
    thread_id: UUID,
    body: MessageRequest,
    request: Request,
    response: Response,
    session: SessionDep,
    settings: SettingsDep,
    kshagg_id: str | None = Cookie(default=None),
) -> StreamingResponse:
    identity = _identity(response, settings, kshagg_id)
    consultation = _owned_consultation(session, thread_id, identity)
    if consultation.title == "New consultation":
        consultation.title = body.message[:120]
    consultation.last_message_summary = body.message[:240]
    consultation.status = "active"
    session.commit()
    stream = _stream_graph(
        request,
        thread_id,
        identity,
        {"messages": [HumanMessage(content=body.message)]},
        settings.AGENT_TIMEOUT_SECONDS,
    )
    return StreamingResponse(
        stream,
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.post("/{thread_id}/resume")
def resume_consultation(
    thread_id: UUID,
    body: ResumeRequest,
    request: Request,
    response: Response,
    session: SessionDep,
    settings: SettingsDep,
    kshagg_id: str | None = Cookie(default=None),
) -> StreamingResponse:
    identity = _identity(response, settings, kshagg_id)
    _owned_consultation(session, thread_id, identity)
    stream = _stream_graph(
        request,
        thread_id,
        identity,
        Command(resume=body.model_dump(exclude_none=True)),
        settings.AGENT_TIMEOUT_SECONDS,
    )
    return StreamingResponse(
        stream,
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.put("/{thread_id}/shortlist/{variant_id}", status_code=status.HTTP_204_NO_CONTENT)
def add_shortlist_item(
    thread_id: UUID,
    variant_id: int,
    response: Response,
    session: SessionDep,
    settings: SettingsDep,
    kshagg_id: str | None = Cookie(default=None),
) -> Response:
    identity = _identity(response, settings, kshagg_id)
    _owned_consultation(session, thread_id, identity)
    if not session.get(Variant, variant_id):
        raise HTTPException(status_code=404, detail="Variant not found")
    key = {"consultation_thread_id": thread_id, "variant_id": variant_id}
    if not session.get(ConsultationShortlistItem, key):
        session.add(ConsultationShortlistItem(**key))
        session.commit()
    response.status_code = status.HTTP_204_NO_CONTENT
    return response


@router.delete("/{thread_id}/shortlist/{variant_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_shortlist_item(
    thread_id: UUID,
    variant_id: int,
    response: Response,
    session: SessionDep,
    settings: SettingsDep,
    kshagg_id: str | None = Cookie(default=None),
) -> Response:
    identity = _identity(response, settings, kshagg_id)
    _owned_consultation(session, thread_id, identity)
    session.execute(
        delete(ConsultationShortlistItem).where(
            ConsultationShortlistItem.consultation_thread_id == thread_id,
            ConsultationShortlistItem.variant_id == variant_id,
        )
    )
    session.commit()
    response.status_code = status.HTTP_204_NO_CONTENT
    return response
