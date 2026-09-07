"""
Supplier service.
"""

from app.models.supplier import Supplier

from app.repositories.supplier_repository import (
    SupplierRepository,
)

from app.validators.supplier_validator import (
    SupplierValidator,
)

from app.exceptions.custom_exceptions import (
    DuplicateSupplierError,
)


class SupplierService:
    """Business logic for suppliers."""

    def __init__(self, session):

        self.repository = SupplierRepository(session)

    # -------------------------------------------------
    # Create Supplier
    # -------------------------------------------------

    def create_supplier(
        self,
        name: str,
        phone: str | None = None,
        email: str | None = None,
        address: str | None = None,
        gst_number: str | None = None,
    ) -> Supplier:

        SupplierValidator.validate_name(name)
        SupplierValidator.validate_phone(phone)

        if (
            phone is not None
            and self.repository.exists(phone)
        ):
            raise DuplicateSupplierError(
                f"Supplier '{phone}' already exists."
            )

        supplier = Supplier(
            name=name,
            phone=phone,
            email=email,
            address=address,
            gst_number=gst_number,
        )

        return self.repository.add(supplier)

    # -------------------------------------------------
    # Get All Suppliers
    # -------------------------------------------------

    def get_all(self):
        return self.repository.list_all()

    def list_all(self):
        return self.repository.list_all()

    def list_suppliers(self):
        return self.repository.list_all()

    # -------------------------------------------------
    # Get Supplier
    # -------------------------------------------------

    def get(self, supplier_id: int):
        return self.repository.get(supplier_id)

    def get_supplier(self, supplier_id: int):
        return self.repository.get(supplier_id)

    # -------------------------------------------------
    # Search
    # -------------------------------------------------

    def search(self, keyword: str):
        return self.repository.search(keyword)

    # -------------------------------------------------
    # Delete
    # -------------------------------------------------

    def delete(self, supplier):
        self.repository.delete(supplier)

    # -------------------------------------------------
    # Save Changes
    # -------------------------------------------------

    def update(self):
        self.repository.update()