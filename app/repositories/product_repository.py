from sqlalchemy import select

from app.models.product import Product
from app.repositories.base_repository import BaseRepository

class ProductRepository(BaseRepository[Product]):
    """Repository for product operations."""
    model = Product

    def get_by_sku(self, sku: str) -> Product | None:
        statement = select(Product).where(Product.sku == sku)
        return self.session.execute(statement).scalar_one_or_none()

    def exists(self, sku: str) -> bool:
        return self.get_by_sku(sku) is not None

    def list_all(self) -> list[Product]:
        statement = select(Product).order_by(Product.name)
        return list(self.session.execute(statement).scalars().all())