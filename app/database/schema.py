"""
Database schema initialization.
"""

from app.database.base import Base
from app.database.connection import engine


# Import all models here
from app.models import Category, Product
from app.models import StockTransaction

def create_database() -> None:
    """
    Create all database tables.
    """
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_database()
    print("Database initialized successfully.")