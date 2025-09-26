import asyncio

from dotenv import load_dotenv


async def seed_base_data():
    """
    Функция генерации данных в таблицы без зависимостей
    """

    from src.core.config import config
    from src.core.constants import AMENITIES_LIST
    from src.core.utils.logging import get_logger
    from src.infra.db import PostgresDB
    from src.seed.generation_funcs import (generate_amenities,
                                           generate_countries, generate_users)

    logger = get_logger(__name__)
    logger.info("Начинается вставка начальных данных пользователей, стран и удобств")

    db = PostgresDB()
    logger.info("Соединение с БД получено")
    countries = generate_countries(config.SEED_BASE_COUNTRIES_SIZE)
    users = generate_users(config.SEED_BASE_USERS_SIZE)
    amenities = generate_amenities(len(AMENITIES_LIST))

    await asyncio.gather(
        db.insert_batch_data_into_table_async("countries", countries, 10),
        db.insert_batch_data_into_table_async("users", users, 10),
        db.insert_batch_data_into_table_async("amenities", amenities, 10),
    )
    logger.info(
        f"Сгенерировано: {config.SEED_BASE_COUNTRIES_SIZE} стран, {config.SEED_BASE_USERS_SIZE} пользователей, {len(amenities)} удобств."
    )


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(seed_base_data())
