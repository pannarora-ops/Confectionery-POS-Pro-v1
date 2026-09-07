"""
Business logic for Brand.
"""

from app.exceptions.custom_exceptions import (
    DuplicateCategoryError,
)
from app.models.brand import Brand
from app.repositories.brand_repository import BrandRepository
from app.services.base_service import BaseService


class BrandService(BaseService):
    """Service for Brand operations."""

    def __init__(self, session):
        super().__init__(session)

        self.repository = BrandRepository(session)

    # -------------------------------------------------
    # Get All Brands
    # -------------------------------------------------

    def get_all(self) -> list[Brand]:
        return self.repository.list_all()

    # -------------------------------------------------
    # Search
    # -------------------------------------------------

    def search(self, keyword: str) -> list[Brand]:
        return self.repository.search(keyword)

    # -------------------------------------------------
    # Get
    # -------------------------------------------------

    def get(self, brand_id: int) -> Brand | None:
        return self.repository.get(brand_id)

    # -------------------------------------------------
    # Create
    # -------------------------------------------------

    def create(
        self,
        name: str,
        description: str | None = None,
    ) -> Brand:

        name = name.strip()

        if not name:
            raise ValueError(
                "Brand name is required."
            )

        if self.repository.exists(name):
            raise DuplicateCategoryError(
                f"Brand '{name}' already exists."
            )

        brand = Brand(
            name=name,
            description=description,
        )

        return self.repository.add(brand)

    # -------------------------------------------------
    # Update
    # -------------------------------------------------

    def update(
        self,
        brand_id: int,
        **kwargs,
    ) -> Brand | None:

        brand = self.repository.get(brand_id)

        if brand is None:
            return None

        if "name" in kwargs:

            new_name = kwargs["name"].strip()

            existing = self.repository.get_by_name(
                new_name
            )

            if (
                existing
                and existing.id != brand.id
            ):
                raise DuplicateCategoryError(
                    f"Brand '{new_name}' already exists."
                )

            brand.name = new_name

        if "description" in kwargs:
            brand.description = kwargs[
                "description"
            ]

        if "active" in kwargs:
            brand.active = kwargs[
                "active"
            ]

        self.repository.update()

        return brand

    # -------------------------------------------------
    # Delete
    # -------------------------------------------------

    def delete(
        self,
        brand_id: int,
    ) -> bool:

        brand = self.repository.get(brand_id)

        if brand is None:
            return False

        # Prevent delete if products exist

        if (
            hasattr(brand, "products")
            and len(brand.products) > 0
        ):
            raise ValueError(
                "Brand is used in products and cannot be deleted."
            )

        self.repository.delete(brand)

        return True