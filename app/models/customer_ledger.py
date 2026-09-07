"""
Customer Ledger model.
"""

from __future__ import annotations

from decimal import Decimal
from enum import Enum

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel


class CustomerLedgerType(str, Enum):
    SALE = "SALE"
    PAYMENT = "PAYMENT"
    ADJUSTMENT = "ADJUSTMENT"


class CustomerLedger(BaseModel):
    """Customer Ledger."""

    __tablename__ = "customer_ledgers"

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False,
    )

    transaction_type: Mapped[CustomerLedgerType] = mapped_column(
        SqlEnum(CustomerLedgerType),
        nullable=False,
    )

    reference_number: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    debit: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=Decimal("0.00"),
        nullable=False,
    )

    credit: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=Decimal("0.00"),
        nullable=False,
    )

    balance: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=Decimal("0.00"),
        nullable=False,
    )

    remarks: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    customer = relationship(
        "Customer",
        back_populates="ledger_entries",
    )

    def __repr__(self) -> str:
        return (
            f"<CustomerLedger("
            f"id={self.id}, "
            f"customer_id={self.customer_id}, "
            f"balance={self.balance})>"
        )