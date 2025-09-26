import asyncio

from dotenv import load_dotenv


async def stream_data(batch_size: int):
    """
    Функция для батчевой генерации данных
    :param batch_size: размер батча
    """

    from src.core.utils.logging import get_logger
    from src.infra.db import PostgresDB
    from src.seed.generation_funcs import (generate_addresses,
                                           generate_bookings, generate_hotels,
                                           generate_locations,
                                           generate_reviews,
                                           generate_room_amenities,
                                           generate_rooms,
                                           generate_search_history)

    logger = get_logger(__name__)
    logger.info("Начинается seeding данных в основные таблицы")

    db = PostgresDB()
    logger.info("Соединение с БД получено")
    while True:
        logger.info("Генерация новой партии данных...")

        (
            country_ids,
            location_type_ids,
            location_ids,
            address_ids,
            hotel_ids,
            room_type_ids,
            user_ids,
            room_ids,
            amenity_ids,
            booking_status_ids,
        ) = await asyncio.gather(
            db.get_all_ids_async("countries"),
            db.get_all_ids_async("location_types"),
            db.get_all_ids_async("locations"),
            db.get_all_ids_async("addresses"),
            db.get_all_ids_async("hotels"),
            db.get_all_ids_async("room_types"),
            db.get_all_ids_async("users"),
            db.get_all_ids_async("rooms"),
            db.get_all_ids_async("amenities"),
            db.get_all_ids_async("booking_statuses"),
        )

        if len(location_ids) == 0:
            await db.insert_batch_data_into_table_async(
                "locations",
                generate_locations(batch_size, country_ids, location_type_ids),
            )
            continue

        if len(address_ids) == 0:
            await db.insert_batch_data_into_table_async(
                "addresses", generate_addresses(batch_size, location_ids)
            )
            continue

        if len(hotel_ids) == 0:
            await db.insert_batch_data_into_table_async(
                "hotels", generate_hotels(batch_size, address_ids)
            )
            continue

        if len(room_ids) == 0:
            await db.insert_batch_data_into_table_async(
                "rooms", generate_rooms(batch_size, hotel_ids, room_type_ids)
            )
            continue

        await asyncio.gather(
            db.insert_batch_data_into_table_async(
                "locations",
                generate_locations(batch_size, country_ids, location_type_ids),
            ),
            db.insert_batch_data_into_table_async(
                "addresses", generate_addresses(batch_size, location_ids)
            ),
            db.insert_batch_data_into_table_async(
                "hotels", generate_hotels(batch_size, address_ids)
            ),
            db.insert_batch_data_into_table_async(
                "rooms", generate_rooms(batch_size, hotel_ids, room_type_ids)
            ),
            db.insert_batch_data_into_table_async(
                "room_amenities", generate_room_amenities(room_ids, amenity_ids)
            ),
            db.insert_batch_data_into_table_async(
                "bookings",
                generate_bookings(batch_size, user_ids, room_ids, booking_status_ids),
            ),
            db.insert_batch_data_into_table_async(
                "reviews", generate_reviews(batch_size, user_ids, hotel_ids)
            ),
            db.insert_batch_data_into_table_async(
                "search_history",
                generate_search_history(batch_size, user_ids, location_ids),
            ),
        )

        logger.info(
            f"> Вставлено по {batch_size} записей в зависимые таблицы."
            + f"\n> Ожидание {config.SEED_TIMEOUT_S} секунд..."
        )
        await asyncio.sleep(config.SEED_TIMEOUT_S)


if __name__ == "__main__":
    load_dotenv()

    from src.core.config import config

    asyncio.run(stream_data(config.SEED_BATCH_SIZE))
