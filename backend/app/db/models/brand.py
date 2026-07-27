"""Brand ORM model mapping manufacturers."""

from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.db.models.vehicle import Vehicle


class Brand(Base, TimestampMixin):
    """Brand model representing automotive manufacturers."""

    __tablename__ = "brands"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    origin: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Relationships
    vehicles: Mapped[list["Vehicle"]] = relationship(
        "Vehicle",
        back_populates="brand",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Brand(id={self.id}, name={self.name!r})>"
