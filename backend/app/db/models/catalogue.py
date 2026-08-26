"""Catalogue identity models."""

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    ForeignKey,
    Identity,
    Index,
    Integer,
    Text,
    func,
    true,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class Brand(Base, TimestampMixin):
    """Vehicle manufacturer."""

    __tablename__ = "brands"

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)

    __table_args__ = (
        CheckConstraint("btrim(name) <> ''", name="name_not_blank"),
        Index("uq_brands_name_ci", func.lower(name), unique=True),
    )


class VehicleModel(Base, TimestampMixin):
    """Named model belonging to a brand."""

    __tablename__ = "vehicle_models"

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)
    brand_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("brands.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)

    __table_args__ = (
        CheckConstraint("btrim(name) <> ''", name="name_not_blank"),
        Index(
            "uq_vehicle_models_brand_name_ci",
            brand_id,
            func.lower(name),
            unique=True,
        ),
    )


class Variant(Base, TimestampMixin):
    """Current catalogue variant identified by a stable external code."""

    __tablename__ = "variants"

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)
    catalogue_id: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    model_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("vehicle_models.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    trim: Mapped[str] = mapped_column(Text, nullable=False)
    variant_name: Mapped[str] = mapped_column(Text, nullable=False)
    model_year: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=true(),
    )

    __table_args__ = (
        CheckConstraint("btrim(catalogue_id) <> ''", name="catalogue_id_not_blank"),
        CheckConstraint("btrim(trim) <> ''", name="trim_not_blank"),
        CheckConstraint("btrim(variant_name) <> ''", name="variant_name_not_blank"),
        CheckConstraint(
            "model_year BETWEEN 1886 AND 2100",
            name="model_year_range",
        ),
    )
