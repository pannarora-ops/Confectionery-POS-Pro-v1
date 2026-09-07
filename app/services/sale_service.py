"""
Sale service.
"""

from decimal import Decimal

from app.exceptions.custom_exceptions import (
    CustomerNotFoundError,
    DuplicateInvoiceError,
    InsufficientStockError,
    ProductNotFoundError,
)
from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.models.stock_transaction import (
    StockTransaction,
    StockTransactionType,
)
from app.repositories.customer_repository import (
    CustomerRepository,
)
from app.repositories.product_repository import (
    ProductRepository,
)
from app.repositories.sale_repository import (
    SaleRepository,
)
from app.services.ledger_service import LedgerService
from app.services.loyalty_service import LoyaltyService


class SaleService:
    """Business logic for sales."""

    def __init__(self, session):
        self.session = session

        self.sale_repository = SaleRepository(session)
        self.customer_repository = CustomerRepository(session)
        self.product_repository = ProductRepository(session)

        self.ledger_service = LedgerService(session)
        self.loyalty_service = LoyaltyService(session)

    def create_sale(
        self,
        invoice_number: str,
        items: list[dict],
        customer_id: int | None = None,
        customer_name: str | None = None,
        remarks: str | None = None,
    ) -> Sale:
        """
        Create Sale Invoice.
        """

        # ---------------------------------
        # Duplicate Invoice
        # ---------------------------------

        if self.sale_repository.find_by_invoice(
            invoice_number
        ):
            raise DuplicateInvoiceError(
                f"Invoice '{invoice_number}' already exists."
            )

        # ---------------------------------
        # Customer Validation
        # ---------------------------------

        if customer_id is not None:

            customer = self.customer_repository.get(
                customer_id
            )

            if customer is None:
                raise CustomerNotFoundError(
                    f"Customer {customer_id} not found."
                )

        # ---------------------------------
        # Create Sale
        # ---------------------------------

        sale = Sale(
            invoice_number=invoice_number,
            customer_id=customer_id,
            customer_name=customer_name,
            remarks=remarks,
        )

        total_amount = Decimal("0.00")

        # ---------------------------------
        # Process Items
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
                str(
                    item.get(
                        "rate",
                        product.selling_price,
                    )
                )
            )

            gst_percent = Decimal(
                str(
                    item.get(
                        "gst_percent",
                        product.gst_percent,
                    )
                )
            )

            # -----------------------------
            # Calculate Current Stock
            # -----------------------------

            current_stock = Decimal("0.000")

            for tx in product.stock_transactions:

                if tx.transaction_type in (
                    StockTransactionType.PURCHASE,
                    StockTransactionType.STOCK_IN,
                    StockTransactionType.RETURN_IN,
                ):
                    current_stock += tx.quantity

                elif tx.transaction_type in (
                    StockTransactionType.SALE,
                    StockTransactionType.STOCK_OUT,
                    StockTransactionType.RETURN_OUT,
                ):
                    current_stock -= tx.quantity

            # -----------------------------
            # Stock Validation
            # -----------------------------

            if current_stock < quantity:

                raise InsufficientStockError(
                    f"{product.name} has only "
                    f"{current_stock} in stock."
                )

            # -----------------------------
            # Sale Item
            # -----------------------------

            sale_item = SaleItem(
                product_id=product.id,
                quantity=quantity,
                rate=rate,
                gst_percent=gst_percent,
            )

            sale.items.append(sale_item)

            total_amount += quantity * rate

            # -----------------------------
            # Stock Transaction
            # -----------------------------

            self.session.add(
                StockTransaction(
                    product_id=product.id,
                    transaction_type=StockTransactionType.SALE,
                    quantity=quantity,
                    reference=invoice_number,
                    remarks="Sale Invoice",
                )
            )

        # ---------------------------------
        # Save Sale
        # ---------------------------------

        self.session.add(sale)
        self.session.flush()

        # ---------------------------------
        # Ledger Entry
        # ---------------------------------

        if customer_id is not None:

            self.ledger_service.customer_sale(
                customer_id=customer_id,
                amount=total_amount,
                reference=invoice_number,
                remarks="Sale Invoice",
            )

        # ---------------------------------
        # Loyalty Points
        # ---------------------------------

        if customer_id is not None:

            self.loyalty_service.add_points(
                customer_id=customer_id,
                bill_amount=total_amount,
                reference=invoice_number,
            )

        # ---------------------------------
        # Commit
        # ---------------------------------

        self.session.commit()
        self.session.refresh(sale)

        return sale