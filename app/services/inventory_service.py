"""
Inventory service.
"""

from decimal import Decimal

from sqlalchemy import select

from app.models.product import Product
from app.models.stock_transaction import (
    StockTransactionType,
)


class InventoryService:
    """Inventory related business logic."""

    def __init__(self, session):
        self.session = session

    # ---------------------------------------
    # Current Stock
    # ---------------------------------------

    def current_stock(
        self,
        product_id: int,
    ) -> Decimal:

        product = self.session.get(
            Product,
            product_id,
        )

        if product is None:
            return Decimal("0.000")

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

        return qty

    # ---------------------------------------
    # Stock Value
    # ---------------------------------------

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

            total += (
                self.current_stock(product.id)
                * product.purchase_price
            )

        return total

    # ---------------------------------------
    # Product Summary
    # ---------------------------------------

    def product_summary(
        self,
        product_id: int,
    ) -> dict:

        product = self.session.get(
            Product,
            product_id,
        )

        if product is None:
            raise ValueError(
                "Product not found."
            )

        stock = self.current_stock(
            product.id
        )

        return {
            "id": product.id,
            "sku": product.sku,
            "name": product.name,
            "stock": stock,
            "purchase_price": product.purchase_price,
            "selling_price": product.selling_price,
            "stock_value": (
                stock
                * product.purchase_price
            ),
        }

    # ---------------------------------------
    # All Products
    # ---------------------------------------

    def inventory(self) -> list[dict]:

        products = (
            self.session.execute(
                select(Product)
            )
            .scalars()
            .all()
        )

        data = []

        for product in products:

            stock = self.current_stock(
                product.id
            )

            data.append(
                {
                    "id": product.id,
                    "sku": product.sku,
                    "name": product.name,
                    "stock": stock,
                    "purchase_price": product.purchase_price,
                    "selling_price": product.selling_price,
                    "stock_value": (
                        stock
                        * product.purchase_price
                    ),
                }
            )

        return data

    # ---------------------------------------
    # Low Stock
    # ---------------------------------------

    def low_stock_products(
        self,
    ) -> list[dict]:

        products = []

        for item in self.inventory():

            product = self.session.get(
                Product,
                item["id"],
            )

            if (
                item["stock"]
                <= product.min_stock
            ):
                products.append(item)

        return products

    # ---------------------------------------
    # Out of Stock
    # ---------------------------------------

    def out_of_stock_products(
        self,
    ) -> list[dict]:

        return [
            item
            for item in self.inventory()
            if item["stock"] <= 0
        ]