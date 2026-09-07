"""
Stock Transaction Model
Commercial POS Version
"""

from __future__ import annotations

from decimal import Decimal

from sqlalchemy import (
    ForeignKey,
    Numeric,
    String,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models.base_model import BaseModel


class StockTransaction(BaseModel):
    """Stock Movement History"""

    __tablename__ = "stock_transactions"

    # -------------------------------------------------
    # Product
    # -------------------------------------------------

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )

    product = relationship(
        "Product",
        back_populates="stock_transactions",
    )

    # -------------------------------------------------
    # Transaction
    # -------------------------------------------------

    transaction_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
    )

    # OPENING
    # PURCHASE
    # SALE
    # PURCHASE_RETURN
    # SALES_RETURN
    # ADJUSTMENT
    # DAMAGE
    # EXPIRED

    # -------------------------------------------------
    # Quantity
    # -------------------------------------------------

    quantity: Mapped[Decimal] = mapped_column(
        Numeric(14,3),
        nullable=False,
    )

    # -------------------------------------------------
    # Units
    # -------------------------------------------------

    primary_unit: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    secondary_unit: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    conversion_factor: Mapped[Decimal] = mapped_column(
        Numeric(12,4),
        default=Decimal("1"),
    )

    # -------------------------------------------------
    # Rates
    # -------------------------------------------------

    purchase_rate: Mapped[Decimal] = mapped_column(
        Numeric(12,2),
        default=Decimal("0"),
    )

    sale_rate: Mapped[Decimal] = mapped_column(
        Numeric(12,2),
        default=Decimal("0"),
    )

    mrp: Mapped[Decimal] = mapped_column(
        Numeric(12,2),
        default=Decimal("0"),
    )

    # -------------------------------------------------
    # Batch
    # -------------------------------------------------

    batch_no: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    serial_no: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    expiry_date: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    # -------------------------------------------------
    # Reference
    # -------------------------------------------------

    reference_type: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    # PURCHASE
    # SALE
    # ADJUSTMENT

    reference_id: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    reference_no: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    # -------------------------------------------------
    # Remarks
    # -------------------------------------------------

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # -------------------------------------------------

    def __repr__(self):

        return (
            f"<StockTransaction("
            f"id={self.id}, "
            f"product={self.product_id}, "
            f"type='{self.transaction_type}', "
            f"qty={self.quantity})>"
        )