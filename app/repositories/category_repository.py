"""
Repository for Category model.
"""

from sqlalchemy import select

from app.models.category import Category
from app.repositories.base_repository import BaseRepository

class CategoryRepository(BaseRepository[Category]):
    """Repository for category operations."""
    model = Category

    def get_by_name(self, name: str) -> Category | None:
        """Return category by name."""
        statement = select(Category).where(Category.name == name)
        return self.session.execute(statement).scalar_one_or_none()

    def exists(self, name: str) -> bool:
        """Check if a category already exists."""
        return self.get_by_name(name) is not None

    def list_all(self) -> list[Category]:
        """Return all categories."""
        statement = select(Category).order_by(Category.name)
        return list(self.session.execute(statement).scalars().all())