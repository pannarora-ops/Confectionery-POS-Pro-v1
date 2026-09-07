"""
Business logic for Category.
"""

from app.exceptions.custom_exceptions import (
    DuplicateCategoryError,
)

from app.models.category import Category
from app.repositories.category_repository import (
    CategoryRepository,
)
from app.services.base_service import BaseService
from app.validators.category_validator import (
    CategoryValidator,
)


class CategoryService(BaseService):
    """Category Service."""

    def __init__(self, session):

        super().__init__(session)

        self.repository = CategoryRepository(session)

    # -------------------------------------------------
    # Get All
    # -------------------------------------------------

    def get_all(self):

        return self.repository.list_all()

    list_all = get_all

    # -------------------------------------------------
    # Get
    # -------------------------------------------------

    def get(self, category_id):

        return self.repository.get(category_id)

    # -------------------------------------------------
    # Create
    # -------------------------------------------------

    def create_category(
        self,
        name,
        description=None,
    ):

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

    create = create_category

    # -------------------------------------------------
    # Update
    # -------------------------------------------------

    def update_category(

        self,

        category_id,

        name,

        description=None,

    ):

        category = self.repository.get(category_id)

        if category is None:

            return None

        CategoryValidator.validate_name(name)

        duplicate = self.repository.get_by_name(
            name.strip()
        )

        if (
            duplicate
            and duplicate.id != category.id
        ):

            raise DuplicateCategoryError(
                "Category already exists."
            )

        category.name = name.strip()

        category.description = description

        self.repository.update()

        return category

    update = update_category

    # -------------------------------------------------
    # Delete
    # -------------------------------------------------

    def delete_category(
        self,
        category_id,
    ):

        category = self.repository.get(category_id)

        if category is None:

            return False

        # Prevent deleting category
        # if products exist.

        if (
            hasattr(category, "products")
            and len(category.products) > 0
        ):

            raise Exception(
                "Cannot delete category.\n"
                "Products exist under this category."
            )

        self.repository.delete(category)

        return True

    delete = delete_category

    # -------------------------------------------------
    # Search
    # -------------------------------------------------

    def search(self, keyword):

        keyword = keyword.lower()

        return [

            c

            for c in self.repository.list_all()

            if keyword in c.name.lower()

        ]

    # -------------------------------------------------
    # Count
    # -------------------------------------------------

    def count(self):

        return len(
            self.repository.list_all()
        )