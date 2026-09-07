"""
Payment service.
"""

from decimal import Decimal

from app.models.payment import (
    Payment,
    PaymentMode,
    PaymentType,
)

from app.repositories.payment_repository import (
    PaymentRepository,
)
from app.repositories.customer_repository import (
    CustomerRepository,
)
from app.repositories.supplier_repository import (
    SupplierRepository,
)

from app.exceptions.custom_exceptions import (
    CustomerNotFoundError,
    SupplierNotFoundError,
)


class PaymentService:
    """Business logic for payments."""

    def __init__(self, session):
        self.session = session

        self.payment_repository = PaymentRepository(session)
        self.customer_repository = CustomerRepository(session)
        self.supplier_repository = SupplierRepository(session)

    def receive_customer_payment(
        self,
        customer_id: int,
        amount: Decimal,
        payment_mode: PaymentMode = PaymentMode.CASH,
        reference_number: str | None = None,
        remarks: str | None = None,
    ) -> Payment:

        customer = self.customer_repository.get(customer_id)

        if customer is None:
            raise CustomerNotFoundError(
                f"Customer {customer_id} not found."
            )

        payment = Payment(
            payment_type=PaymentType.CUSTOMER,
            customer_id=customer_id,
            amount=amount,
            payment_mode=payment_mode,
            reference_number=reference_number,
            remarks=remarks,
        )

        return self.payment_repository.add(payment)

    def pay_supplier(
        self,
        supplier_id: int,
        amount: Decimal,
        payment_mode: PaymentMode = PaymentMode.CASH,
        reference_number: str | None = None,
        remarks: str | None = None,
    ) -> Payment:

        supplier = self.supplier_repository.get(
            supplier_id
        )

        if supplier is None:
            raise SupplierNotFoundError(
                f"Supplier {supplier_id} not found."
            )

        payment = Payment(
            payment_type=PaymentType.SUPPLIER,
            supplier_id=supplier_id,
            amount=amount,
            payment_mode=payment_mode,
            reference_number=reference_number,
            remarks=remarks,
        )

        return self.payment_repository.add(payment)

    def list_payments(self) -> list[Payment]:
        """Return all payments."""
        return self.payment_repository.list_all()

    def customer_payments(
        self,
        customer_id: int,
    ) -> list[Payment]:
        """Return customer payments."""
        return self.payment_repository.by_customer(
            customer_id
        )

    def supplier_payments(
        self,
        supplier_id: int,
    ) -> list[Payment]:
        """Return supplier payments."""
        return self.payment_repository.by_supplier(
            supplier_id
        )