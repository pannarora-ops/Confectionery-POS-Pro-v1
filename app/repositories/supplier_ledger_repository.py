"""
Supplier Ledger repository.
"""

from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.supplier_ledger import SupplierLedger
from app.repositories.base_repository import BaseRepository


class SupplierLedgerRepository(
    BaseRepository[SupplierLedger]
):
    """Repository for Supplier Ledger."""

    model = SupplierLedger

    def __init__(self, session: Session):
        super().__init__(session)

    def list_by_supplier(
        self,
        supplier_id: int,
    ) -> list[SupplierLedger]:

        stmt = (
            select(SupplierLedger)
            .where(
                SupplierLedger.supplier_id == supplier_id
            )
            .order_by(SupplierLedger.id)
        )

        return list(
            self.session.execute(stmt).scalars().all()
        )

    def current_balance(
        self,
        supplier_id: int,
    ) -> Decimal:

        stmt = (
            select(
                func.coalesce(
                    func.sum(SupplierLedger.debit),
                    0,
                ),
                func.coalesce(
                    func.sum(SupplierLedger.credit),
                    0,
                ),
            )
            .where(
                SupplierLedger.supplier_id == supplier_id
            )
        )

        debit, credit = self.session.execute(
            stmt
        ).one()

        return Decimal(debit) - Decimal(credit)