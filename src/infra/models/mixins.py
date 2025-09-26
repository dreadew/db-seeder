from sqlalchemy import Column, String
from sqlalchemy.orm import declared_attr


class NamedMixin:
    """
    Mixin для наименования
    """

    @classmethod
    @declared_attr
    def name(cls):
        return Column(String(cls.__name_length__), unique=True, nullable=False)


class ShortNameMixin:
    """
    Mixin для короткого наименования
    """

    @classmethod
    @declared_attr
    def short_name(cls):
        return Column(String(cls.__short_name_length__), unique=True, nullable=False)
