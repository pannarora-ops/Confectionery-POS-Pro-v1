"""
Base service class.
"""

from sqlalchemy.orm import Session


class BaseService:
    """Base class for all services."""

    def __init__(self, session: Session):
        self.session = session