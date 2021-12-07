import main
import config
import status_base
import control
import id_city_file
import website
from loguru import logger

logger.add("debug.log", format="{time} {message}")


@logger.catch
def handler_user(id: str, text_user: str) -> None:
    """
    Функция - обработчик сообщений пользователя. Пользователь идентифицируется по id
    """
    param = ["Укажите минимальную цену отеля.", "Укажите максимальную цену отеля.",
             "Укажите максимальное расстояние от центра", "Сколько отелей вывести (не более 25)?"]

    if text_user in [config.Status_user_base.S_LOWPRICE.value,
                         config.Status_user_base.S_HIGHPRICE.value, config.Status_user_base.S_BESTDEAL.value]:
        status_base.set_user_status(id_user=id, value=text_user)
        main.print_user(id=id, text="Введите город, в котором будет осуществляться поиск.")

    elif status_base.get_user_status(id_user=id)[0] == config.Status_user_base.S_START.value:
        website.photo_hotels(id_user=id, id_hotel=text_user)

    elif status_base.get_user_status(id_user=id)[0] == config.Status_user_base.S_BESTDEAL.value:
        len_base = len(status_base.get_user_status(id_user=id))
        if len_base == 1:
            id_city_file.id_user_city(id=id, user_city=text_user)
        elif len_base == 6:
            if control.control_type(id=id, text_user=text_user):
                main.list_city_user(id=id, count_hotel=text_user)
        elif len_base >= 1:
            main.print_user(id=id, text=param[len_base-2])
            if control.control_type(id=id, text_user=text_user):
                status_base.set_append_value(id_user=id, value=text_user)
        print(status_base.get_user_status(id_user=id))

    elif status_base.get_user_status(id_user=id)[0] in [config.Status_user_base.S_LOWPRICE.value,
                                                        config.Status_user_base.S_HIGHPRICE.value]:
        len_base = len(status_base.get_user_status(id_user=id))
        if len_base == 1:
            id_city_file.id_user_city(id=id, user_city=text_user)

        elif len_base == 2:
            status_base.set_append_value(id_user=id, value=text_user)
            main.print_user(id=id, text=param[-1])

        elif len_base == 3:
            if control.control_type(id=id, text_user=text_user):
                main.list_city_user(id=id, count_hotel=text_user)

    else:
        main.print_user(id=id, text="Наберите /help")
