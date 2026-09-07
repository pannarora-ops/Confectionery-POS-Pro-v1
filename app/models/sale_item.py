"""
Sale Item Model
"""

from __future__ import annotations

from decimal import Decimal

from sqlalchemy import (
    ForeignKey,
    Integer,
    Numeric,
    String,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import Base


class SaleItem(Base):
    __tablename__ = "sale_items"

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

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )

    batch_id: Mapped[int] = mapped_column(
        ForeignKey("batches.id"),
        nullable=False,
        index=True,
    )

    product_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    product_code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    barcode: Mapped[str | None] = mapped_column(
        String(100),
    )

    batch_no: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    expiry_date: Mapped[str | None] = mapped_column(
        String(20),
    )

    qty: Mapped[Decimal] = mapped_column(
        Numeric(12,3),
        default=0,
    )

    free_qty: Mapped[Decimal] = mapped_column(
        Numeric(12,3),
        default=0,
    )

    unit: Mapped[str] = mapped_column(
        String(20),
        default="PCS",
    )

    cost_price: Mapped[Decimal] = mapped_column(
        Numeric(12,2),
        default=0,
    )

    sale_price: Mapped[Decimal] = mapped_column(
        Numeric(12,2),
        default=0,
    )

    discount_percent: Mapped[Decimal] = mapped_column(
        Numeric(5,2),
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

    gst_percent: Mapped[Decimal] = mapped_column(
        Numeric(5,2),
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

    line_total: Mapped[Decimal] = mapped_column(
        Numeric(12,2),
        default=0,
    )

    profit_amount: Mapped[Decimal] = mapped_column(
        Numeric(12,2),
        default=0,
    )

    margin_percent: Mapped[Decimal] = mapped_column(
        Numeric(5,2),
        default=0,
    )

    sale = relationship(
        "Sale",
        back_populates="items",
    )

    product = relationship(
        "Product",
    )

    batch = relationship(
        "Batch",
    )