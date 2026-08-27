"""Add durable consultation storage and the SQL-agent catalogue view.

Revision ID: 20260827_0002
Revises: 20260827_0001
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260827_0002"
down_revision: str | Sequence[str] | None = "20260827_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.create_table(
        "consultations",
        sa.Column("thread_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("kshagg_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("status", sa.Text(), nullable=False),
        sa.Column(
            "profile",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
        sa.Column("last_message_summary", sa.Text(), server_default="", nullable=False),
        sa.Column(
            "latest_recommended_variant_ids",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'[]'::jsonb"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "status IN ('active','completed','saved')",
            name=op.f("ck_consultations_status_values"),
        ),
        sa.PrimaryKeyConstraint("thread_id", name=op.f("pk_consultations")),
    )
    op.create_index(
        op.f("ix_consultations_kshagg_id"),
        "consultations",
        ["kshagg_id"],
    )
    op.create_table(
        "consultation_shortlist_items",
        sa.Column(
            "consultation_thread_id", postgresql.UUID(as_uuid=True), nullable=False
        ),
        sa.Column("variant_id", sa.BigInteger(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["consultation_thread_id"],
            ["consultations.thread_id"],
            name=op.f(
                "fk_consultation_shortlist_items_consultation_thread_id_consultations"
            ),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["variant_id"],
            ["variants.id"],
            name=op.f("fk_consultation_shortlist_items_variant_id_variants"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "consultation_thread_id",
            "variant_id",
            name=op.f("pk_consultation_shortlist_items"),
        ),
    )
    op.execute(_CATALOGUE_VIEW)
    op.execute(
        """
        DO $$ BEGIN
          IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'catalogue_agent_readonly') THEN
            CREATE ROLE catalogue_agent_readonly NOLOGIN;
          END IF;
        END $$;
        GRANT USAGE ON SCHEMA public TO catalogue_agent_readonly;
        GRANT SELECT ON agent_vehicle_catalogue TO catalogue_agent_readonly;
        """
    )


def downgrade() -> None:
    op.execute(
        "REVOKE SELECT ON agent_vehicle_catalogue FROM catalogue_agent_readonly"
    )
    op.execute("DROP VIEW IF EXISTS agent_vehicle_catalogue")
    op.drop_table("consultation_shortlist_items")
    op.drop_index(op.f("ix_consultations_kshagg_id"), table_name="consultations")
    op.drop_table("consultations")


_CATALOGUE_VIEW = """
CREATE VIEW agent_vehicle_catalogue AS
SELECT
  v.id AS variant_id,
  v.catalogue_id,
  b.name AS brand,
  vm.name AS model,
  v.variant_name,
  v.trim,
  v.model_year,
  v.is_active,
  p.city,
  p.ex_showroom_price,
  p.on_road_price,
  pt.fuel_type,
  pt.transmission_type,
  pt.drivetrain,
  pt.mileage_arai_kmpl,
  pt.mileage_arai_kmkg,
  pt.mileage_user_reported,
  pt.engine_displacement_cc,
  pt.max_power_bhp,
  pt.max_torque_nm,
  pt.driving_range_km,
  pt.battery_capacity_kwh,
  ph.seating_capacity,
  ph.bootspace_litres,
  ph.ground_clearance_mm,
  ph.length_mm,
  ph.width_mm,
  ph.height_mm,
  s.adas_level,
  s.airbag_count,
  s.abs,
  s.ebd,
  s.esp,
  s.hill_hold_control,
  s.isofix_child_seat_anchors,
  s.rear_parking_sensors,
  s.parking_camera,
  c.air_conditioner,
  c.rear_ac_vents,
  c.keyless_entry,
  c.push_button_start,
  c.cruise_control,
  c.driver_seat_height_adjustment,
  i.touchscreen,
  i.android_auto,
  i.apple_carplay,
  i.bluetooth,
  i.navigation,
  i.number_of_speakers,
  i.wireless_charging,
  i.hud
FROM variants v
JOIN vehicle_models vm ON vm.id = v.model_id
JOIN brands b ON b.id = vm.brand_id
JOIN variant_prices p ON p.variant_id = v.id
LEFT JOIN variant_powertrain_specs pt ON pt.variant_id = v.id
LEFT JOIN variant_physical_specs ph ON ph.variant_id = v.id
LEFT JOIN variant_safety_specs s ON s.variant_id = v.id
LEFT JOIN variant_comfort_specs c ON c.variant_id = v.id
LEFT JOIN variant_infotainment_specs i ON i.variant_id = v.id
WHERE lower(b.name) IN ('maruti suzuki', 'maruti') AND v.is_active = true
"""
