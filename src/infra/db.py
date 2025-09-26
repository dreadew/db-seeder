from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.abstractions.db import Database
from src.core.config import config
from src.core.utils.logging import get_logger


class PostgresDB(Database):
    def __init__(self):
        self.logger = get_logger(__name__)

        self.engine = create_async_engine(
            config.PG_URL,
            echo=False,
            future=True,
            pool_size=config.POOL_SIZE,
            max_overflow=config.MAX_OVERFLOW,
            pool_timeout=config.POOL_TIMEOUT,
        )

        self.SessionLocal = sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def insert_data_into_table_async(self, table_name: str, data: list[dict]):
        columns = data[0].keys()
        col_names = ", ".join(columns)
        placeholders = ", ".join([f":{col}" for col in columns])

        sql = text(
            f"""
                INSERT INTO {table_name} ({col_names})
                VALUES ({placeholders})
                ON CONFLICT DO NOTHING
            """
        )

        async with self.SessionLocal() as session:
            async with session.begin():
                await session.execute(sql, data)

    async def insert_batch_data_into_table_async(
        self, table_name: str, data: list[dict], batch_size: int = 100
    ):
        for i in range(0, len(data), batch_size):
            await self.insert_data_into_table_async(
                table_name, data[i : i + batch_size]
            )
            self.logger.info(
                f"Обработаны записи с {i} до {min(i+batch_size, len(data))} в таблицу {table_name}"
            )

    async def get_all_ids_async(self, table_name: str, id_column: str = "id"):
        query = text(f"SELECT {id_column} FROM {table_name};")
        async with self.engine.connect() as session:
            result = await session.execute(query)
            rows = result.all()
            self.logger.info(f"Получено {len(rows)} записей из таблицы {table_name}")
            return [row[0] for row in rows]

    async def close(self):
        await self.engine.dispose()
