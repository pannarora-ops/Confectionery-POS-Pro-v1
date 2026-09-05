"""
Supplier model.
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel


class Supplier(BaseModel):
    """Supplier master."""

    __tablename__ = "suppliers"

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True,
    )

    contact_person: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    email: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    address: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True,
    )

    gst_number: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    def __repr__(self) -> str:
        return (
            f"<Supplier(id={self.id}, "
            f"name='{self.name}')>"
        )