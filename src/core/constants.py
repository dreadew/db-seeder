from src.core.utils.hashing_utils import hash_password

AMENITIES_LIST = [
    "WiFi",
    "Кондиционер",
    "Телевизор",
    "Мини-холодильник",
    "Фен",
    "Сейф",
    "Кофемашина",
    "Гладильная доска",
    "Ванна",
    "Душ",
    "Балкон",
    "Рабочий стол",
    "Телефон",
    "Чайник",
    "Полотенца",
    "Зеркало",
    "Шампунь",
    "Парковка",
    "Бассейн",
    "Фитнес-зал",
]

LOCATION_TYPES = [
    {"name": "Город", "short_name": "г", "description": "Крупный населённый пункт"},
    {"name": "Деревня", "short_name": "д", "description": "Сельский населённый пункт"},
    {"name": "Посёлок", "short_name": "п", "description": "Небольшой населённый пункт"},
    {"name": "ПГТ", "short_name": "пгт", "description": "Посёлок городского типа"},
]

ROOM_TYPES = [
    {"name": "Стандарт", "description": "Стандартный номер для 1-2 человек"},
    {"name": "Люкс", "description": "Улучшенный номер с дополнительными удобствами"},
    {"name": "Апартаменты", "description": "Номер с кухней и несколькими комнатами"},
    {"name": "Семейный", "description": "Просторный номер для всей семьи"},
]

BOOKING_STATUSES = [
    {"name": "В обработке"},
    {"name": "Подтверждено"},
    {"name": "Отменено"},
    {"name": "Завершено"},
]

USERS = [
    {
        "email": "admin@example.com",
        "first_name": "Admin",
        "last_name": "User",
        "phone_number": "+79000000000",
        "hashed_password": hash_password("admin123"),
    },
    {
        "email": "user@example.com",
        "first_name": "Test",
        "last_name": "User",
        "phone_number": "+79110000000",
        "hashed_password": hash_password("user123"),
    },
]
