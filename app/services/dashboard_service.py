"""
Dashboard service.
"""

from datetime import date
from datetime import datetime
from datetime import time
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy import select

from app.models.customer import Customer
from app.models.product import Product
from app.models.purchase import Purchase
from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.models.stock_transaction import (
    StockTransaction,
    StockTransactionType,
)
from app.models.supplier import Supplier


class DashboardService:
    """Dashboard statistics."""

    def __init__(self, session):
        self.session = session

    # -------------------------------------------------
    # Today's Sales Amount
    # -------------------------------------------------

    def today_sales(self) -> Decimal:

        start = datetime.combine(
            date.today(),
            time.min,
        )

        end = datetime.combine(
            date.today(),
            time.max,
        )

        stmt = (
            select(
                func.coalesce(
                    func.sum(
                        SaleItem.quantity
                        * SaleItem.rate
                    ),
                    0,
                )
            )
            .join(
                Sale,
                Sale.id == SaleItem.sale_id,
            )
            .where(
                Sale.sale_date >= start,
                Sale.sale_date <= end,
            )
        )

        value = self.session.scalar(stmt)

        return Decimal(str(value or 0))

    # -------------------------------------------------
    # Today's Sale Count
    # -------------------------------------------------

    def today_sale_count(self) -> int:

        start = datetime.combine(
            date.today(),
            time.min,
        )

        end = datetime.combine(
            date.today(),
            time.max,
        )

        stmt = (
            select(func.count())
            .select_from(Sale)
            .where(
                Sale.sale_date >= start,
                Sale.sale_date <= end,
            )
        )

        return int(self.session.scalar(stmt) or 0)

    # -------------------------------------------------
    # Today's Purchase Count
    # -------------------------------------------------

    def today_purchase_count(self) -> int:

        start = datetime.combine(
            date.today(),
            time.min,
        )

        end = datetime.combine(
            date.today(),
            time.max,
        )

        stmt = (
            select(func.count())
            .select_from(Purchase)
            .where(
                Purchase.purchase_date >= start,
                Purchase.purchase_date <= end,
            )
        )

        return int(self.session.scalar(stmt) or 0)

    # -------------------------------------------------
    # Total Customers
    # -------------------------------------------------

    def total_customers(self) -> int:

        stmt = select(func.count()).select_from(Customer)

        return int(self.session.scalar(stmt) or 0)

    # -------------------------------------------------
    # Total Suppliers
    # -------------------------------------------------

    def total_suppliers(self) -> int:

        stmt = select(func.count()).select_from(Supplier)

        return int(self.session.scalar(stmt) or 0)

    # -------------------------------------------------
    # Total Products
    # -------------------------------------------------

    def total_products(self) -> int:

        stmt = select(func.count()).select_from(Product)

        return int(self.session.scalar(stmt) or 0)

    # -------------------------------------------------
    # Current Stock
    # -------------------------------------------------

    def total_stock(self) -> Decimal:

        transactions = (
            self.session.execute(
                select(StockTransaction)
            )
            .scalars()
            .all()
        )

        total = Decimal("0.000")

        for tx in transactions:

            if tx.transaction_type in (
                StockTransactionType.PURCHASE,
                StockTransactionType.STOCK_IN,
                StockTransactionType.RETURN_IN,
            ):
                total += tx.quantity

            elif tx.transaction_type in (
                StockTransactionType.SALE,
                StockTransactionType.STOCK_OUT,
                StockTransactionType.RETURN_OUT,
            ):
                total -= tx.quantity

        return total

    # -------------------------------------------------
    # Inventory Value
    # -------------------------------------------------

    def stock_value(self) -> Decimal:

        products = (
            self.session.execute(
                select(Product)
            )
            .scalars()
            .all()
        )

        total = Decimal("0.00")

        for product in products:

            qty = Decimal("0.000")

            for tx in product.stock_transactions:

                if tx.transaction_type in (
                    StockTransactionType.PURCHASE,
                    StockTransactionType.STOCK_IN,
                    StockTransactionType.RETURN_IN,
                ):
                    qty += tx.quantity

                elif tx.transaction_type in (
                    StockTransactionType.SALE,
                    StockTransactionType.STOCK_OUT,
                    StockTransactionType.RETURN_OUT,
                ):
                    qty -= tx.quantity

            total += (
                qty * product.purchase_price
            )

        return total

    # -------------------------------------------------
    # Dashboard Summary
    # -------------------------------------------------

    def summary(self) -> dict:

        return {
            "today_sales": self.today_sales(),
            "today_sale_count": self.today_sale_count(),
            "today_purchase_count": self.today_purchase_count(),
            "customers": self.total_customers(),
            "suppliers": self.total_suppliers(),
            "products": self.total_products(),
            "stock_quantity": self.total_stock(),
            "stock_value": self.stock_value(),
        }