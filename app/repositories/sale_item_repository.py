"""
Repository for SaleItem model.
"""

from sqlalchemy import select

from app.models.sale_item import SaleItem
from app.repositories.base_repository import BaseRepository


class SaleItemRepository(BaseRepository[SaleItem]):
    """Repository for sale items."""

    model = SaleItem

    def by_sale(self, sale_id: int) -> list[SaleItem]:
        statement = (
            select(SaleItem)
            .where(SaleItem.sale_id == sale_id)
        )
        return list(self.session.execute(statement).scalars().all())