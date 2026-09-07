"""
Supplier business logic.
"""

from app.models.supplier import Supplier
from app.repositories.supplier_repository import SupplierRepository
from app.validators.supplier_validator import SupplierValidator
from app.exceptions.custom_exceptions import DuplicateSupplierError


class SupplierService:

    def __init__(self, session):
        self.repository = SupplierRepository(session)

    def create_supplier(
        self,
        name: str,
        contact_person: str | None = None,
        phone: str | None = None,
        email: str | None = None,
        address: str | None = None,
        gst_number: str | None = None,
    ) -> Supplier:

        SupplierValidator.validate_name(name)
        SupplierValidator.validate_phone(phone)

        if self.repository.exists(name):
            raise DuplicateSupplierError(
                f"Supplier '{name}' already exists."
            )

        supplier = Supplier(
            name=name,
            contact_person=contact_person,
            phone=phone,
            email=email,
            address=address,
            gst_number=gst_number,
        )

        return self.repository.add(supplier)

    def list_suppliers(self):
        return self.repository.list_all()