"""
Sale Model
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
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


class Sale(Base):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    invoice_no: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
    )

    invoice_type: Mapped[str] = mapped_column(
        String(20),
        default="Retail",
    )

    sale_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
    )

    customer_id: Mapped[int | None] = mapped_column(
        ForeignKey("customers.id"),
        nullable=True,
    )

    cashier_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    gross_amount: Mapped[Decimal] = mapped_column(
        Numeric(12,2),
        default=0,
    )

    discount_amount: Mapped[Decimal] = mapped_column(
        Numeric(12,2),
        default=0,
    )

    taxable_amount: Mapped[Decimal] = mapped_column(
        Numeric(12,2),
        default=0,
    )

    cgst_amount: Mapped[Decimal] = mapped_column(
        Numeric(12,2),
        default=0,
    )

    sgst_amount: Mapped[Decimal] = mapped_column(
        Numeric(12,2),
        default=0,
    )

    igst_amount: Mapped[Decimal] = mapped_column(
        Numeric(12,2),
        default=0,
    )

    cess_amount: Mapped[Decimal] = mapped_column(
        Numeric(12,2),
        default=0,
    )

    round_off: Mapped[Decimal] = mapped_column(
        Numeric(12,2),
        default=0,
    )

    grand_total: Mapped[Decimal] = mapped_column(
        Numeric(12,2),
        default=0,
    )

    received_amount: Mapped[Decimal] = mapped_column(
        Numeric(12,2),
        default=0,
    )

    balance_amount: Mapped[Decimal] = mapped_column(
        Numeric(12,2),
        default=0,
    )

    loyalty_earned: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    loyalty_redeemed: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    payment_status: Mapped[str] = mapped_column(
        String(20),
        default="Paid",
    )

    sale_status: Mapped[str] = mapped_column(
        String(20),
        default="Completed",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
    )

    is_hold: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    items = relationship(
        "SaleItem",
        back_populates="sale",
        cascade="all, delete-orphan",
    )

    payments = relationship(
        "Payment",
        back_populates="sale",
        cascade="all, delete-orphan",
    )