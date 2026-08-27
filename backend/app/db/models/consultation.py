"""Durable consultation and shortlist metadata."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import BigInteger, CheckConstraint, DateTime, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class Consultation(Base, TimestampMixin):
    """Queryable metadata for a checkpointed LangGraph thread."""

    __tablename__ = "consultations"

    thread_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    kshagg_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(Text, nullable=False, default="New consultation")
    status: Mapped[str] = mapped_column(Text, nullable=False, default="active")
    profile: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False, default=dict)
    last_message_summary: Mapped[str] = mapped_column(Text, nullable=False, default="")
    latest_recommended_variant_ids: Mapped[list[int]] = mapped_column(
        JSONB, nullable=False, default=list
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('active','completed','saved')", name="status_values"
        ),
    )


class ConsultationShortlistItem(Base):
    """One user-saved variant in a consultation comparison list."""

    __tablename__ = "consultation_shortlist_items"

    consultation_thread_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("consultations.thread_id", ondelete="CASCADE"),
        primary_key=True,
    )
    variant_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("variants.id", ondelete="CASCADE"),
        primary_key=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
