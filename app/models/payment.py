"""
Payment Model
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import Base


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    sale_id: Mapped[int] = mapped_column(
        ForeignKey("sales.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    payment_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
    )

    payment_mode: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12,2),
        nullable=False,
        default=0,
    )

    reference_no: Mapped[str | None] = mapped_column(
        String(100),
    )

    transaction_id: Mapped[str | None] = mapped_column(
        String(100),
    )

    bank_name: Mapped[str | None] = mapped_column(
        String(100),
    )

    card_last4: Mapped[str | None] = mapped_column(
        String(4),
    )

    approval_code: Mapped[str | None] = mapped_column(
        String(50),
    )

    payment_status: Mapped[str] = mapped_column(
        String(20),
        default="Success",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
    )

    sale = relationship(
        "Sale",
        back_populates="payments",
    )