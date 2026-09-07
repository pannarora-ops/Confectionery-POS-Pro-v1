"""
Sale model.
"""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class Sale(BaseModel):
    """Sales invoice."""

    __tablename__ = "sales"

    invoice_number: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
    )

    customer_id: Mapped[int | None] = mapped_column(
        ForeignKey("customers.id"),
        nullable=True,
    )

    customer_name: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    remarks: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True,
    )

    sale_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # -------------------------
    # Relationships
    # -------------------------

    customer = relationship(
        "Customer",
        back_populates="sales",
    )

    items = relationship(
        "SaleItem",
        back_populates="sale",
        cascade="all, delete-orphan",
    )

    @property
    def subtotal(self) -> Decimal:
        return sum(
            (item.amount for item in self.items),
            Decimal("0.00"),
        )

    @property
    def gst_total(self) -> Decimal:
        return sum(
            (item.gst_amount for item in self.items),
            Decimal("0.00"),
        )

    @property
    def grand_total(self) -> Decimal:
        return self.subtotal + self.gst_total

    def __repr__(self) -> str:
        return (
            f"<Sale(invoice='{self.invoice_number}')>"
        )