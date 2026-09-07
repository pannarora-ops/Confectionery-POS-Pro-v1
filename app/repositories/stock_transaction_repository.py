"""
Repository for StockTransaction model.
"""

from decimal import Decimal

from sqlalchemy import func, select

from app.models.stock_transaction import (
    StockTransaction,
    StockTransactionType,
)
from app.repositories.base_repository import BaseRepository


class StockTransactionRepository(
    BaseRepository[StockTransaction]
):
    """Repository for stock transactions."""

    model = StockTransaction

    def by_product(
        self,
        product_id: int,
    ) -> list[StockTransaction]:
        """
        Return stock ledger for a product.
        """
        statement = (
            select(StockTransaction)
            .where(
                StockTransaction.product_id == product_id
            )
            .order_by(
                StockTransaction.created_at
            )
        )

        return list(
            self.session.execute(statement)
            .scalars()
            .all()
        )

    def current_stock(
        self,
        product_id: int,
    ) -> Decimal:
        """
        Return current stock quantity.
        """

        statement = (
            select(
                func.coalesce(
                    func.sum(
                        StockTransaction.quantity
                    ),
                    0,
                )
            )
            .where(
                StockTransaction.product_id == product_id
            )
        )

        quantity = self.session.execute(
            statement
        ).scalar_one()

        return Decimal(str(quantity))

    def stock_in_transactions(
        self,
        product_id: int,
    ) -> list[StockTransaction]:
        """
        Return all stock-in transactions.
        """

        statement = (
            select(StockTransaction)
            .where(
                StockTransaction.product_id == product_id,
                StockTransaction.transaction_type
                == StockTransactionType.STOCK_IN,
            )
            .order_by(
                StockTransaction.created_at
            )
        )

        return list(
            self.session.execute(statement)
            .scalars()
            .all()
        )

    def stock_out_transactions(
        self,
        product_id: int,
    ) -> list[StockTransaction]:
        """
        Return all stock-out transactions.
        """

        statement = (
            select(StockTransaction)
            .where(
                StockTransaction.product_id == product_id,
                StockTransaction.transaction_type
                == StockTransactionType.STOCK_OUT,
            )
            .order_by(
                StockTransaction.created_at
            )
        )

        return list(
            self.session.execute(statement)
            .scalars()
            .all()
        )

    def total_stock_in(
        self,
        product_id: int,
    ) -> Decimal:
        """
        Return total stock received.
        """

        statement = (
            select(
                func.coalesce(
                    func.sum(
                        StockTransaction.quantity
                    ),
                    0,
                )
            )
            .where(
                StockTransaction.product_id == product_id,
                StockTransaction.transaction_type
                == StockTransactionType.STOCK_IN,
            )
        )

        quantity = self.session.execute(
            statement
        ).scalar_one()

        return Decimal(str(quantity))

    def total_stock_out(
        self,
        product_id: int,
    ) -> Decimal:
        """
        Return total stock issued.
        """

        statement = (
            select(
                func.coalesce(
                    func.sum(
                        func.abs(
                            StockTransaction.quantity
                        )
                    ),
                    0,
                )
            )
            .where(
                StockTransaction.product_id == product_id,
                StockTransaction.transaction_type
                == StockTransactionType.STOCK_OUT,
            )
        )

        quantity = self.session.execute(
            statement
        ).scalar_one()

        return Decimal(str(quantity))