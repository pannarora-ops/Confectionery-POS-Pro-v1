"""
Ledger service.
"""

from decimal import Decimal

from app.models.customer_ledger import (
    CustomerLedger,
    CustomerLedgerType,
)
from app.models.supplier_ledger import (
    SupplierLedger,
    SupplierLedgerType,
)
from app.repositories.customer_ledger_repository import (
    CustomerLedgerRepository,
)
from app.repositories.supplier_ledger_repository import (
    SupplierLedgerRepository,
)


class LedgerService:
    """Customer & Supplier Ledger Service."""

    def __init__(self, session):
        self.session = session
        self.customer_repo = CustomerLedgerRepository(session)
        self.supplier_repo = SupplierLedgerRepository(session)

    # --------------------------------------------------
    # Customer Ledger
    # --------------------------------------------------

    def customer_sale(
        self,
        customer_id: int,
        amount: Decimal,
        reference: str,
        remarks: str | None = None,
    ) -> CustomerLedger:

        balance = (
            self.customer_repo.current_balance(customer_id)
            + amount
        )

        entry = CustomerLedger(
            customer_id=customer_id,
            transaction_type=CustomerLedgerType.SALE,
            reference_number=reference,
            debit=amount,
            credit=Decimal("0.00"),
            balance=balance,
            remarks=remarks,
        )

        return self.customer_repo.add(entry)

    def customer_payment(
        self,
        customer_id: int,
        amount: Decimal,
        reference: str,
        remarks: str | None = None,
    ) -> CustomerLedger:

        balance = (
            self.customer_repo.current_balance(customer_id)
            - amount
        )

        entry = CustomerLedger(
            customer_id=customer_id,
            transaction_type=CustomerLedgerType.PAYMENT,
            reference_number=reference,
            debit=Decimal("0.00"),
            credit=amount,
            balance=balance,
            remarks=remarks,
        )

        return self.customer_repo.add(entry)

    # --------------------------------------------------
    # Supplier Ledger
    # --------------------------------------------------

    def supplier_purchase(
        self,
        supplier_id: int,
        amount: Decimal,
        reference: str,
        remarks: str | None = None,
    ) -> SupplierLedger:

        balance = (
            self.supplier_repo.current_balance(supplier_id)
            + amount
        )

        entry = SupplierLedger(
            supplier_id=supplier_id,
            transaction_type=SupplierLedgerType.PURCHASE,
            reference_number=reference,
            debit=amount,
            credit=Decimal("0.00"),
            balance=balance,
            remarks=remarks,
        )

        return self.supplier_repo.add(entry)

    def supplier_payment(
        self,
        supplier_id: int,
        amount: Decimal,
        reference: str,
        remarks: str | None = None,
    ) -> SupplierLedger:

        balance = (
            self.supplier_repo.current_balance(supplier_id)
            - amount
        )

        entry = SupplierLedger(
            supplier_id=supplier_id,
            transaction_type=SupplierLedgerType.PAYMENT,
            reference_number=reference,
            debit=Decimal("0.00"),
            credit=amount,
            balance=balance,
            remarks=remarks,
        )

        return self.supplier_repo.add(entry)

    # --------------------------------------------------
    # Balance
    # --------------------------------------------------

    def customer_balance(
        self,
        customer_id: int,
    ) -> Decimal:

        return self.customer_repo.current_balance(
            customer_id
        )

    def supplier_balance(
        self,
        supplier_id: int,
    ) -> Decimal:

        return self.supplier_repo.current_balance(
            supplier_id
        )