"""
Validation for Product.
"""

from decimal import Decimal

from app.exceptions.custom_exceptions import ValidationError


class ProductValidator:
    """Validate product data."""

    @staticmethod
    def validate_name(name: str) -> None:
        if not name or not name.strip():
            raise ValidationError("Product name is required.")

    @staticmethod
    def validate_sku(sku: str) -> None:
        if not sku or not sku.strip():
            raise ValidationError("SKU is required.")

    @staticmethod
    def validate_price(price: Decimal) -> None:
        if price < 0:
            raise ValidationError("Price cannot be negative.")