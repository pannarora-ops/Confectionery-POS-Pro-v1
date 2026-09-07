"""
Seed database with sample data.
"""

from decimal import Decimal

from app.database.session import get_session
from app.models.category import Category
from app.models.customer import Customer
from app.models.product import Product
from app.models.supplier import Supplier


def seed() -> None:
    session = get_session()

    # -------------------------
    # Category
    # -------------------------

    if session.query(Category).count() == 0:

        bakery = Category(
            name="Bakery",
        )

        session.add(bakery)
        session.flush()

        # -------------------------
        # Products
        # -------------------------

        session.add_all(
            [
                Product(
                    sku="P001",
                    barcode="890000000001",
                    name="Chocolate Cake",
                    category_id=bakery.id,
                    purchase_price=Decimal("200"),
                    selling_price=Decimal("250"),
                    gst_percent=Decimal("18"),
                    unit="pcs",
                    min_stock=5,
                ),
                Product(
                    sku="P002",
                    barcode="890000000002",
                    name="Black Forest Cake",
                    category_id=bakery.id,
                    purchase_price=Decimal("300"),
                    selling_price=Decimal("375"),
                    gst_percent=Decimal("18"),
                    unit="pcs",
                    min_stock=5,
                ),
            ]
        )

    # -------------------------
    # Supplier
    # -------------------------

    if session.query(Supplier).count() == 0:

        session.add(
            Supplier(
                name="ABC Suppliers",
                phone="9876543210",
            )
        )

    # -------------------------
    # Customer
    # -------------------------

    if session.query(Customer).count() == 0:

        session.add(
            Customer(
                name="Rahul",
                phone="9999999999",
            )
        )

    session.commit()

    print("Seed data inserted successfully.")


if __name__ == "__main__":
    seed()