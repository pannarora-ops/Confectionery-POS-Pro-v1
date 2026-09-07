"""
POS Controller
Commercial POS Version
"""

from __future__ import annotations

from decimal import Decimal

from sqlalchemy.orm import Session

from app.services.product_service import ProductService
from app.services.batch_service import BatchService
from app.services.sale_service import SaleService
from app.services.customer_service import CustomerService
from app.services.loyalty_service import LoyaltyService


class POSController:

    def __init__(
        self,
        window,
        session: Session,
    ):

        self.window = window
        self.session = session

        self.product_service = ProductService(session)
        self.batch_service = BatchService(session)
        self.sale_service = SaleService(session)
        self.customer_service = CustomerService(session)
        self.loyalty_service = LoyaltyService(session)

    # -------------------------------------------------
    # Product Search
    # -------------------------------------------------

    def search_product(self):

        text = self.window.search.text().strip()

        if not text:
            return

        product = self.product_service.search(text)

        if product is None:

            self.window.search.clear()

            return

        allocation = self.batch_service.allocate_stock(
            product.id,
            Decimal("1"),
        )

        batch, qty = allocation[0]

        self.window.model.add_product(
            product,
            batch,
            qty,
        )

        self.window.search.clear()

        self.refresh_summary()

    # -------------------------------------------------
    # Refresh Summary
    # -------------------------------------------------

    def refresh_summary(self):

        model = self.window.model

        subtotal = model.subtotal()

        qty = model.total_qty()

        self.window.loyalty.update_bill(
            subtotal,
            qty,
        )

    # -------------------------------------------------
    # Customer Changed
    # -------------------------------------------------

    def customer_changed(self):

        customer_id = self.window.customer.currentData()

        if customer_id is None:
            return

        customer = self.customer_service.get(
            customer_id
        )

        self.window.loyalty.load_customer(
            customer
        )

    # -------------------------------------------------
    # Hold Bill
    # -------------------------------------------------

    def hold_bill(self):

        self.sale_service.hold_bill(

            self.window.model.export()

        )

        self.window.model.clear()

        self.refresh_summary()

    # -------------------------------------------------
    # Resume Bill
    # -------------------------------------------------

    def resume_bill(

        self,
        bill_id,
    ):

        rows = self.sale_service.resume_bill(
            bill_id
        )

        self.window.model.clear()

        for row in rows:

            self.window.model.add_product(

                row["product"],

                row["batch"],

                row["qty"],

            )

        self.refresh_summary()

    # -------------------------------------------------
    # Payment
    # -------------------------------------------------

    def payment(self):

        from app.ui.pos.payment_dialog import PaymentDialog

        dialog = PaymentDialog(

            self.window,

            total=self.window.model.subtotal(),

        )

        dialog.exec()

    # -------------------------------------------------
    # Save Bill
    # -------------------------------------------------

    def save_bill(self):

        items = self.window.model.export()

        customer = self.window.customer.currentData()

        invoice = self.sale_service.create_sale(

            customer,

            items,

        )

        self.loyalty_service.process_sale(

            invoice

        )

        self.window.model.clear()

        self.refresh_summary()

    # -------------------------------------------------
    # Delete Current Row
    # -------------------------------------------------

    def delete_row(self):

        index = self.window.table.currentIndex()

        if not index.isValid():
            return

        self.window.model.remove_row(

            index.row()

        )

        self.refresh_summary()

    # -------------------------------------------------
    # New Bill
    # -------------------------------------------------

    def new_bill(self):

        self.window.model.clear()

        self.window.search.clear()

        self.refresh_summary()

    def scan_barcode(self, barcode: str):

        product = self.product_service.find_by_barcode(barcode)

        if product is None:
            return

        allocation = self.batch_service.allocate_stock(
            product.id,
            Decimal("1")
        )

        batch, qty = allocation[0]

            self.window.model.add_product(
                product,
                batch,
                qty,
        )

            self.refresh_summary()