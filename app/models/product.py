"""
Product model.
Commercial POS Version
"""

from decimal import Decimal

from sqlalchemy import (
    Boolean,
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


class Product(BaseModel):
    """Product Master"""

    __tablename__ = "products"

    # ---------------------------------------
    # Identification
    # ---------------------------------------

    product_no: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
    )

    sku: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    barcode: Mapped[str | None] = mapped_column(
        String(100),
        unique=True,
        nullable=True,
        index=True,
    )

    manufacturer_serial_no: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    # ---------------------------------------
    # Basic Information
    # ---------------------------------------

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ---------------------------------------
    # Category / Brand
    # ---------------------------------------

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        nullable=False,
    )

    brand_id: Mapped[int | None] = mapped_column(
        ForeignKey("brands.id"),
        nullable=True,
    )

    category = relationship(
        "Category",
        back_populates="products",
    )

    brand = relationship(
        "Brand",
        back_populates="products",
    )

    # ---------------------------------------
    # GST
    # ---------------------------------------

    hsn_code: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    gst_percent: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        default=Decimal("0.00"),
    )

    gst_type: Mapped[str] = mapped_column(
        String(20),
        default="Exclusive",
        nullable=False,
    )

    # ---------------------------------------
    # Pricing
    # ---------------------------------------

    purchase_price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=Decimal("0.00"),
    )

    selling_price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=Decimal("0.00"),
    )

    mrp: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=Decimal("0.00"),
    )

    # ---------------------------------------
    # Units
    # ---------------------------------------

    primary_unit_id: Mapped[int] = mapped_column(
        ForeignKey("units.id"),
        nullable=False,
    )

    secondary_unit_id: Mapped[int | None] = mapped_column(
        ForeignKey("units.id"),
        nullable=True,
    )

    conversion_factor: Mapped[float] = mapped_column(
        default=1.0,
    )

    primary_unit = relationship(
        "Unit",
        foreign_keys=[primary_unit_id],
    )

    secondary_unit = relationship(
        "Unit",
        foreign_keys=[secondary_unit_id],
    )

    # ---------------------------------------
    # Stock
    # ---------------------------------------

    opening_stock: Mapped[float] = mapped_column(
        default=0,
    )

    minimum_stock: Mapped[float] = mapped_column(
        default=0,
    )

    maximum_stock: Mapped[float] = mapped_column(
        default=0,
    )

    reorder_level: Mapped[float] = mapped_column(
        default=0,
    )

    # ---------------------------------------
    # Image
    # ---------------------------------------

    image_path: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # ---------------------------------------
    # Status
    # ---------------------------------------

    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    # ---------------------------------------
    # Relationships
    # ---------------------------------------

    stock_transactions = relationship(
        "StockTransaction",
        back_populates="product",
        cascade="all, delete-orphan",
    )

    purchase_items = relationship(
        "PurchaseItem",
        back_populates="product",
    )

    sale_items = relationship(
        "SaleItem",
        back_populates="product",
    )

    # ---------------------------------------

    def __repr__(self):

        return (
            f"<Product("
            f"id={self.id}, "
            f"product_no='{self.product_no}', "
            f"name='{self.name}')>"
        )