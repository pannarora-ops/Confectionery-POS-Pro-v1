"""
Customer model.
"""

from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel


class Customer(BaseModel):
    """Customer master."""

    __tablename__ = "customers"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    phone: Mapped[str] = mapped_column(
        String(15),
        unique=True,
        nullable=False,
    )

    email: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    address: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    gst_number: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    # ---------------------------------
    # Relationships
    # ---------------------------------

    sales = relationship(
        "Sale",
        back_populates="customer",
        cascade="all, delete-orphan",
    )

    payments = relationship(
        "Payment",
        back_populates="customer",
        cascade="all, delete-orphan",
    )

    ledger_entries = relationship(
        "CustomerLedger",
        back_populates="customer",
        cascade="all, delete-orphan",
    )

    loyalty_entries = relationship(
        "LoyaltyPoint",
        back_populates="customer",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<Customer(id={self.id}, "
            f"name='{self.name}')>"
        )