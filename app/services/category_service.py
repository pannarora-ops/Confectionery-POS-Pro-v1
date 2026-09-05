"""
Business logic for Category.
"""

from app.exceptions.custom_exceptions import DuplicateCategoryError
from app.models.category import Category
from app.repositories.category_repository import CategoryRepository
from app.services.base_service import BaseService
from app.validators.category_validator import CategoryValidator


class CategoryService(BaseService):
    """Service for category operations."""

    def __init__(self, session):
        super().__init__(session)
        self.repository = CategoryRepository(session)

    def create_category(
        self,
        name: str,
        description: str | None = None,
    ) -> Category:
        """Create a new category."""

        CategoryValidator.validate_name(name)

        if self.repository.exists(name):
            raise DuplicateCategoryError(
                f"Category '{name}' already exists."
            )

        category = Category(
            name=name.strip(),
            description=description,
        )

        return self.repository.add(category)