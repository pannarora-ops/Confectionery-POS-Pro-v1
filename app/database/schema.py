"""
Database Schema Initialization
"""

from app.database.base import Base
from app.database.connection import engine

# Register ALL Models

from app.models import (
    Batch,
    Brand,
    Category,
    Customer,
    CustomerLedger,
    Payment,
    Product,
    Purchase,
    PurchaseItem,
    Sale,
    SaleItem,
    StockTransaction,
    Supplier,
    SupplierLedger,
    Unit,
)


def create_database() -> None:
    """Create all database tables."""

    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":

    create_database()

    print("Database initialized successfully.")