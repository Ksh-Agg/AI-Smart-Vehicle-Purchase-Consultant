"""Brand loader component."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.brand import Brand
from app.etl.models.brand import CanonicalBrand


class BrandLoader:
    """Handles resolving or inserting Brand ORM records during loading."""

    def get_or_create(self, session: Session, brand_data: CanonicalBrand) -> Brand:
        """Looks up a Brand by name (case-insensitively). If it exists, returns it; otherwise, creates it.

        Args:
            session: Active SQLAlchemy DB Session.
            brand_data: The CanonicalBrand Pydantic data model.

        Returns:
            The resolved/created Brand database ORM instance.
        """
        stmt = select(Brand).where(Brand.name.ilike(brand_data.name))
        result = session.execute(stmt).scalar_one_or_none()

        if result:
            return result

        # Create new Brand
        new_brand = Brand(
            name=brand_data.name.strip(),
            country=brand_data.country.strip(),
            origin=brand_data.origin.strip() if brand_data.origin else None,
        )
        session.add(new_brand)
        session.flush()  # Populates new_brand.id for FK linkages without committing the transaction

        return new_brand
