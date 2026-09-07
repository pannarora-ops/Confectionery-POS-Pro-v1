"""
Brand model.
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class Brand(BaseModel):
    """Product Brand."""

    __tablename__ = "brands"

    # ----------------------------------------
    # Basic Information
    # ----------------------------------------

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
    )

    # ----------------------------------------
    # Relationships
    # ----------------------------------------

    products = relationship(
        "Product",
        back_populates="brand",
    )

    # ----------------------------------------

    def __repr__(self):

        return (
            f"<Brand("
            f"id={self.id}, "
            f"name='{self.name}')>"
        )