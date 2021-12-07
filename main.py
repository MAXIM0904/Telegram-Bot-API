import telebot
import os
import control
import config
import keyboard
import handler
import website
import status_base
import id_city_file
import history
from loguru import logger
from dotenv import load_dotenv


logger.add("debug.log", format="{time} {message}")
load_dotenv()
bot = telebot.TeleBot(os.environ.get("BOT_TOKEN"))


@logger.catch
def print_user(id: str, text: str, keyboard=None) -> None:
    """
    Единая функция для вывода сообщений пользователю.
    """
    bot.send_message(id, text, reply_markup=keyboard, disable_web_page_preview=True)


@logger.catch
def photo(id: str, img: str) -> None:
    """
    Единая функция для вывода фотографий пользователю.
    """
    bot.send_photo(id, img)


@logger.catch
def del_status(id: str, text: str) -> None:
    """
    Единая функция для вывода сброса параметров предыдущего сеанса работы.
    """
    status_base.set_user_status(id, config.Status_user_base.S_START.value)
    keyboard.get_markup(id_chat=id,
                        text=text, user_message=config.text_user)


@logger.catch
def list_city_user(id: str, count_hotel: str) -> None:
    """
     Функция обработки сообщений. Направляет собранную от пользователя информацию для поиска отелей в выбранном городе
    """
    print_user(id=id, text="Уже ищу варианты. Поиск может занять время.")
    user_text = status_base.get_user_status(id)
    count = int(count_hotel)
    if len(status_base.get_user_status(id)) == 3:
        website.search_city_id(id=id, price_filter=user_text[0], city=user_text[2],
                               language=user_text[1], counter=count)

    else:
        website.search_city_id(id=id, price_filter=user_text[0], city=user_text[2], language=user_text[1],
                               counter=count, user_min_price=user_text[3], user_max_price=user_text[4])


@logger.catch
@bot.message_handler(commands=["start", "help", "stop", "history"])
def send_welcome(message):
    """
    Функция обработки команд "start", "help", "stop", "history", введенных пользователем
    """
    history.set_history_append(id_user=message.chat.id, value=message.text, time=website.history_time(message.chat.id))
    if message.text in ["/start",  "/help"]:
        keyboard.get_markup(id_chat=message.chat.id, text="Привет. Я бот. Выбери команду.",
                            user_message=config.text_user)
    elif message.text == "/stop":
        del_status(id=message.chat.id, text="Параметры сброшены. Начнем с начала.")
    elif message.text == "/history":
        for i_history in history.get_history_status(id_user=call.message.chat.id):
            print_user(id=call.message.chat.id, text=i_history)


@logger.catch
@bot.message_handler(func=lambda message: True)
def text_handler(message):
    """
    Функция передает сообщения, введенные пользователем в hendler.
    """
    history.set_history_append(id_user=message.chat.id, value=message.text, time=website.history_time(message.chat.id))
    handler.handler_user(id=message.chat.id, text_user=message.text)


@logger.catch
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    """
    Функция обработки сообщений с инлайн клавиатуры. Передает сообщения в hendler.
    Обрабатывает команды "start", "help", "stop", "history"
    """
    if call.message:
        history.set_history_append(id_user=call.message.chat.id, value=call.data,
                                   time=website.history_time(call.message.chat.id))
        print(history.get_history_status(id_user=call.message.chat.id))
        print(call.data)
        if call.data == config.Status_user_base.S_START.value:
            del_status(id=call.message.chat.id, text="Параметры сброшены. Начнем с начала.")

        elif call.data == config.Status_user_base.S_HELP.value:
            keyboard.get_markup(id_chat=call.message.chat.id, text="Помощь пришла. Выбирай.",
                                user_message=config.text_user)

        elif call.data == config.Status_user_base.S_HISTORY.value:
            for i_history in history.get_history_status(id_user=call.message.chat.id):
                print_user(id=call.message.chat.id, text=i_history)
        else:
            handler.handler_user(id=call.message.chat.id, text_user=call.data)


if __name__ == "__main__":
    logger.info("Запуск бота(info)")
    bot.infinity_polling()
