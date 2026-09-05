"""
Product model.
"""

from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class Product(BaseModel):
    """Product master."""

    __tablename__ = "products"

    sku: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
    )

    barcode: Mapped[str | None] = mapped_column(
        String(50),
        unique=True,
        nullable=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        nullable=False,
    )

    purchase_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=0,
    )

    selling_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    gst_percent: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=0,
    )

    unit: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pcs",
    )

    min_stock: Mapped[int] = mapped_column(
        nullable=False,
        default=0,
    )

    category = relationship(
        "Category",
        backref="products",
    )

    def __repr__(self) -> str:
        return (
            f"<Product(id={self.id}, "
            f"sku='{self.sku}', "
            f"name='{self.name}')>"
        )