"""
Purchase Item repository.
"""

from sqlalchemy import select

from app.models.purchase_item import PurchaseItem
from app.repositories.base_repository import BaseRepository


class PurchaseItemRepository(
    BaseRepository[PurchaseItem]
):
    """Repository for purchase items."""

    model = PurchaseItem

    def by_purchase(
        self,
        purchase_id: int,
    ) -> list[PurchaseItem]:

        statement = (
            select(PurchaseItem)
            .where(
                PurchaseItem.purchase_id
                == purchase_id
            )
            .order_by(PurchaseItem.id)
        )

        return list(
            self.session.execute(statement)
            .scalars()
            .all()
        )