"""
Inventory business logic.
"""

from decimal import Decimal

from app.exceptions.custom_exceptions import (
    InsufficientStockError,
    ProductNotFoundError,
)
from app.models.stock_transaction import (
    StockTransaction,
    StockTransactionType,
)
from app.repositories.product_repository import ProductRepository
from app.repositories.stock_transaction_repository import (
    StockTransactionRepository,
)
from app.services.base_service import BaseService
from app.validators.inventory_validator import InventoryValidator


class InventoryService(BaseService):
    """Inventory operations."""

    def __init__(self, session):
        super().__init__(session)

        self.products = ProductRepository(session)
        self.transactions = StockTransactionRepository(session)

    def stock_in(
        self,
        product_id: int,
        quantity: Decimal,
        reference: str | None = None,
        remarks: str | None = None,
    ) -> StockTransaction:

        InventoryValidator.validate_quantity(quantity)

        product = self.products.get(product_id)

        if product is None:
            raise ProductNotFoundError(
                f"Product {product_id} not found."
            )

        transaction = StockTransaction(
            product_id=product_id,
            transaction_type=StockTransactionType.STOCK_IN,
            quantity=quantity,
            reference=reference,
            remarks=remarks,
        )

        return self.transactions.add(transaction)

    def stock_out(
        self,
        product_id: int,
        quantity: Decimal,
        reference: str | None = None,
        remarks: str | None = None,
    ) -> StockTransaction:

        InventoryValidator.validate_quantity(quantity)

        product = self.products.get(product_id)

        if product is None:
            raise ProductNotFoundError(
                f"Product {product_id} not found."
            )

        current_stock = self.current_stock(product_id)

        if current_stock < quantity:
            raise InsufficientStockError(
                "Insufficient stock."
            )

        transaction = StockTransaction(
            product_id=product_id,
            transaction_type=StockTransactionType.STOCK_OUT,
            quantity=-quantity,
            reference=reference,
            remarks=remarks,
        )

        return self.transactions.add(transaction)

    def current_stock(
        self,
        product_id: int,
    ) -> Decimal:
        return self.transactions.get_current_stock(product_id)

    def stock_ledger(
        self,
        product_id: int,
    ):
        return self.transactions.list_by_product(product_id)