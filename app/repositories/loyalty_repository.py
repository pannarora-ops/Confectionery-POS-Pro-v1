"""
Loyalty repository.
"""

from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.loyalty_point import LoyaltyPoint
from app.repositories.base_repository import BaseRepository


class LoyaltyRepository(
    BaseRepository[LoyaltyPoint]
):
    """Repository for loyalty points."""

    model = LoyaltyPoint

    def __init__(self, session: Session):
        super().__init__(session)

    def list_by_customer(
        self,
        customer_id: int,
    ) -> list[LoyaltyPoint]:

        stmt = (
            select(LoyaltyPoint)
            .where(
                LoyaltyPoint.customer_id == customer_id
            )
            .order_by(LoyaltyPoint.id)
        )

        return list(
            self.session.execute(stmt).scalars().all()
        )

    def current_points(
        self,
        customer_id: int,
    ) -> Decimal:

        stmt = (
            select(
                func.coalesce(
                    func.sum(
                        LoyaltyPoint.earned_points
                    ),
                    0,
                ),
                func.coalesce(
                    func.sum(
                        LoyaltyPoint.redeemed_points
                    ),
                    0,
                ),
            )
            .where(
                LoyaltyPoint.customer_id
                == customer_id
            )
        )

        earned, redeemed = self.session.execute(
            stmt
        ).one()

        return Decimal(earned) - Decimal(redeemed)