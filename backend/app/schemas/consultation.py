"""Consultation API contracts."""

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

from app.agentic.state import PreferenceProfile


class CreateConsultationRequest(BaseModel):
    title: str = Field(default="New consultation", min_length=1, max_length=120)
    profile: PreferenceProfile = Field(default_factory=PreferenceProfile)


class ConsultationSummary(BaseModel):
    thread_id: UUID
    title: str
    status: Literal["active", "completed", "saved"]
    last_message_summary: str
    vehicle_count: int
    updated_at: datetime


class ConsultationCreated(BaseModel):
    thread_id: UUID
    profile: PreferenceProfile


class ConsultationDetail(ConsultationSummary):
    profile: PreferenceProfile
    messages: list[dict[str, str]]
    recommendations: list[dict[str, object]]
    shortlisted_variant_ids: list[int]


class MessageRequest(BaseModel):
    message: str = Field(min_length=1, max_length=8_000)


class ResumeRequest(BaseModel):
    decision: Literal["approved", "modified", "rejected"] | None = None
    message: str | None = Field(default=None, max_length=8_000)
    profile_patch: dict[str, object] = Field(default_factory=dict)
