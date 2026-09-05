"""
Repository for Product model.
"""

from sqlalchemy import select

from app.models.product import Product
from app.repositories.base_repository import BaseRepository


class ProductRepository(BaseRepository[Product]):
    """Repository for product operations."""

    def get_by_sku(self, sku: str) -> Product | None:
        statement = select(Product).where(Product.sku == sku)
        return self.session.execute(statement).scalar_one_or_none()

    def get_by_barcode(self, barcode: str) -> Product | None:
        statement = select(Product).where(Product.barcode == barcode)
        return self.session.execute(statement).scalar_one_or_none()

    def list_all(self) -> list[Product]:
        statement = select(Product).order_by(Product.name)
        return list(self.session.execute(statement).scalars().all())