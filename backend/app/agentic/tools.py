"""Deterministic database, scoring, and ownership-cost operations."""

from __future__ import annotations

from decimal import Decimal
from math import pow
from typing import Any

from sqlalchemy import bindparam, text
from sqlalchemy.orm import Session

from app.agentic.state import Evidence, OwnershipCost, PreferenceProfile, Scorecard

FEATURE_FIELDS = (
    "air_conditioner",
    "rear_ac_vents",
    "keyless_entry",
    "push_button_start",
    "cruise_control",
    "driver_seat_height_adjustment",
    "touchscreen",
    "android_auto",
    "apple_carplay",
    "bluetooth",
    "navigation",
    "wireless_charging",
    "hud",
)
SAFETY_FIELDS = (
    "abs",
    "ebd",
    "esp",
    "hill_hold_control",
    "isofix_child_seat_anchors",
    "rear_parking_sensors",
    "parking_camera",
)


def _plain(value: object) -> object:
    if isinstance(value, Decimal):
        return float(value)
    return value


def _rows(result: Any) -> list[dict[str, object]]:
    return [
        {key: _plain(value) for key, value in row._mapping.items()}
        for row in result
    ]


def validate_candidate_ids(
    session: Session,
    variant_ids: list[int],
    profile: PreferenceProfile,
    limit: int,
) -> list[dict[str, object]]:
    """Re-fetch proposed IDs and enforce every hard constraint."""
    if not variant_ids or not profile.city or profile.max_budget is None:
        return []
    conditions = [
        "variant_id IN :variant_ids",
        "lower(city) = lower(:city)",
        "COALESCE(on_road_price, ex_showroom_price) <= :max_budget",
    ]
    params: dict[str, object] = {
        "variant_ids": variant_ids,
        "city": profile.city,
        "max_budget": profile.max_budget,
        "limit": limit,
    }
    if profile.mandatory_seats is not None:
        conditions.append("seating_capacity >= :mandatory_seats")
        params["mandatory_seats"] = profile.mandatory_seats
    statement = text(
        "SELECT * FROM agent_vehicle_catalogue WHERE "
        + " AND ".join(conditions)
        + " ORDER BY COALESCE(on_road_price, ex_showroom_price), variant_id LIMIT :limit"
    ).bindparams(bindparam("variant_ids", expanding=True))
    return _rows(session.execute(statement, params))


def fallback_candidate_ids(
    session: Session, profile: PreferenceProfile, limit: int
) -> list[int]:
    """Return safe candidates only when the SQL agent failed before querying."""
    if not profile.city or profile.max_budget is None:
        return []
    conditions = [
        "lower(city) = lower(:city)",
        "COALESCE(on_road_price, ex_showroom_price) <= :max_budget",
    ]
    params: dict[str, object] = {
        "city": profile.city,
        "max_budget": profile.max_budget,
        "limit": limit,
    }
    if profile.mandatory_seats is not None:
        conditions.append("seating_capacity >= :mandatory_seats")
        params["mandatory_seats"] = profile.mandatory_seats
    rows = session.execute(
        text(
            "SELECT variant_id FROM agent_vehicle_catalogue WHERE "
            + " AND ".join(conditions)
            + " ORDER BY COALESCE(on_road_price, ex_showroom_price) LIMIT :limit"
        ),
        params,
    )
    return [int(row.variant_id) for row in rows]


def get_variant_details(
    session: Session, variant_ids: list[int], city: str
) -> list[dict[str, object]]:
    if not variant_ids:
        return []
    statement = text(
        "SELECT * FROM agent_vehicle_catalogue "
        "WHERE variant_id IN :variant_ids AND lower(city) = lower(:city)"
    ).bindparams(bindparam("variant_ids", expanding=True))
    return _rows(session.execute(statement, {"variant_ids": variant_ids, "city": city}))


def _normalize(value: float | int | None, values: list[float], higher: bool = True) -> float:
    if value is None:
        return 0.5
    if not values or min(values) == max(values):
        return 0.5
    scaled = (float(value) - min(values)) / (max(values) - min(values))
    return scaled if higher else 1 - scaled


def _boolean_score(row: dict[str, object], fields: tuple[str, ...]) -> float:
    values = [0.5 if row.get(field) is None else float(bool(row[field])) for field in fields]
    return sum(values) / len(values)


def score_catalogue(
    candidates: list[dict[str, object]], profile: PreferenceProfile
) -> list[Scorecard]:
    """Score raw catalogue facts; SQL NULL is neutral and lowers confidence."""
    if not candidates:
        return []
    efficiency_values = [
        float(value)
        for row in candidates
        if (value := row.get("mileage_arai_kmpl") or row.get("mileage_arai_kmkg"))
        is not None
    ]
    space_values = [
        float(value)
        for row in candidates
        if (value := row.get("bootspace_litres")) is not None
    ]
    power_values = [
        float(value)
        for row in candidates
        if (value := row.get("max_power_bhp")) is not None
    ]
    priority_value = {"low": 1.0, "medium": 2.0, "high": 3.0}
    weights = {
        "budget": 3.0,
        "efficiency": priority_value[profile.priorities.efficiency],
        "safety": priority_value[profile.priorities.safety],
        "space": priority_value[profile.priorities.space],
        "performance": priority_value[profile.priorities.performance],
        "features": priority_value[profile.priorities.features],
    }
    if profile.preferred_fuels or profile.preferred_transmissions:
        weights["preference_match"] = 2.0
    weight_total = sum(weights.values())
    scorecards: list[Scorecard] = []
    evidence_fields = (
        "on_road_price",
        "mileage_arai_kmpl",
        "mileage_arai_kmkg",
        "airbag_count",
        "bootspace_litres",
        "max_power_bhp",
        *SAFETY_FIELDS,
        *FEATURE_FIELDS,
    )
    for row in candidates:
        price = row.get("on_road_price") or row.get("ex_showroom_price")
        ratio = float(price) / profile.max_budget if price and profile.max_budget else 1
        budget = max(0.0, min(1.0, (1 - ratio) / 0.4)) if ratio > 0.6 else 1.0
        # ponytail: compare each available official efficiency unit as-is for v1;
        # split fuel-specific curves when mixed-fuel data proves this materially wrong.
        efficiency_value = row.get("mileage_arai_kmpl") or row.get("mileage_arai_kmkg")
        safety = (
            _boolean_score(row, SAFETY_FIELDS)
            + _normalize(row.get("airbag_count"), [2, 6])
        ) / 2
        seating = min(float(row.get("seating_capacity") or 3.5) / 7, 1)
        space = (
            _normalize(row.get("bootspace_litres"), space_values) + seating
        ) / 2
        dimensions = {
            "budget": budget,
            "efficiency": _normalize(efficiency_value, efficiency_values),
            "safety": safety,
            "space": space,
            "performance": _normalize(row.get("max_power_bhp"), power_values),
            "features": _boolean_score(row, FEATURE_FIELDS),
        }
        preference_checks = [
            not profile.preferred_fuels or row.get("fuel_type") in profile.preferred_fuels,
            not profile.preferred_transmissions
            or row.get("transmission_type") in profile.preferred_transmissions,
        ]
        if "preference_match" in weights:
            dimensions["preference_match"] = sum(preference_checks) / len(preference_checks)
        weighted = sum(dimensions[key] * weights[key] for key in weights) / weight_total
        known = sum(row.get(field) is not None for field in evidence_fields)
        scorecards.append(
            Scorecard(
                variant_id=int(row["variant_id"]),
                dimensions={key: round(value * 100, 1) for key, value in dimensions.items()},
                total=round(weighted * 100, 1),
                confidence=round(known / len(evidence_fields), 3),
            )
        )
    return sorted(scorecards, key=lambda card: card.total, reverse=True)


def _fact(
    evidence: list[Evidence], dimension: str, variant_id: int, model: str
) -> Evidence | None:
    exact = [
        fact
        for fact in evidence
        if fact.dimension == dimension and fact.variant_id == variant_id and fact.value is not None
    ]
    if exact:
        return exact[0]
    scoped = [
        fact
        for fact in evidence
        if fact.dimension == dimension
        and fact.value is not None
        and fact.model
        and fact.model.lower() == model.lower()
    ]
    return scoped[0] if scoped else next(
        (
            fact
            for fact in evidence
            if fact.dimension == dimension
            and fact.value is not None
            and fact.variant_id is None
            and fact.model is None
        ),
        None,
    )


def _period_cost(fact: Evidence | None, years: int) -> float | None:
    if not fact or fact.value is None:
        return None
    unit = (fact.unit or "").lower()
    if "month" in unit:
        return fact.value * 12 * years
    if "year" in unit or "annual" in unit:
        return fact.value * years
    return fact.value


def calculate_ownership_costs(
    candidates: list[dict[str, object]],
    profile: PreferenceProfile,
    raw_evidence: list[dict[str, object]],
) -> list[OwnershipCost]:
    evidence = [Evidence.model_validate(item) for item in raw_evidence]
    costs: list[OwnershipCost] = []
    for row in candidates:
        variant_id = int(row["variant_id"])
        model = str(row["model"])
        years = profile.ownership_years
        purchase = float(row.get("on_road_price") or row["ex_showroom_price"])
        assumptions: list[str] = []
        fuel_type = str(row.get("fuel_type") or "petrol")
        fuel_fact = _fact(evidence, f"fuel_price_{fuel_type}", variant_id, model)
        fuel_price = profile.local_fuel_price or (fuel_fact.value if fuel_fact else None)
        efficiency = row.get("mileage_arai_kmpl") or row.get("mileage_arai_kmkg")
        if fuel_type == "electric" and row.get("driving_range_km") and row.get("battery_capacity_kwh"):
            efficiency = float(row["driving_range_km"]) / float(row["battery_capacity_kwh"])
        fuel_cost = None
        if fuel_price and efficiency:
            fuel_cost = profile.annual_distance_km * years / float(efficiency) * float(fuel_price)
        else:
            assumptions.append("Fuel/energy cost excluded because price or efficiency is unavailable.")

        maintenance = _period_cost(
            _fact(evidence, "maintenance_cost", variant_id, model), years
        )
        insurance = (
            profile.annual_insurance_quote * years
            if profile.annual_insurance_quote is not None
            else _period_cost(_fact(evidence, "insurance_cost", variant_id, model), years)
        )
        resale_fact = _fact(evidence, "resale_value", variant_id, model)
        resale = resale_fact.value if resale_fact else None
        finance = None
        if profile.loan_rate_percent is not None and profile.loan_term_months:
            principal = max(0.0, purchase - float(profile.down_payment or 0))
            monthly_rate = profile.loan_rate_percent / 1200
            months = profile.loan_term_months
            if monthly_rate == 0:
                finance = 0.0
            else:
                emi = principal * monthly_rate * pow(1 + monthly_rate, months) / (
                    pow(1 + monthly_rate, months) - 1
                )
                finance = emi * months - principal

        components = [fuel_cost, maintenance, insurance, finance]
        total = purchase + sum(value for value in components if value is not None)
        if resale is not None:
            total -= resale
        else:
            assumptions.append("Resale value excluded; total cost is conservative.")
        available = sum(value is not None for value in [fuel_cost, maintenance, insurance, resale])
        costs.append(
            OwnershipCost(
                variant_id=variant_id,
                years=years,
                purchase_price=round(purchase, 2),
                fuel_energy_cost=round(fuel_cost, 2) if fuel_cost is not None else None,
                maintenance_cost=round(maintenance, 2) if maintenance is not None else None,
                insurance_cost=round(insurance, 2) if insurance is not None else None,
                finance_cost=round(finance, 2) if finance is not None else None,
                resale_value=round(resale, 2) if resale is not None else None,
                total_cost=round(total, 2),
                assumptions=assumptions,
                confidence=round(0.4 + available * 0.15, 2),
            )
        )
    return costs


def final_rank(
    fit_cards: list[Scorecard], costs: list[OwnershipCost]
) -> list[Scorecard]:
    cost_values = [cost.total_cost for cost in costs]
    by_cost = {cost.variant_id: cost for cost in costs}
    ranked: list[Scorecard] = []
    for fit in fit_cards:
        cost = by_cost[fit.variant_id]
        ownership_score = _normalize(cost.total_cost, cost_values, higher=False) * 100
        total = fit.total * 0.8 + ownership_score * 0.2
        ranked.append(
            Scorecard(
                variant_id=fit.variant_id,
                dimensions={**fit.dimensions, "ownership_cost": round(ownership_score, 1)},
                total=round(total, 1),
                confidence=round((fit.confidence + cost.confidence) / 2, 3),
            )
        )
    return sorted(ranked, key=lambda card: card.total, reverse=True)
