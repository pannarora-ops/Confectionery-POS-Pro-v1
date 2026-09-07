"""
Purchase Controller
"""

from __future__ import annotations

from decimal import Decimal

from sqlalchemy.orm import Session

from app.services.purchase_service import PurchaseService
from app.services.product_service import ProductService
from app.services.batch_service import BatchService
from app.ui.purchase.purchase_controller import PurchaseController


class PurchaseController:

    def __init__(
        self,
        dialog,
        session: Session,
    ):

        self.dialog = dialog

        self.session = session

        self.purchase_service = PurchaseService(session)

        self.product_service = ProductService(session)

        self.batch_service = BatchService(session)

    # -------------------------------------------------

    def load_products(self):

        products = self.product_service.get_all()

        self.dialog.product_cache = products

    # -------------------------------------------------

    def load_suppliers(self):

        suppliers = self.purchase_service.get_suppliers()

        combo = self.dialog.supplier

        combo.clear()

        for supplier in suppliers:

            combo.addItem(

                supplier.name,

                supplier.id,

            )

    # -------------------------------------------------

    def add_new_row(self):

        self.dialog.model.add_item()

        self.refresh_summary()

    # -------------------------------------------------

    def remove_row(self):

        index = self.dialog.table.currentIndex()

        if not index.isValid():

            return

        self.dialog.model.remove_item(

            index.row()

        )

        self.refresh_summary()

    # -------------------------------------------------

    def refresh_summary(self):

        model = self.dialog.model

        subtotal = model.subtotal()

        qty = model.total_qty()

        self.dialog.summary.update_summary(

            items=model.rowCount(),

            qty=qty,

            free_qty=Decimal("0"),

            subtotal=subtotal,

            discount=Decimal("0"),

            gst=Decimal("0"),

            roundoff=Decimal("0"),

            grand=subtotal,

            landing_cost=Decimal("0"),

            margin=Decimal("0"),

        )

    # -------------------------------------------------

    def save_purchase(self):

        purchase = self.dialog.build_purchase()

        items = self.dialog.model.export()

        self.purchase_service.create(

            purchase,

            items,

        )

    # -------------------------------------------------

    def new_purchase(self):

        self.dialog.clear()

    self.controller = PurchaseController(
        self,
        session,
    )
    self.btn_add.clicked.connect(
        self.controller.add_new_row
    )

    self.btn_remove.clicked.connect(
        self.controller.remove_row
    )

    self.btn_save.clicked.connect(
        self.controller.save_purchase
    )