import main
from loguru import logger

logger.add("debug.log", format="{time} {message}")


@logger.catch
def del_number(id: str) -> bool:
    """
    Функция удаления пользователя из базы данных
    """
    try:
        del dict_number[id]
        return dict_number
    except (KeyError, NameError):
        return False


@logger.catch
def control_type(id: str, text_user: str) -> bool:
    '''
    Функция контроля ввода строки. Строка должна состоять из цифр.
    '''
    if text_user.isdigit():
        return True
    main.print_user(id=id, text="Значение необходимо ввести цифрами.")
    return False


@logger.catch
def param_control(message_user: str, param_min: str, param_max: str, user_func: str) -> bool:
    '''
    Функция контроля минимального и максимального параметра. Минимальный параметр не должен быть
    больше максимального.
    '''
    if float(param_min) > float(param_max):
        bot.send_message(message_user.chat.id,
                         f"Минимальное значение {param_min} не может быть больше максимального {param_max}")
        bot.register_next_step_handler(param_min, user_func)
    return True


dict_number = {}
