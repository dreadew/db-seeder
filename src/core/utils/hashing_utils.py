import bcrypt


def hash_password(password: str):
    """
    Функция для хэширования пароля
    :param password: пароль для хэширования
    :return: хэшированный пароль
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def check_password(password: str, hashed_password: str):
    """
    Функция для проверки пароля
    :param password: пароль, введенный пользователем
    :param hashed_password: хэшированный пароль
    :return: результат проверки
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
