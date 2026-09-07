"""
Product Service
Commercial POS Version
"""

from __future__ import annotations

from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.product import Product
from app.repositories.product_repository import ProductRepository


class ProductService:

    def __init__(self, session: Session):

        self.session = session
        self.repo = ProductRepository(session)

    # -------------------------------------------------
    # Product Create
    # -------------------------------------------------

    def create(self, **data):

        # Auto Product Number

        if not data.get("product_no"):

            data["product_no"] = (
                self.repo.generate_product_no()
            )

        # SKU Validation

        if self.repo.sku_exists(data["sku"]):

            raise ValueError(
                "SKU already exists."
            )

        # Barcode Validation

        barcode = data.get("barcode")

        if barcode:

            if self.repo.barcode_exists(barcode):

                raise ValueError(
                    "Barcode already exists."
                )

        # Default Prices

        data.setdefault(
            "purchase_price",
            Decimal("0.00"),
        )

        data.setdefault(
            "selling_price",
            Decimal("0.00"),
        )

        data.setdefault(
            "mrp",
            Decimal("0.00"),
        )

        data.setdefault(
            "gst_percent",
            Decimal("0.00"),
        )

        data.setdefault(
            "gst_type",
            "Exclusive",
        )

        data.setdefault(
            "conversion_factor",
            1,
        )

        data.setdefault(
            "active",
            True,
        )

        product = Product(**data)

        self.repo.create(product)

        self.session.commit()

        return product

    # -------------------------------------------------
    # Product Update
    # -------------------------------------------------

    def update(
        self,
        product_id: int,
        **data,
    ):

        product = self.repo.get(product_id)

        if not product:

            raise ValueError(
                "Product not found."
            )

        sku = data.get("sku")

        if sku:

            if self.repo.sku_exists(
                sku,
                exclude_id=product.id,
            ):

                raise ValueError(
                    "SKU already exists."
                )

        barcode = data.get("barcode")

        if barcode:

            if self.repo.barcode_exists(
                barcode,
                exclude_id=product.id,
            ):

                raise ValueError(
                    "Barcode already exists."
                )

        for key, value in data.items():

            setattr(
                product,
                key,
                value,
            )

        self.repo.update()

        self.session.commit()

        return product

    # -------------------------------------------------
    # Delete
    # -------------------------------------------------

    def delete(
        self,
        product_id: int,
    ):

        product = self.repo.get(product_id)

        if not product:

            return

        self.repo.delete(product)

        self.session.commit()

    # -------------------------------------------------
    # Listing
    # -------------------------------------------------

    def get(
        self,
        product_id: int,
    ):

        return self.repo.get(product_id)

    def get_all(self):

        return self.repo.get_all()

    def get_active(self):

        return self.repo.get_active()

    # -------------------------------------------------
    # Search
    # -------------------------------------------------

    def search(
        self,
        text: str,
    ):

        return self.repo.search(text)

    # -------------------------------------------------
    # Stock
    # -------------------------------------------------

    def low_stock(self):

        return self.repo.low_stock_products()