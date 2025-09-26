from abc import ABC, abstractmethod
from typing import Any, Dict, List


class Database(ABC):
    """
    Абстрактный интерфейс БД
    """

    @abstractmethod
    async def insert_data_into_table_async(
        self, table_name: str, data: List[Dict[str, Any]]
    ):
        """
        Вставить данные в таблицу
        :param table_name: название таблицы
        :param data: данные для вставки
        """
        pass

    @abstractmethod
    async def insert_batch_data_into_table_async(
        self, table_name: str, data: List[Dict[str, Any]]
    ):
        """
        Вставить данные батчами
        :param table_name: название таблицы
        :param data: данные для вставки
        """
        pass

    @abstractmethod
    async def get_all_ids_async(self, table_name: str, id_column: str = "id"):
        """
        Получить все идентификаторы записей
        :param table_name: название таблицы
        :param id_column: название столбца идентификатора
        """
        pass

    @abstractmethod
    async def close(self):
        """
        Закрыть соединение
        """
        pass
