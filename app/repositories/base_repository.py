"""
Generic repository for CRUD operations.
"""

from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """Generic repository providing common CRUD operations."""

    model: type[ModelType]

    def __init__(self, session: Session):
        self.session = session

    def add(self, obj: ModelType) -> ModelType:
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def get(self, obj_id: int) -> ModelType | None:
        return self.session.get(self.model, obj_id)

    def list_all(self) -> list[ModelType]:
        statement = select(self.model)
        return list(self.session.execute(statement).scalars().all())

    def update(self) -> None:
        self.session.commit()

    def delete(self, obj: ModelType) -> None:
        self.session.delete(obj)
        self.session.commit()