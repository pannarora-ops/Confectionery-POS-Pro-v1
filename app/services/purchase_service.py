"""
Purchase service.
"""

from decimal import Decimal

from app.exceptions.custom_exceptions import (
    DuplicateInvoiceError,
    ProductNotFoundError,
    SupplierNotFoundError,
)
from app.models.purchase import Purchase
from app.models.purchase_item import PurchaseItem
from app.models.stock_transaction import (
    StockTransaction,
    StockTransactionType,
)
from app.repositories.product_repository import (
    ProductRepository,
)
from app.repositories.purchase_repository import (
    PurchaseRepository,
)
from app.repositories.supplier_repository import (
    SupplierRepository,
)
from app.services.ledger_service import LedgerService


class PurchaseService:
    """Business logic for purchases."""

    def __init__(self, session):
        self.session = session

        self.purchase_repository = PurchaseRepository(session)
        self.product_repository = ProductRepository(session)
        self.supplier_repository = SupplierRepository(session)

        self.ledger_service = LedgerService(session)

    def create_purchase(
        self,
        invoice_number: str,
        supplier_id: int,
        items: list[dict],
        remarks: str | None = None,
    ) -> Purchase:
        """Create purchase invoice."""

        # ---------------------------------
        # Duplicate Invoice
        # ---------------------------------

        if self.purchase_repository.find_by_invoice(
            invoice_number
        ):
            raise DuplicateInvoiceError(
                f"Invoice '{invoice_number}' already exists."
            )

        # ---------------------------------
        # Supplier Validation
        # ---------------------------------

        supplier = self.supplier_repository.get(
            supplier_id
        )

        if supplier is None:
            raise SupplierNotFoundError(
                f"Supplier {supplier_id} not found."
            )

        # ---------------------------------
        # Create Purchase
        # ---------------------------------

        purchase = Purchase(
            invoice_number=invoice_number,
            supplier_id=supplier_id,
            remarks=remarks,
        )

        total_amount = Decimal("0.00")

        # ---------------------------------
        # Purchase Items
        # ---------------------------------

        for item in items:

            product = self.product_repository.get(
                item["product_id"]
            )

            if product is None:
                raise ProductNotFoundError(
                    f"Product {item['product_id']} not found."
                )

            quantity = Decimal(
                str(item["quantity"])
            )

            rate = Decimal(
                str(item["rate"])
            )

            gst_percent = Decimal(
                str(
                    item.get(
                        "gst_percent",
                        product.gst_percent,
                    )
                )
            )

            purchase_item = PurchaseItem(
                product_id=product.id,
                quantity=quantity,
                rate=rate,
                gst_percent=gst_percent,
            )

            purchase.items.append(
                purchase_item
            )

            total_amount += quantity * rate

            # -----------------------------
            # Stock Transaction
            # -----------------------------

            self.session.add(
                StockTransaction(
                    product_id=product.id,
                    transaction_type=StockTransactionType.PURCHASE,
                    quantity=quantity,
                    reference=invoice_number,
                    remarks="Purchase Invoice",
                )
            )

        # ---------------------------------
        # Save Purchase
        # ---------------------------------

        self.session.add(purchase)
        self.session.flush()

        # ---------------------------------
        # Supplier Ledger
        # ---------------------------------

        self.ledger_service.supplier_purchase(
            supplier_id=supplier_id,
            amount=total_amount,
            reference=invoice_number,
            remarks="Purchase Invoice",
        )

        # ---------------------------------
        # Commit
        # ---------------------------------

        self.session.commit()
        self.session.refresh(purchase)

        return purchase