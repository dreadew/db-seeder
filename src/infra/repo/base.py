from typing import Generic, Type, TypeVar

from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.infra.models.base import BaseEntity

T = TypeVar("T", bound=BaseEntity)


class BaseRepository(Generic[T]):
    """
    Базовый репозиторий для сущностей, наследуемых от BaseEntity
    """

    def __init__(self, model: Type[T]):
        self.model = model

    async def get_all(self, session: AsyncSession):
        """
        Получить все записи
        :param session: сессия БД
        :return: все записи из таблицы
        """
        result = await session.execute(select(self.model))
        return result.scalars().all()

    async def get_by_id(self, session: AsyncSession, entity_id: int):
        """
        Получить запись по идентификатору
        :param session: сессия БД
        :param entity_id: идентификатор записи
        :return: запись
        """
        result = await session.execute(
            select(self.model).where(self.model.id == entity_id)
        )
        return result.scalar_one_or_none()

    async def create(self, session: AsyncSession, obj_in: dict):
        """
        Создание записи
        :param session: сессия БД
        :param obj_in: данные для создания записи
        :return: созданная запись
        """
        obj = self.model(**obj_in)
        session.add(obj)
        await session.flush()
        return obj

    async def update(self, session: AsyncSession, entity_id: int, obj_in: dict):
        """
        Обновить запись
        :param session: сессия БД
        :param entity_id: идентифиатор записи
        :param obj_in: данные для обновления
        :return: обновленная запись
        """
        await session.execute(
            update(self.model)
            .where(self.model.id == entity_id)
            .values(**obj_in)
            .execution_options(synchronize_session="fetch")
        )
        return await self.get_by_id(entity_id)

    async def delete(self, session: AsyncSession, entity_id: int):
        """
        Удалить запись
        :param session: сессия БД
        :param entity_id: идентификатор записи
        """
        await session.execute(delete(self.model).where(self.model.id == entity_id))
