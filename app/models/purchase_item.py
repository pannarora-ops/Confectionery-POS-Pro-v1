"""
Purchase Item model.
"""

from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class PurchaseItem(BaseModel):
    """Purchase invoice line."""

    __tablename__ = "purchase_items"

    purchase_id: Mapped[int] = mapped_column(
        ForeignKey("purchases.id"),
        nullable=False,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
    )

    quantity: Mapped[Decimal] = mapped_column(
        Numeric(10, 3),
        nullable=False,
    )

    rate: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    gst_percent: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=0,
    )

    purchase = relationship(
        "Purchase",
        back_populates="items",
    )

    product = relationship(
        "Product",
    )

    @property
    def amount(self) -> Decimal:
        return self.quantity * self.rate

    @property
    def gst_amount(self) -> Decimal:
        return (
            self.amount * self.gst_percent
        ) / Decimal("100")

    @property
    def total(self) -> Decimal:
        return self.amount + self.gst_amount

    def __repr__(self) -> str:
        return (
            f"<PurchaseItem("
            f"purchase_id={self.purchase_id}, "
            f"product_id={self.product_id})>"
        )