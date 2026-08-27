"""Typed state and structured model outputs for the recommendation graph."""

from dataclasses import dataclass
from typing import Literal

from langgraph.graph import MessagesState
from pydantic import BaseModel, Field

Priority = Literal["low", "medium", "high"]
FuelType = Literal["petrol", "cng", "hybrid", "electric"]
TransmissionType = Literal[
    "manual", "automatic", "amt", "torque_converter", "e_cvt"
]


class Priorities(BaseModel):
    safety: Priority = "high"
    efficiency: Priority = "medium"
    space: Priority = "medium"
    performance: Priority = "low"
    features: Priority = "medium"


class PreferenceProfile(BaseModel):
    city: str | None = None
    min_budget: int | None = Field(default=None, ge=0)
    max_budget: int | None = Field(default=None, gt=0)
    preferred_fuels: list[FuelType] = Field(default_factory=list)
    preferred_transmissions: list[TransmissionType] = Field(default_factory=list)
    mandatory_seats: int | None = Field(default=None, ge=1, le=20)
    primary_use: str | None = None
    annual_distance_km: int = Field(default=10_000, gt=0)
    ownership_years: int = Field(default=5, ge=1, le=15)
    local_fuel_price: float | None = Field(default=None, gt=0)
    down_payment: float | None = Field(default=None, ge=0)
    loan_rate_percent: float | None = Field(default=None, ge=0)
    loan_term_months: int | None = Field(default=None, ge=1, le=120)
    annual_insurance_quote: float | None = Field(default=None, ge=0)
    minimum_safety_rating: float | None = Field(default=None, ge=0, le=5)
    priorities: Priorities = Field(default_factory=Priorities)


class IntakeResult(BaseModel):
    intent: Literal[
        "recommendation", "compare", "catalogue_question", "follow_up"
    ] = "recommendation"
    profile: PreferenceProfile
    research_questions: list[str] = Field(default_factory=list)


class Evidence(BaseModel):
    dimension: str
    statement: str
    source_url: str
    title: str = ""
    page: int | None = None
    effective_date: str | None = None
    city: str | None = None
    model: str | None = None
    variant_id: int | None = None
    value: float | None = None
    unit: str | None = None
    confidence: float = Field(default=0.5, ge=0, le=1)


class WebResearchResult(BaseModel):
    facts: list[Evidence] = Field(default_factory=list)
    gaps: list[str] = Field(default_factory=list)


class Scorecard(BaseModel):
    variant_id: int
    dimensions: dict[str, float]
    total: float
    confidence: float


class OwnershipCost(BaseModel):
    variant_id: int
    years: int
    purchase_price: float
    fuel_energy_cost: float | None = None
    maintenance_cost: float | None = None
    insurance_cost: float | None = None
    finance_cost: float | None = None
    resale_value: float | None = None
    total_cost: float
    assumptions: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.5, ge=0, le=1)


class RecommendationNarrative(BaseModel):
    variant_id: int
    pros: list[str] = Field(default_factory=list)
    cons: list[str] = Field(default_factory=list)
    key_features: list[str] = Field(default_factory=list)


class SynthesisResult(BaseModel):
    answer: str
    narratives: list[RecommendationNarrative] = Field(default_factory=list)


class ConsultationState(MessagesState, total=False):
    intent: str
    profile: dict[str, object]
    profile_missing: list[str]
    research_questions: list[str]
    catalogue_query: str
    proposed_candidate_ids: list[int]
    candidates: list[dict[str, object]]
    catalogue_scorecards: list[dict[str, object]]
    document_evidence: list[dict[str, object]]
    web_evidence: list[dict[str, object]]
    evidence_gaps: list[str]
    ownership_costs: list[dict[str, object]]
    scorecards: list[dict[str, object]]
    ranked_variant_ids: list[int]
    recommendations: list[dict[str, object]]
    answer: str
    recoverable_error: str


@dataclass(frozen=True)
class RuntimeContext:
    kshagg_id: str
    locale: str = "en-IN"
