"""
Validation for Category.
"""

from app.exceptions.custom_exceptions import ValidationError


class CategoryValidator:
    """Validate category data."""

    @staticmethod
    def validate_name(name: str) -> None:
        """Validate category name."""

        if not name:
            raise ValidationError("Category name is required.")

        if len(name.strip()) < 2:
            raise ValidationError(
                "Category name must contain at least 2 characters."
            )

        if len(name.strip()) > 100:
            raise ValidationError(
                "Category name cannot exceed 100 characters."
            )