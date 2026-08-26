"""Variant lighting specifications."""

from sqlalchemy import BigInteger, Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class VariantLightingSpec(Base):
    """Canonical exterior and interior lighting facts."""

    __tablename__ = "variant_lighting_specs"

    variant_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("variants.id", ondelete="CASCADE"), primary_key=True
    )
    headlamp_type: Mapped[str | None] = mapped_column(Text)
    projector_headlamps: Mapped[bool | None] = mapped_column(Boolean)
    led_headlamps: Mapped[bool | None] = mapped_column(Boolean)
    fog_lights: Mapped[bool | None] = mapped_column(Boolean)
    front_fog_lights: Mapped[bool | None] = mapped_column(Boolean)
    rear_fog_lights: Mapped[bool | None] = mapped_column(Boolean)
    drl: Mapped[bool | None] = mapped_column(Boolean)
    drl_type: Mapped[str | None] = mapped_column(Text)
    follow_me_home_headlamps: Mapped[bool | None] = mapped_column(Boolean)
    automatic_headlamps: Mapped[bool | None] = mapped_column(Boolean)
    ambient_interior_lighting: Mapped[bool | None] = mapped_column(Boolean)
