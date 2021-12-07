import config
import main
from loguru import logger

logger.add("debug.log", format="{time} {message}")


@logger.catch
def get_user_status(id_user: str) -> str:
    """
    Функция извлечения данных о пользователе из базы данных. Данные возвращаются в обратившуюся функцию.
    """
    try:
        return config.status_file[id_user]
    except KeyError as error:
        logger.exception(error)
        return config.Status_user_base.S_START.value


@logger.catch
def set_append_value(id_user: str, value: str) -> bool:
    """
    Функция добавления данных о пользователе в базу данных.
    """
    try:
        value_append = config.status_file.get(id_user)
        value_append.append(value)
        config.status_file[id_user] = value_append
        return True
    except Exception as error:
        logger.exception(error)
        return False


@logger.catch
def set_user_status(id_user: str, value: str) -> bool:
    """
    Функция вносит пользователя в базу данных при первом обращении.
    """
    try:
        config.status_file[id_user] = [value]
        return True
    except KeyError as error:
        logger.exception(error)
        return False
