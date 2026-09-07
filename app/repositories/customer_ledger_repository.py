"""
Customer Ledger repository.
"""

from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.customer_ledger import CustomerLedger
from app.repositories.base_repository import BaseRepository


class CustomerLedgerRepository(
    BaseRepository[CustomerLedger]
):
    """Repository for Customer Ledger."""

    model = CustomerLedger

    def __init__(self, session: Session):
        super().__init__(session)

    def list_by_customer(
        self,
        customer_id: int,
    ) -> list[CustomerLedger]:

        stmt = (
            select(CustomerLedger)
            .where(
                CustomerLedger.customer_id == customer_id
            )
            .order_by(CustomerLedger.id)
        )

        return list(
            self.session.execute(stmt).scalars().all()
        )

    def current_balance(
        self,
        customer_id: int,
    ) -> Decimal:

        stmt = (
            select(
                func.coalesce(
                    func.sum(CustomerLedger.debit),
                    0,
                ),
                func.coalesce(
                    func.sum(CustomerLedger.credit),
                    0,
                ),
            )
            .where(
                CustomerLedger.customer_id == customer_id
            )
        )

        debit, credit = self.session.execute(
            stmt
        ).one()

        return Decimal(debit) - Decimal(credit)