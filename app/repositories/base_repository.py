"""
Generic repository for CRUD operations.
"""

from typing import Generic, TypeVar

from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """
    Generic repository providing common CRUD operations.
    """

    def __init__(self, session: Session):
        self.session = session

    def add(self, obj: ModelType) -> ModelType:
        """Add a new object."""
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def get_by_id(self, model: type[ModelType], obj_id: int) -> ModelType | None:
        """Get object by primary key."""
        return self.session.get(model, obj_id)

    def get_all(self, model: type[ModelType]) -> list[ModelType]:
        """Return all objects."""
        return self.session.query(model).all()

    def delete(self, obj: ModelType) -> None:
        """Delete an object."""
        self.session.delete(obj)
        self.session.commit()