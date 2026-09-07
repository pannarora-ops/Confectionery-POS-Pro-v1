"""
Repository for Supplier model.
"""

from sqlalchemy import select

from app.models.supplier import Supplier
from app.repositories.base_repository import BaseRepository


class SupplierRepository(BaseRepository[Supplier]):
    """Repository for supplier operations."""

    model = Supplier

    def get_by_name(self, name: str) -> Supplier | None:
        statement = select(Supplier).where(Supplier.name == name)
        return self.session.execute(statement).scalar_one_or_none()

    def exists(self, name: str) -> bool:
        return self.get_by_name(name) is not None

    def list_all(self) -> list[Supplier]:
        statement = select(Supplier).order_by(Supplier.name)
        return list(self.session.execute(statement).scalars().all())