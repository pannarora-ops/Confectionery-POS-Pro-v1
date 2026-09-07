"""
Unit model.
"""

from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel


class Unit(BaseModel):
    """Product Unit Master."""

    __tablename__ = "units"

    # ------------------------------------------
    # Basic Information
    # ------------------------------------------

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    short_name: Mapped[str] = mapped_column(
        String(15),
        unique=True,
        nullable=False,
    )

    # ------------------------------------------
    # Unit Type
    # ------------------------------------------

    unit_type: Mapped[str] = mapped_column(
        String(20),
        default="Primary",
        nullable=False,
    )

    # Primary / Secondary

    # ------------------------------------------
    # Conversion
    # ------------------------------------------

    base_unit: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    conversion_factor: Mapped[float] = mapped_column(
        Float,
        default=1.0,
        nullable=False,
    )

    # Example:
    #
    # Box
    # Base Unit = pcs
    # Conversion = 24
    #
    # Means
    # 1 Box = 24 pcs

    # ------------------------------------------
    # Status
    # ------------------------------------------

    active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )

    # ------------------------------------------

    def __repr__(self) -> str:

        return (
            f"<Unit("
            f"id={self.id}, "
            f"name='{self.name}', "
            f"short='{self.short_name}')>"
        )