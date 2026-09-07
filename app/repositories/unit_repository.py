"""
Repository for Unit operations.
"""

from sqlalchemy import select

from app.models.unit import Unit
from app.repositories.base_repository import BaseRepository


class UnitRepository(BaseRepository[Unit]):
    """Repository for Unit."""

    model = Unit

    # -------------------------------------------------
    # Get by Name
    # -------------------------------------------------

    def get_by_name(
        self,
        name: str,
    ) -> Unit | None:

        statement = (
            select(Unit)
            .where(Unit.name == name)
        )

        return (
            self.session.execute(statement)
            .scalar_one_or_none()
        )

    # -------------------------------------------------
    # Exists
    # -------------------------------------------------

    def exists(
        self,
        name: str,
    ) -> bool:

        return self.get_by_name(name) is not None

    # -------------------------------------------------
    # Active Units
    # -------------------------------------------------

    def get_active(self) -> list[Unit]:

        statement = (
            select(Unit)
            .where(Unit.active.is_(True))
            .order_by(Unit.name)
        )

        return list(
            self.session.execute(statement)
            .scalars()
            .all()
        )

    # -------------------------------------------------
    # All Units
    # -------------------------------------------------

    def list_all(self) -> list[Unit]:

        statement = (
            select(Unit)
            .order_by(Unit.name)
        )

        return list(
            self.session.execute(statement)
            .scalars()
            .all()
        )

    # -------------------------------------------------
    # Search
    # -------------------------------------------------

    def search(
        self,
        keyword: str,
    ) -> list[Unit]:

        statement = (
            select(Unit)
            .where(
                Unit.name.ilike(f"%{keyword}%")
            )
            .order_by(Unit.name)
        )

        return list(
            self.session.execute(statement)
            .scalars()
            .all()
        )