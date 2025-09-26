from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, Text
from sqlalchemy.orm import declarative_base

from src.infra.models.mixins import NamedMixin, ShortNameMixin

Base = declarative_base()


class BaseEntity(Base):
    """
    Базовая сущность
    """

    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)


class AuditableEntity(BaseEntity):
    """
    Сущность с аудитом
    """

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)


class SoftDeletableEntity(AuditableEntity):
    """
    Сущность с мягким удалением
    """

    is_deleted = Column(Boolean, default=False)


class NamedEntity(SoftDeletableEntity, NamedMixin):
    """
    Сущность с наименованием
    """

    __name_length__ = 100


class NamedEntityWithDescription(NamedEntity):
    """
    Сущность с наименованием и описанием
    """

    description = Column(Text)


class NamedEntityWithShortName(NamedEntityWithDescription, ShortNameMixin):
    """
    Сущность с наименованием и коротким наименованием
    """

    __short_name_length__ = 10
