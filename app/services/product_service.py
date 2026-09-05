"""
Business logic for Product.
"""

from decimal import Decimal

from app.exceptions.custom_exceptions import (
    CategoryNotFoundError,
    DuplicateSKUError,
)
from app.models.product import Product
from app.repositories.category_repository import CategoryRepository
from app.repositories.product_repository import ProductRepository
from app.services.base_service import BaseService
from app.validators.product_validator import ProductValidator


class ProductService(BaseService):
    """Service for product operations."""

    def __init__(self, session):
        super().__init__(session)
        self.product_repository = ProductRepository(session)
        self.category_repository = CategoryRepository(session)

    def create_product(
        self,
        name: str,
        sku: str,
        purchase_price: Decimal,
        selling_price: Decimal,
        category_id: int,
        description: str | None = None,
        barcode: str | None = None,
        gst_percent: Decimal = Decimal("0.00"),
        unit: str = "pcs",
        min_stock: int = 0,
    ) -> Product:
        """Create a new product."""

        ProductValidator.validate_name(name)
        ProductValidator.validate_sku(sku)
        ProductValidator.validate_price(purchase_price)
        ProductValidator.validate_price(selling_price)

        if self.product_repository.exists(sku):
            raise DuplicateSKUError(
                f"SKU '{sku}' already exists."
            )

        category = self.category_repository.get(category_id)

        if category is None:
            raise CategoryNotFoundError(
                f"Category ID {category_id} not found."
            )

        product = Product(
            name=name.strip(),
            sku=sku.strip().upper(),
            barcode=barcode,
            description=description,
            category_id=category_id,
            purchase_price=purchase_price,
            selling_price=selling_price,
            gst_percent=gst_percent,
            unit=unit,
            min_stock=min_stock,
        )

        return self.product_repository.add(product)