"""
Database schema initialization.
"""

from app.database.base import Base
from app.database.connection import engine

# Import ALL models so SQLAlchemy registers them
from app.models import (
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
)


def create_database() -> None:
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_database()
    print("Database initialized successfully.")