"""
Customer service.
"""

from app.models.customer import Customer

from app.repositories.customer_repository import (
    CustomerRepository,
)

from app.validators.customer_validator import (
    CustomerValidator,
)

from app.exceptions.custom_exceptions import (
    DuplicateCustomerError,
)


class CustomerService:
    """Business logic for customers."""

    def __init__(self, session):

        self.repository = CustomerRepository(session)

    # -------------------------------------------------
    # Create Customer
    # -------------------------------------------------

    def create_customer(
        self,
        name: str,
        phone: str | None = None,
        email: str | None = None,
        address: str | None = None,
        gst_number: str | None = None,
    ) -> Customer:

        CustomerValidator.validate_name(name)
        CustomerValidator.validate_phone(phone)

        if (
            phone is not None
            and self.repository.exists(phone)
        ):
            raise DuplicateCustomerError(
                f"Customer '{phone}' already exists."
            )

        customer = Customer(
            name=name,
            phone=phone,
            email=email,
            address=address,
            gst_number=gst_number,
        )

        return self.repository.add(customer)

    # -------------------------------------------------
    # Get All Customers
    # -------------------------------------------------

    def get_all(self):
        return self.repository.list_all()

    # Backward compatibility

    def list_all(self):
        return self.repository.list_all()

    def list_customers(self):
        return self.repository.list_all()

    # -------------------------------------------------
    # Get Customer
    # -------------------------------------------------

    def get(self, customer_id: int):
        return self.repository.get(customer_id)

    def get_customer(self, customer_id: int):
        return self.repository.get(customer_id)

    # -------------------------------------------------
    # Search
    # -------------------------------------------------

    def search(self, keyword: str):
        return self.repository.search(keyword)

    # -------------------------------------------------
    # Delete
    # -------------------------------------------------

    def delete(self, customer):
        self.repository.delete(customer)

    # -------------------------------------------------
    # Save Changes
    # -------------------------------------------------

    def update(self):
        self.repository.update()