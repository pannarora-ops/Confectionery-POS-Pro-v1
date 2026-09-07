"""
Repository for Customer model.
"""

from sqlalchemy import select

from app.models.customer import Customer
from app.repositories.base_repository import BaseRepository


class CustomerRepository(BaseRepository[Customer]):
    """Repository for customer operations."""

    model = Customer

    def get_by_phone(
        self,
        phone: str,
    ) -> Customer | None:
        statement = (
            select(Customer)
            .where(Customer.phone == phone)
        )

        return self.session.execute(
            statement
        ).scalar_one_or_none()

    def get_by_name(
        self,
        name: str,
    ) -> Customer | None:
        statement = (
            select(Customer)
            .where(Customer.name == name)
        )

        return self.session.execute(
            statement
        ).scalar_one_or_none()

    def exists(
        self,
        phone: str,
    ) -> bool:
        return self.get_by_phone(phone) is not None

    def search(
        self,
        keyword: str,
    ) -> list[Customer]:
        statement = (
            select(Customer)
            .where(
                Customer.name.contains(keyword)
            )
            .order_by(Customer.name)
        )

        return list(
            self.session.execute(statement)
            .scalars()
            .all()
        )