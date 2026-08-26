"""Checks for the normalized catalogue metadata contract."""

from sqlalchemy import Boolean, Enum, Numeric

from app.db import models  # noqa: F401
from app.db.base import Base

EXPECTED_TABLES = {
    "brands",
    "vehicle_models",
    "variants",
    "variant_prices",
    "variant_powertrain_specs",
    "variant_charging_options",
    "variant_terrain_modes",
    "variant_physical_specs",
    "variant_safety_specs",
    "variant_comfort_specs",
    "variant_infotainment_specs",
    "variant_lighting_specs",
    "variant_connected_specs",
}


def test_catalogue_metadata_contract() -> None:
    """Keep table boundaries, nullable facts, and derived fields intentional."""
    assert set(Base.metadata.tables) == EXPECTED_TABLES

    variants = Base.metadata.tables["variants"]
    assert variants.c.catalogue_id.unique
    assert not variants.c.is_active.nullable

    prices = Base.metadata.tables["variant_prices"]
    assert list(prices.primary_key.columns.keys()) == ["variant_id", "city"]
    assert isinstance(prices.c.ex_showroom_price.type, Numeric)

    for table in Base.metadata.tables.values():
        assert not any(isinstance(column.type, Enum) for column in table.columns)
        for column in table.columns:
            if isinstance(column.type, Boolean) and column.name != "is_active":
                assert column.nullable

    all_columns = {
        column.name
        for table in Base.metadata.tables.values()
        for column in table.columns
    }
    assert {"four_wheel_drive", "fast_charging", "curtain_airbags"}.isdisjoint(
        all_columns
    )
