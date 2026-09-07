"""
Business logic for Unit.
"""

from app.exceptions.custom_exceptions import ValidationError
from app.models.unit import Unit
from app.repositories.unit_repository import UnitRepository
from app.services.base_service import BaseService


class UnitService(BaseService):
    """Service for Unit operations."""

    def __init__(self, session):
        super().__init__(session)

        self.repository = UnitRepository(session)

    # -------------------------------------------------
    # Get All
    # -------------------------------------------------

    def get_all(self) -> list[Unit]:
        """Return all units."""
        return self.repository.list_all()

    # -------------------------------------------------
    # Get Active
    # -------------------------------------------------

    def get_active(self) -> list[Unit]:
        """Return only active units."""
        return self.repository.get_active()

    # -------------------------------------------------
    # Get By ID
    # -------------------------------------------------

    def get(self, unit_id: int) -> Unit | None:
        """Return unit by ID."""
        return self.repository.get(unit_id)

    # -------------------------------------------------
    # Search
    # -------------------------------------------------

    def search(self, keyword: str) -> list[Unit]:
        """Search units."""
        keyword = keyword.strip()

        if not keyword:
            return self.get_all()

        return self.repository.search(keyword)

    # -------------------------------------------------
    # Create
    # -------------------------------------------------

    def create_unit(
        self,
        name: str,
        short_name: str,
        active: bool = True,
    ) -> Unit:
        """Create new unit."""

        name = name.strip()
        short_name = short_name.strip()

        if not name:
            raise ValidationError(
                "Unit name is required."
            )

        if not short_name:
            raise ValidationError(
                "Short name is required."
            )

        if self.repository.exists(name):
            raise ValidationError(
                f"Unit '{name}' already exists."
            )

        unit = Unit(
            name=name,
            short_name=short_name,
            active=active,
        )

        return self.repository.add(unit)

    # -------------------------------------------------
    # Update
    # -------------------------------------------------

    def update_unit(
        self,
        unit_id: int,
        name: str,
        short_name: str,
        active: bool,
    ) -> Unit | None:
        """Update unit."""

        unit = self.repository.get(unit_id)

        if unit is None:
            return None

        name = name.strip()
        short_name = short_name.strip()

        if not name:
            raise ValidationError(
                "Unit name is required."
            )

        if not short_name:
            raise ValidationError(
                "Short name is required."
            )

        duplicate = self.repository.get_by_name(name)

        if (
            duplicate
            and duplicate.id != unit.id
        ):
            raise ValidationError(
                f"Unit '{name}' already exists."
            )

        unit.name = name
        unit.short_name = short_name
        unit.active = active

        self.repository.update()

        return unit

    # -------------------------------------------------
    # Delete
    # -------------------------------------------------

    def delete_unit(
        self,
        unit_id: int,
    ) -> bool:
        """Delete unit."""

        unit = self.repository.get(unit_id)

        if unit is None:
            return False

        self.repository.delete(unit)

        return True