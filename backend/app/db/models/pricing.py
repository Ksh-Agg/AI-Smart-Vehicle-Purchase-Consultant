"""Current city-level catalogue pricing."""

from decimal import Decimal

from sqlalchemy import BigInteger, CheckConstraint, ForeignKey, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class VariantPrice(Base, TimestampMixin):
    """Latest price for one variant in one city."""

    __tablename__ = "variant_prices"

    variant_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("variants.id", ondelete="CASCADE"),
        primary_key=True,
    )
    city: Mapped[str] = mapped_column(Text, primary_key=True)
    ex_showroom_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    on_road_price: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))

    __table_args__ = (
        CheckConstraint("btrim(city) <> ''", name="city_not_blank"),
        CheckConstraint("ex_showroom_price > 0", name="ex_showroom_price_positive"),
        CheckConstraint(
            "on_road_price IS NULL OR on_road_price > 0",
            name="on_road_price_positive",
        ),
    )
