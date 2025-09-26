import asyncio

from dotenv import load_dotenv


async def seed_static_data():
    """
    Функция для генерации константных данных
    """

    from src.core.constants import (BOOKING_STATUSES, LOCATION_TYPES,
                                    ROOM_TYPES, USERS)
    from src.core.utils.logging import get_logger
    from src.infra.db import PostgresDB

    logger = get_logger(__name__)
    logger.info("Начинается вставка константных данных")

    db = PostgresDB()
    logger.info("Соединение с БД получено")

    await asyncio.gather(
        db.insert_batch_data_into_table_async("location_types", LOCATION_TYPES, 10),
        db.insert_batch_data_into_table_async("room_types", ROOM_TYPES, 10),
        db.insert_batch_data_into_table_async("users", USERS, 10),
        db.insert_batch_data_into_table_async("booking_statuses", BOOKING_STATUSES, 10),
    )
    logger.info("Константные данные и тестовые пользователи успешно вставлены")


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(seed_static_data())
