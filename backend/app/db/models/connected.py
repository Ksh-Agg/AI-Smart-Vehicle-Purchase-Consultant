"""Variant connected-car specifications."""

from sqlalchemy import BigInteger, Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class VariantConnectedSpec(Base):
    """Canonical remote and connected-car facts."""

    __tablename__ = "variant_connected_specs"

    variant_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("variants.id", ondelete="CASCADE"), primary_key=True
    )
    connected_car_technology: Mapped[bool | None] = mapped_column(Boolean)
    ota_updates: Mapped[bool | None] = mapped_column(Boolean)
    alexa_compatibility: Mapped[bool | None] = mapped_column(Boolean)
    remote_ac: Mapped[str | None] = mapped_column(Text)
    remote_lock_unlock: Mapped[str | None] = mapped_column(Text)
    remote_engine_start: Mapped[bool | None] = mapped_column(Boolean)
    vehicle_tracking: Mapped[bool | None] = mapped_column(Boolean)
    geo_fencing: Mapped[bool | None] = mapped_column(Boolean)
