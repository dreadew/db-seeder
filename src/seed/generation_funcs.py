import random
from datetime import timedelta

from faker import Faker

from src.core.constants import AMENITIES_LIST
from src.core.utils.hashing_utils import hash_password

faker = Faker("RU-ru")


def generate_countries(n: int):
    """
    Функция генерации рандомных стран
    :param n: количество записей для генерации
    :return: список стран
    """
    return [{"name": faker.country()} for _ in range(n)]


def generate_users(n: int):
    """
    Функция генерации рандомных юзеров
    :param n: количество записей для генерации
    :return: список юзеров
    """
    list_ = []
    for _ in range(n):
        dict_ = {
            "email": faker.email(),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "hashed_password": hash_password(faker.password()),
            "phone_number": faker.phone_number(),
        }
        list_.append(dict_)
    return list_


def generate_amenities(n: int):
    """
    Функция генерации рандомных удобств номера
    :param n: список записей для генерации
    :return: список удобств
    """
    list_ = []
    for _ in range(n):
        dict_ = {"name": random.choice(AMENITIES_LIST), "description": faker.text()}
        list_.append(dict_)
    return list_


def generate_locations(n: int, country_ids: list[int], location_type_ids: list[int]):
    """
    Генерация локаций
    :param n: количество локаций
    :param country_ids: список ID стран
    :param location_type_ids: список ID типов локаций
    :return: список локаций
    """
    list_ = []
    for _ in range(n):
        location = {
            "name": faker.city(),
            "country_id": random.choice(country_ids),
            "location_type_id": random.choice(location_type_ids),
        }
        list_.append(location)
    return list_


def generate_addresses(n: int, location_ids: list[int]):
    """
    Генерация адресов
    :param n: количество адресов
    :param location_ids: список ID локаций
    :return: список адресов
    """
    list_ = []
    for _ in range(n):
        address = {
            "location_id": random.choice(location_ids),
            "street_address": faker.street_address(),
            "postal_code": faker.postcode(),
        }
        list_.append(address)
    return list_


def generate_hotels(n: int, address_ids: list[int]):
    """
    Генерация отелей
    :param n: количество отелей
    :param address_ids: список ID адресов
    :return: список отелей
    """
    list_ = []
    for _ in range(n):
        hotel = {
            "name": faker.company(),
            "address_id": random.choice(address_ids),
            "star_rating": random.randint(1, 5),
        }
        list_.append(hotel)
    return list_


def generate_rooms(n: int, hotel_ids: list[int], room_type_ids: list[int]):
    """
    Генерация номеров отелей
    :param n: количество номеров
    :param hotel_ids: список ID отелей
    :param room_type_ids: список ID типов номеров
    :return: список номеров
    """
    list_ = []
    for _ in range(n):
        room = {
            "hotel_id": random.choice(hotel_ids),
            "room_type_id": random.choice(room_type_ids),
            "room_number": str(random.randint(100, 999)),
            "price_per_night": round(random.uniform(2000, 15000), 2),
            "capacity": random.randint(1, 5),
        }
        list_.append(room)
    return list_


def generate_room_amenities(
    room_ids: list[int], amenity_ids: list[int], min_count=2, max_count=6
):
    """
    Связь комнат и удобств
    :param room_ids: список ID комнат
    :param amenity_ids: список ID удобств
    :return: список связей
    """
    relations = []
    for room_id in room_ids:
        count = random.randint(min_count, max_count)
        selected_amenities = random.sample(amenity_ids, min(count, len(amenity_ids)))
        for amenity_id in selected_amenities:
            relations.append({"room_id": room_id, "amenity_id": amenity_id})
    return relations


def generate_bookings(
    n: int, user_ids: list[int], room_ids: list[int], booking_status_ids: list[int]
):
    """
    Генерация бронирований
    """
    bookings = []
    for _ in range(n):
        user_id = random.choice(user_ids)
        room_id = random.choice(room_ids)
        status_id = random.choice(booking_status_ids)
        check_in = faker.date_between(start_date="+1d", end_date="+60d")
        check_out = check_in + timedelta(days=random.randint(1, 14))
        total_days = (check_out - check_in).days
        price_per_night = round(random.uniform(2000, 15000), 2)
        total_price = round(price_per_night * total_days, 2)

        booking = {
            "user_id": user_id,
            "room_id": room_id,
            "booking_status_id": status_id,
            "check_in_date": check_in,
            "check_out_date": check_out,
            "total_price": total_price,
        }
        bookings.append(booking)
    return bookings


def generate_reviews(n: int, user_ids: list[int], hotel_ids: list[int]):
    """
    Генерация отзывов
    """
    reviews = []
    for _ in range(n):
        review = {
            "user_id": random.choice(user_ids),
            "hotel_id": random.choice(hotel_ids),
            "rating": random.randint(1, 5),
            "comment": faker.text(max_nb_chars=200),
        }
        reviews.append(review)
    return reviews


def generate_search_history(n: int, user_ids: list[int], location_ids: list[int]):
    """
    Генерация истории поисков
    """
    history = []
    for _ in range(n):
        check_in = faker.date_between(start_date="-90d", end_date="today")
        check_out = check_in + timedelta(days=random.randint(1, 10))
        history.append(
            {
                "user_id": random.choice(user_ids),
                "location_id": random.choice(location_ids),
                "check_in_date": check_in,
                "check_out_date": check_out,
                "adults": random.randint(1, 4),
                "children": random.randint(0, 3),
            }
        )
    return history
