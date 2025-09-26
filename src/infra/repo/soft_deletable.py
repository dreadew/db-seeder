from datetime import datetime
from typing import TypeVar

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.models.base import SoftDeletableEntity
from src.infra.repo.auditable import AuditableRepository

T = TypeVar("T", bound=SoftDeletableEntity)


class SoftDeletableRepository(AuditableRepository[T]):
    """
    Репозиторий для сущностей с мягким удалением
    """

    async def delete(self, session: AsyncSession, entity_id: int):
        """
        Мягкое удаление сущности
        :param session: сессия БД
        :param entity_id: идентификатор удаляемой записи
        """
        await self.__update_internal(session, entity_id, True)

    async def restore(self, session: AsyncSession, entity_id: int):
        """
        Восстановление удаленной сущности
        :param session: сессия БД
        :param entity_id: идентификатор восстанавливаемой записи
        """
        await self.__update_internal(session, entity_id, False)

    async def __update_internal(
        self, session: AsyncSession, entity_id: int, is_deleted: True
    ):
        """
        Внутренний метод для мягкого удаления
        :param session: сессия БД
        :param entity_id: идентификатор удаляемой записи
        """
        await session.execute(
            update(self.model)
            .where(self.model.id == entity_id)
            .values(is_deleted=is_deleted, updated_at=datetime.now())
            .execution_options(synchronize_session="fetch")
        )
        await session.flush()
