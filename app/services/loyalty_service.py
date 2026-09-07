"""
Loyalty service.
"""

from decimal import Decimal

from app.models.loyalty_point import LoyaltyPoint
from app.repositories.customer_repository import (
    CustomerRepository,
)
from app.repositories.loyalty_repository import (
    LoyaltyRepository,
)
from app.exceptions.custom_exceptions import (
    CustomerNotFoundError,
    ValidationError,
)


class LoyaltyService:
    """Business logic for loyalty points."""

    # ₹100 = 1 Point
    POINTS_PER_100 = Decimal("1")

    def __init__(self, session):
        self.session = session
        self.customer_repository = CustomerRepository(session)
        self.loyalty_repository = LoyaltyRepository(session)

    # ----------------------------------------
    # Add Points
    # ----------------------------------------

    def add_points(
        self,
        customer_id: int,
        bill_amount: Decimal,
        reference: str,
    ) -> LoyaltyPoint:

        customer = self.customer_repository.get(
            customer_id
        )

        if customer is None:
            raise CustomerNotFoundError(
                f"Customer {customer_id} not found."
            )

        points = (
            bill_amount // Decimal("100")
        ) * self.POINTS_PER_100

        current_balance = (
            self.loyalty_repository.current_points(
                customer_id
            )
        )

        loyalty = LoyaltyPoint(
            customer_id=customer_id,
            earned_points=points,
            redeemed_points=Decimal("0.00"),
            balance_points=current_balance + points,
            reference_number=reference,
        )

        return self.loyalty_repository.add(
            loyalty
        )

    # ----------------------------------------
    # Redeem Points
    # ----------------------------------------

    def redeem_points(
        self,
        customer_id: int,
        points: Decimal,
        reference: str,
    ) -> LoyaltyPoint:

        balance = (
            self.loyalty_repository.current_points(
                customer_id
            )
        )

        if points > balance:
            raise ValidationError(
                "Insufficient loyalty points."
            )

        loyalty = LoyaltyPoint(
            customer_id=customer_id,
            earned_points=Decimal("0.00"),
            redeemed_points=points,
            balance_points=balance - points,
            reference_number=reference,
        )

        return self.loyalty_repository.add(
            loyalty
        )

    # ----------------------------------------
    # Balance
    # ----------------------------------------

    def current_points(
        self,
        customer_id: int,
    ) -> Decimal:

        return (
            self.loyalty_repository.current_points(
                customer_id
            )
        )