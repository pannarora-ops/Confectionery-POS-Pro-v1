"""
Product Repository
Commercial POS Version
"""

from __future__ import annotations

from sqlalchemy import or_, func
from sqlalchemy.orm import Session

from app.models.product import Product


class ProductRepository:

    def __init__(self, session: Session):
        self.session = session

    # -------------------------------------------------
    # CRUD
    # -------------------------------------------------

    def create(self, product: Product):

        self.session.add(product)
        self.session.flush()

        return product

    def update(self):

        self.session.flush()

    def delete(self, product: Product):

        self.session.delete(product)

    # -------------------------------------------------
    # Find
    # -------------------------------------------------

    def get(self, product_id: int):

        return (
            self.session.query(Product)
            .filter(Product.id == product_id)
            .first()
        )

    def get_by_product_no(
        self,
        product_no: str,
    ):

        return (
            self.session.query(Product)
            .filter(
                Product.product_no == product_no
            )
            .first()
        )

    def get_by_sku(
        self,
        sku: str,
    ):

        return (
            self.session.query(Product)
            .filter(
                Product.sku == sku
            )
            .first()
        )

    def get_by_barcode(
        self,
        barcode: str,
    ):

        return (
            self.session.query(Product)
            .filter(
                Product.barcode == barcode
            )
            .first()
        )

    # -------------------------------------------------
    # Listing
    # -------------------------------------------------

    def get_all(self):

        return (
            self.session.query(Product)
            .order_by(Product.name)
            .all()
        )

    def get_active(self):

        return (
            self.session.query(Product)
            .filter(Product.active.is_(True))
            .order_by(Product.name)
            .all()
        )

    def get_inactive(self):

        return (
            self.session.query(Product)
            .filter(Product.active.is_(False))
            .order_by(Product.name)
            .all()
        )

    # -------------------------------------------------
    # Search
    # -------------------------------------------------

    def search(
        self,
        text: str,
    ):

        if not text:

            return self.get_all()

        text = f"%{text}%"

        return (
            self.session.query(Product)
            .filter(
                or_(
                    Product.product_no.ilike(text),
                    Product.name.ilike(text),
                    Product.sku.ilike(text),
                    Product.barcode.ilike(text),
                    Product.hsn_code.ilike(text),
                )
            )
            .order_by(Product.name)
            .all()
        )

    # -------------------------------------------------
    # Stock
    # -------------------------------------------------

    def low_stock_products(self):

        return (
            self.session.query(Product)
            .filter(
                Product.opening_stock
                <= Product.reorder_level
            )
            .all()
        )

    # -------------------------------------------------
    # Auto Product Number
    # -------------------------------------------------

    def generate_product_no(self):

        last = (
            self.session.query(
                func.max(Product.id)
            )
            .scalar()
        )

        if not last:

            return "PRD000001"

        return f"PRD{last+1:06d}"

    # -------------------------------------------------
    # Duplicate Validation
    # -------------------------------------------------

    def sku_exists(
        self,
        sku: str,
        exclude_id=None,
    ):

        query = (
            self.session.query(Product)
            .filter(Product.sku == sku)
        )

        if exclude_id:

            query = query.filter(
                Product.id != exclude_id
            )

        return query.first() is not None

    def barcode_exists(
        self,
        barcode: str,
        exclude_id=None,
    ):

        if not barcode:

            return False

        query = (
            self.session.query(Product)
            .filter(
                Product.barcode == barcode
            )
        )

        if exclude_id:

            query = query.filter(
                Product.id != exclude_id
            )

        return query.first() is not None