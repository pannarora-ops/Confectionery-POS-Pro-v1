"""
Loyalty Point model.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel


class LoyaltyPoint(BaseModel):
    """Customer Loyalty Points."""

    __tablename__ = "loyalty_points"

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False,
    )

    earned_points: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=Decimal("0.00"),
        nullable=False,
    )

    redeemed_points: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=Decimal("0.00"),
        nullable=False,
    )

    balance_points: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=Decimal("0.00"),
        nullable=False,
    )

    reference_number: Mapped[str] = mapped_column(
        nullable=False,
    )

    transaction_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    customer = relationship(
        "Customer",
        back_populates="loyalty_entries",
    )

    def __repr__(self) -> str:
        return (
            f"<LoyaltyPoint("
            f"customer={self.customer_id}, "
            f"balance={self.balance_points})>"
        )
    