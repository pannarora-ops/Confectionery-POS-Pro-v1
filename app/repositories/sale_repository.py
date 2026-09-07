"""
Repository for Sale model.
"""

from sqlalchemy import select

from app.models.sale import Sale
from app.repositories.base_repository import BaseRepository


class SaleRepository(BaseRepository[Sale]):
    """Repository for sales."""

    model = Sale

    def get_by_invoice(self, invoice_number: str) -> Sale | None:
        statement = (
            select(Sale)
            .where(Sale.invoice_number == invoice_number)
        )
        return self.session.execute(statement).scalar_one_or_none()

    def exists(self, invoice_number: str) -> bool:
        return self.get_by_invoice(invoice_number) is not None

    def list_all(self) -> list[Sale]:
        statement = (
            select(Sale)
            .order_by(Sale.sale_date.desc())
        )
        return list(self.session.execute(statement).scalars().all())