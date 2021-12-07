from telebot import types
import main
from loguru import logger

logger.add("debug.log", format="{time} {message}")


@logger.catch
def get_markup(id_chat: str, text: str, user_message: dict) -> None:
    """
    Функция для формирования клавиатуры и вывода информации пользователю
    """
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for key, value in user_message.items():
        callback_button = types.InlineKeyboardButton(text=value, callback_data=key)
        keyboard.add(callback_button)
    main.print_user(id_chat, text, keyboard=keyboard)
