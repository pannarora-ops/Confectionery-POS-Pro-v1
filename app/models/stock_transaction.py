"""
Stock transaction model.
"""

from decimal import Decimal
from enum import Enum

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class StockTransactionType(str, Enum):
    """Types of stock transactions."""

    STOCK_IN = "STOCK_IN"
    STOCK_OUT = "STOCK_OUT"
    PURCHASE = "PURCHASE"
    SALE = "SALE"
    RETURN_IN = "RETURN_IN"
    RETURN_OUT = "RETURN_OUT"
    ADJUSTMENT = "ADJUSTMENT"


class StockTransaction(BaseModel):
    """Inventory stock movement."""

    __tablename__ = "stock_transactions"

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
    )

    transaction_type: Mapped[StockTransactionType] = mapped_column(
        SqlEnum(StockTransactionType),
        nullable=False,
    )

    quantity: Mapped[Decimal] = mapped_column(
        Numeric(10, 3),
        nullable=False,
    )

    reference: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    remarks: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    product = relationship(
        "Product",
        backref="stock_transactions",
    )

    def __repr__(self) -> str:
        return (
            f"<StockTransaction("
            f"product_id={self.product_id}, "
            f"type={self.transaction_type}, "
            f"qty={self.quantity})>"
        )