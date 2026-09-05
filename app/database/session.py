"""
Database session configuration.

Provides a Session factory for interacting with the database.
"""

from sqlalchemy.orm import Session, sessionmaker

from app.database.connection import engine

# Session Factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)


def get_session() -> Session:
    """
    Create and return a new database session.
    """
    return SessionLocal()