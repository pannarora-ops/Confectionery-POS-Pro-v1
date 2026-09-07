"""
Purchase model.
"""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class Purchase(BaseModel):
    """Purchase invoice."""

    __tablename__ = "purchases"

    invoice_number: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
    )

    supplier_id: Mapped[int] = mapped_column(
        ForeignKey("suppliers.id"),
        nullable=False,
    )

    remarks: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True,
    )

    purchase_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # -------------------------
    # Relationships
    # -------------------------

    supplier = relationship(
        "Supplier",
        back_populates="purchases",
    )

    items = relationship(
        "PurchaseItem",
        back_populates="purchase",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<Purchase(invoice='{self.invoice_number}')>"
        )