"""
Purchase Service
Commercial POS Version
"""

from __future__ import annotations

from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.batch import Batch
from app.models.purchase import Purchase
from app.models.purchase_item import PurchaseItem
from app.repositories.purchase_repository import PurchaseRepository
from app.services.stock_service import StockService


class PurchaseService:

    def __init__(self, session: Session):

        self.session = session

        self.repo = PurchaseRepository(session)

        self.stock = StockService(session)

    # -------------------------------------------------
    # Create Purchase
    # -------------------------------------------------

    def create(
        self,
        purchase: Purchase,
        items: list[dict],
    ):

        if not purchase.purchase_no:

            purchase.purchase_no = (
                self.repo.generate_purchase_no()
            )

        subtotal = Decimal("0.00")
        gst_total = Decimal("0.00")

        self.repo.create(purchase)

        for item in items:

            purchase_item = PurchaseItem(

                purchase_id=purchase.id,

                product_id=item["product_id"],

                quantity=item["quantity"],

                free_quantity=item.get(
                    "free_quantity",
                    Decimal("0"),
                ),

                purchase_price=item["purchase_price"],

                selling_price=item["selling_price"],

                mrp=item["mrp"],

                gst_percent=item["gst_percent"],

                discount=item.get(
                    "discount",
                    Decimal("0"),
                ),

                total=item["total"],
            )

            self.session.add(
                purchase_item
            )

            subtotal += item["total"]

            gst_total += item["gst_amount"]

            # ---------------------------------
            # Create Batch
            # ---------------------------------

            batch = Batch(

                product_id=item["product_id"],

                batch_no=item["batch_no"],

                manufacture_date=item.get(
                    "manufacture_date"
                ),

                expiry_date=item.get(
                    "expiry_date"
                ),

                purchase_rate=item[
                    "purchase_price"
                ],

                sale_rate=item[
                    "selling_price"
                ],

                mrp=item["mrp"],

                available_qty=item["quantity"]
                + item.get(
                    "free_quantity",
                    Decimal("0"),
                ),

                supplier_id=purchase.supplier_id,

                purchase_id=purchase.id,

                purchase_item_id=None,
            )

            self.session.add(batch)

            self.session.flush()

            # ---------------------------------
            # Stock Entry
            # ---------------------------------

            self.stock.purchase_stock(

                product_id=item["product_id"],

                batch_id=batch.id,

                qty=batch.available_qty,

                bill_no=purchase.invoice_no,
            )

        purchase.sub_total = subtotal

        purchase.gst_total = gst_total

        purchase.grand_total = (
            subtotal + gst_total
        )

        self.session.commit()

        return purchase