"""
Report service.
"""

from datetime import date
from decimal import Decimal

from sqlalchemy import func, select

from app.models.customer_ledger import CustomerLedger
from app.models.purchase import Purchase
from app.models.sale import Sale
from app.models.stock_transaction import StockTransaction
from app.models.supplier_ledger import SupplierLedger
from app.services.inventory_service import InventoryService


class ReportService:
    """Reporting service."""

    def __init__(self, session):
        self.session = session

        # Avoid name conflict with inventory() method
        self.inventory_service = InventoryService(
            session
        )

    # -----------------------------------------
    # Sales Report
    # -----------------------------------------

    def sales(
        self,
        start: date | None = None,
        end: date | None = None,
    ) -> list[Sale]:

        stmt = select(Sale)

        if start:
            stmt = stmt.where(
                func.date(Sale.sale_date) >= start
            )

        if end:
            stmt = stmt.where(
                func.date(Sale.sale_date) <= end
            )

        return list(
            self.session.execute(stmt)
            .scalars()
            .all()
        )

    # -----------------------------------------
    # Purchase Report
    # -----------------------------------------

    def purchases(
        self,
        start: date | None = None,
        end: date | None = None,
    ) -> list[Purchase]:

        stmt = select(Purchase)

        if start:
            stmt = stmt.where(
                func.date(Purchase.purchase_date)
                >= start
            )

        if end:
            stmt = stmt.where(
                func.date(Purchase.purchase_date)
                <= end
            )

        return list(
            self.session.execute(stmt)
            .scalars()
            .all()
        )

    # -----------------------------------------
    # Customer Ledger
    # -----------------------------------------

    def customer_ledger(
        self,
        customer_id: int,
    ) -> list[CustomerLedger]:

        stmt = (
            select(CustomerLedger)
            .where(
                CustomerLedger.customer_id
                == customer_id
            )
            .order_by(CustomerLedger.id)
        )

        return list(
            self.session.execute(stmt)
            .scalars()
            .all()
        )

    # -----------------------------------------
    # Supplier Ledger
    # -----------------------------------------

    def supplier_ledger(
        self,
        supplier_id: int,
    ) -> list[SupplierLedger]:

        stmt = (
            select(SupplierLedger)
            .where(
                SupplierLedger.supplier_id
                == supplier_id
            )
            .order_by(SupplierLedger.id)
        )

        return list(
            self.session.execute(stmt)
            .scalars()
            .all()
        )

    # -----------------------------------------
    # Inventory Report
    # -----------------------------------------

    def inventory(self):

        return self.inventory_service.inventory()

    # -----------------------------------------
    # Stock Value
    # -----------------------------------------

    def stock_value(self) -> Decimal:

        return self.inventory_service.stock_value()

    # -----------------------------------------
    # Stock History
    # -----------------------------------------

    def stock_history(
        self,
        product_id: int | None = None,
    ) -> list[StockTransaction]:

        stmt = select(StockTransaction)

        if product_id is not None:
            stmt = stmt.where(
                StockTransaction.product_id
                == product_id
            )

        stmt = stmt.order_by(
            StockTransaction.id
        )

        return list(
            self.session.execute(stmt)
            .scalars()
            .all()
        )

    # -----------------------------------------
    # Summary
    # -----------------------------------------

    def summary(self) -> dict:

        inventory = (
            self.inventory_service.inventory()
        )

        return {
            "sales": len(self.sales()),
            "purchases": len(self.purchases()),
            "products": len(inventory),
            "stock_value": self.stock_value(),
        }