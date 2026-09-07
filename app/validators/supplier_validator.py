"""
Supplier validation.
"""

from app.exceptions.custom_exceptions import ValidationError


class SupplierValidator:

    @staticmethod
    def validate_name(name: str) -> None:
        if not name or not name.strip():
            raise ValidationError("Supplier name cannot be empty.")

    @staticmethod
    def validate_phone(phone: str | None) -> None:
        if phone and len(phone) < 10:
            raise ValidationError(
                "Phone number must contain at least 10 digits."
            )