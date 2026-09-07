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

        self.repository = CustomerRepository(
            session
        )

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

    def list_customers(self):

        return self.repository.list_all()

    def get_customer(self, customer_id: int):

        return self.repository.get(customer_id)

    def search(self, keyword: str):

        return self.repository.search(keyword)