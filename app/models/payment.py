"""
Payment model.
"""

from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import (
    DateTime,
    Enum as SqlEnum,
    ForeignKey,
    Numeric,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models.base_model import BaseModel


class PaymentType(str, Enum):
    CUSTOMER = "CUSTOMER"
    SUPPLIER = "SUPPLIER"


class PaymentMode(str, Enum):
    CASH = "CASH"
    UPI = "UPI"
    CARD = "CARD"
    BANK = "BANK"


class Payment(BaseModel):
    """Customer/Supplier payment."""

    __tablename__ = "payments"

    payment_type: Mapped[PaymentType] = mapped_column(
        SqlEnum(PaymentType),
        nullable=False,
    )

    customer_id: Mapped[int | None] = mapped_column(
        ForeignKey("customers.id"),
        nullable=True,
    )

    supplier_id: Mapped[int | None] = mapped_column(
        ForeignKey("suppliers.id"),
        nullable=True,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    payment_mode: Mapped[PaymentMode] = mapped_column(
        SqlEnum(PaymentMode),
        default=PaymentMode.CASH,
        nullable=False,
    )

    reference_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    remarks: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True,
    )

    payment_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # -------------------------
    # Relationships
    # -------------------------

    customer = relationship(
        "Customer",
        back_populates="payments",
    )

    supplier = relationship(
        "Supplier",
        back_populates="payments",
    )

    def __repr__(self) -> str:
        return (
            f"<Payment(id={self.id}, "
            f"amount={self.amount})>"
        )