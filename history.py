from sqlitedict import SqliteDict
from loguru import logger

logger.add("debug.log", format="{time} {message}")


@logger.catch
def get_history_status(id_user: str) -> str:
    """
    Функция извлечения данных о пользователе из базы данных. Данные возвращаются в обратившуюся функцию.
    """
    try:
        return history_file[id_user]
    except KeyError as error:
        logger.exception(error)
        return config.Status_user_base.S_START.value


@logger.catch
def set_history_append(id_user: str, value: str, time: str) -> bool:
    """
    Функция добавления данных о пользователе в базу данных.
    """
    try:
        value_append = history_file.get(id_user)
        value_append.append(f"{time} {value}")
        history_file[id_user] = value_append
        return True
    except Exception as error:
        history_file[id_user] = [value]
        logger.exception(error)
        return False


history_file = SqliteDict("history.sqlite3", autocommit=True)
