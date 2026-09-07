"""
Purchase repository.
"""

from sqlalchemy import select

from app.models.purchase import Purchase
from app.repositories.base_repository import BaseRepository


class PurchaseRepository(BaseRepository[Purchase]):
    """Repository for purchase operations."""

    model = Purchase

    def get_by_invoice(
        self,
        invoice_number: str,
    ) -> Purchase | None:
        """
        Return purchase by invoice number.
        """

        statement = (
            select(Purchase)
            .where(
                Purchase.invoice_number
                == invoice_number
            )
        )

        return self.session.execute(
            statement
        ).scalar_one_or_none()

    # -----------------------------------------
    # Backward Compatibility
    # -----------------------------------------

    def find_by_invoice(
        self,
        invoice_number: str,
    ) -> Purchase | None:
        """
        Alias for older service code.
        """

        return self.get_by_invoice(
            invoice_number
        )