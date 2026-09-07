"""
Payment repository.
"""

from sqlalchemy import select

from app.models.payment import Payment
from app.repositories.base_repository import BaseRepository


class PaymentRepository(BaseRepository[Payment]):
    """Repository for payment operations."""

    model = Payment

    def list_all(self) -> list[Payment]:
        """Return all payments."""

        statement = (
            select(Payment)
            .order_by(
                Payment.payment_date.desc(),
                Payment.id.desc(),
            )
        )

        return list(
            self.session.execute(statement)
            .scalars()
            .all()
        )

    def by_customer(
        self,
        customer_id: int,
    ) -> list[Payment]:

        statement = (
            select(Payment)
            .where(
                Payment.customer_id == customer_id
            )
            .order_by(
                Payment.payment_date.desc(),
                Payment.id.desc(),
            )
        )

        return list(
            self.session.execute(statement)
            .scalars()
            .all()
        )

    def by_supplier(
        self,
        supplier_id: int,
    ) -> list[Payment]:

        statement = (
            select(Payment)
            .where(
                Payment.supplier_id == supplier_id
            )
            .order_by(
                Payment.payment_date.desc(),
                Payment.id.desc(),
            )
        )

        return list(
            self.session.execute(statement)
            .scalars()
            .all()
        )