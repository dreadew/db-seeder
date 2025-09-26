from datetime import datetime
from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.models.base import AuditableEntity
from src.infra.repo.base import BaseRepository

T = TypeVar("T", bound=AuditableEntity)


class AuditableRepository(BaseRepository[T]):
    """
    Репозиторий для сущностей с аудитом
    """

    async def create(self, session: AsyncSession, obj_in: dict):
        now = datetime.now()
        obj_in["created_at"] = now
        obj_in["updated_at"] = now
        return await super().create(session, obj_in)

    async def update(self, session: AsyncSession, entity_id: int, obj_in: dict):
        obj_in["updated_at"] = datetime.now()
        return await super().update(session, entity_id, obj_in)
