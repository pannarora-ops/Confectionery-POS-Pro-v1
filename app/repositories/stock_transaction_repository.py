"""
Repository for stock transactions.
"""

from decimal import Decimal

from sqlalchemy import func, select

from app.models.stock_transaction import (
    StockTransaction,
    StockTransactionType,
)
from app.repositories.base_repository import BaseRepository


class StockTransactionRepository(BaseRepository[StockTransaction]):
    """Repository for stock transactions."""

    model = StockTransaction

    def list_by_product(self, product_id: int) -> list[StockTransaction]:
        """Return all transactions for a product."""
        statement = (
            select(StockTransaction)
            .where(StockTransaction.product_id == product_id)
            .order_by(StockTransaction.created_at)
        )
        return list(self.session.execute(statement).scalars().all())

    def get_current_stock(self, product_id: int) -> Decimal:
        """Calculate current stock."""

        statement = (
            select(func.coalesce(func.sum(StockTransaction.quantity), 0))
            .where(StockTransaction.product_id == product_id)
        )

        result = self.session.execute(statement).scalar_one()

        return Decimal(result)