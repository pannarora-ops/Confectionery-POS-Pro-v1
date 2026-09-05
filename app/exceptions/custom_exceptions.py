"""
Custom exceptions used across the application.
"""


class POSException(Exception):
    """Base exception for the application."""


class ValidationError(POSException):
    """Raised when validation fails."""


class DuplicateCategoryError(POSException):
    """Raised when category already exists."""


class DuplicateSKUError(POSException):
    """Raised when SKU already exists."""


class CategoryNotFoundError(POSException):
    """Raised when category is not found."""


class ProductNotFoundError(POSException):
    """Raised when product is not found."""

class ProductNotFoundError(Exception):
    """Raised when product does not exist."""


class InsufficientStockError(Exception):
    """Raised when stock is insufficient."""