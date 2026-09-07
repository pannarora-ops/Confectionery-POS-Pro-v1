"""
Repository for Brand.
"""

from sqlalchemy import select

from app.models.brand import Brand
from app.repositories.base_repository import BaseRepository


class BrandRepository(BaseRepository[Brand]):
    """Repository for Brand operations."""

    model = Brand

    # -------------------------------------------------
    # Get Brand by ID
    # -------------------------------------------------

    def get(self, brand_id: int) -> Brand | None:
        return self.session.get(Brand, brand_id)

    # -------------------------------------------------
    # Get Brand by Name
    # -------------------------------------------------

    def get_by_name(
        self,
        name: str,
    ) -> Brand | None:

        statement = (
            select(Brand)
            .where(Brand.name == name.strip())
        )

        return (
            self.session.execute(statement)
            .scalar_one_or_none()
        )

    # -------------------------------------------------
    # Exists
    # -------------------------------------------------

    def exists(
        self,
        name: str,
    ) -> bool:

        return (
            self.get_by_name(name)
            is not None
        )

    # -------------------------------------------------
    # List All
    # -------------------------------------------------

    def list_all(
        self,
    ) -> list[Brand]:

        statement = (
            select(Brand)
            .order_by(Brand.name)
        )

        return list(
            self.session.execute(statement)
            .scalars()
            .all()
        )

    # -------------------------------------------------
    # Search
    # -------------------------------------------------

    def search(
        self,
        keyword: str,
    ) -> list[Brand]:

        statement = (
            select(Brand)
            .where(
                Brand.name.ilike(
                    f"%{keyword}%"
                )
            )
            .order_by(Brand.name)
        )

        return list(
            self.session.execute(statement)
            .scalars()
            .all()
        )

    # -------------------------------------------------
    # Add
    # -------------------------------------------------

    def add(
        self,
        brand: Brand,
    ) -> Brand:

        self.session.add(brand)

        self.session.flush()

        return brand

    # -------------------------------------------------
    # Delete
    # -------------------------------------------------

    def delete(
        self,
        brand: Brand,
    ):

        self.session.delete(brand)

    # -------------------------------------------------
    # Update
    # -------------------------------------------------

    def update(self):

        self.session.flush()