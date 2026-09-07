"""
Custom exceptions used across the application.
"""


class POSException(Exception):
    """Base exception for the application."""


class ValidationError(POSException):
    """Raised when validation fails."""


# -------------------------
# Category
# -------------------------

class DuplicateCategoryError(POSException):
    """Raised when category already exists."""


class CategoryNotFoundError(POSException):
    """Raised when category is not found."""


# -------------------------
# Product
# -------------------------

class DuplicateSKUError(POSException):
    """Raised when SKU already exists."""


class ProductNotFoundError(POSException):
    """Raised when product is not found."""


# -------------------------
# Supplier
# -------------------------

class DuplicateSupplierError(POSException):
    """Raised when supplier already exists."""


class SupplierNotFoundError(POSException):
    """Raised when supplier does not exist."""


# -------------------------
# Customer
# -------------------------

class DuplicateCustomerError(POSException):
    """Raised when customer already exists."""


class CustomerNotFoundError(POSException):
    """Raised when customer does not exist."""


# -------------------------
# Invoice
# -------------------------

class DuplicateInvoiceError(POSException):
    """Raised when invoice already exists."""


# -------------------------
# Inventory
# -------------------------

class InsufficientStockError(POSException):
    """Raised when stock is insufficient."""