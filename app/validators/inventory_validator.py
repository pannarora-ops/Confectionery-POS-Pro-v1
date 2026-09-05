"""
Inventory validation.
"""

from decimal import Decimal


class InventoryValidator:
    """Validator for inventory operations."""

    @staticmethod
    def validate_quantity(quantity: Decimal) -> None:
        """Validate stock quantity."""

        if quantity <= 0:
            raise ValueError(
                "Quantity must be greater than zero."
            )