"""
Batch Master Model
"""

from __future__ import annotations

from decimal import Decimal
from datetime import date

from sqlalchemy import (
    ForeignKey,
    Numeric,
    String,
    Date,
    Boolean,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models.base_model import BaseModel


class Batch(BaseModel):
    """Product Batch"""

    __tablename__ = "batches"

    # ---------------------------------------
    # Product
    # ---------------------------------------

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )

    product = relationship(
        "Product",
        back_populates="batches",
    )

    # ---------------------------------------
    # Batch
    # ---------------------------------------

    batch_no: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    manufacture_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    expiry_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    # ---------------------------------------
    # Pricing
    # ---------------------------------------

    purchase_rate: Mapped[Decimal] = mapped_column(
        Numeric(12,2),
        default=Decimal("0.00"),
    )

    sale_rate: Mapped[Decimal] = mapped_column(
        Numeric(12,2),
        default=Decimal("0.00"),
    )

    mrp: Mapped[Decimal] = mapped_column(
        Numeric(12,2),
        default=Decimal("0.00"),
    )

    # ---------------------------------------
    # Stock
    # ---------------------------------------

    available_qty: Mapped[Decimal] = mapped_column(
        Numeric(14,3),
        default=Decimal("0"),
    )

    reserved_qty: Mapped[Decimal] = mapped_column(
        Numeric(14,3),
        default=Decimal("0"),
    )

    damaged_qty: Mapped[Decimal] = mapped_column(
        Numeric(14,3),
        default=Decimal("0"),
    )

    # ---------------------------------------
    # Status
    # ---------------------------------------

    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    def __repr__(self):

        return (
            f"<Batch("
            f"{self.batch_no}, "
            f"{self.available_qty})>"
        )