"""
Category model.
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class Category(BaseModel):
    """Product category."""

    __tablename__ = "categories"

    # -------------------------------------------------
    # Basic Information
    # -------------------------------------------------

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )

    # -------------------------------------------------
    # Relationships
    # -------------------------------------------------

    products = relationship(
        "Product",
        back_populates="category",
        cascade="all, save-update",
    )

    # -------------------------------------------------

    @property
    def product_count(self) -> int:
        """Return total products in this category."""
        return len(self.products)

    # -------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"<Category("
            f"id={self.id}, "
            f"name='{self.name}')>"
        )