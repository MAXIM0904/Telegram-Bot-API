import requests
import json
import time
import main
import keyboard
import history
import os
from dotenv import load_dotenv
from loguru import logger


logger.add("debug.log", format="{time} {message}")
load_dotenv()


@logger.catch
def control_float(filter_number: str) -> float:
    '''
    Функция контроля. Заменяет запятую на точку в строке чисел и переводит во float
    '''
    try:
        filter_number = float(filter_number)
        return filter_number
    except ValueError:
        filter_number = filter_number.replace(",", ".")
        return float(filter_number)


@logger.catch
def history_time(id: str) -> str:
    """
    Возвращает пользователю время
    """
    return time.strftime(f'%H:%M:%S - %d-%m-%Y')


@logger.catch
def time_user(day_out: int) -> str:
    '''
    Функция форматирует дату. Прибавляет к дате нужное количество дней

    '''
    day = int(time.strftime('%d')) + day_out
    return time.strftime(f'%Y-%m-{day}')


@logger.catch
def search_city_id(id: str, price_filter: str, city: str, language: str, counter: int,
                   user_min_price: str = None, user_max_price: str = None) -> None:
    '''
    Функция получает json файл, обрабатывает его и выдает пользователю информацию об отелях в выбранном городе.
    '''
    response_user = {}
    url = "https://hotels4.p.rapidapi.com/properties/list"
    querystring = {"destinationId": city, "pageNumber": "1", "pageSize": "25", "checkIn": time_user(day_out=0),
                   "checkOut": time_user(day_out=1), "adults1": "1", "priceMin": user_min_price,
                   "priceMax": user_max_price, "sortOrder": price_filter, "locale": language, "currency": "RUB"}
    headers = {
        'x-rapidapi-key': os.environ.get("RAPIDAPI_KEY"),
        'x-rapidapi-host': "hotels4.p.rapidapi.com"
        }
    try:
        response = requests.request("GET", url, headers=headers, params=querystring, timeout=10)
    except Exception as error:
        logger.exception(error)
        return False
    if response.status_code == 200:
        response_user = response.json()
    else:
        main.print_user(id=id, text="Ошибка соединения")
        logger.error("Ошибка search_city_id response(debug)")
        return False

    if counter > 25:
        counter = 25
        main.print_user(id=id, text="Не более 25 отелей.")

    try:
        for i_count_hotel in range(counter):
            price_current = response_user["data"]["body"]["searchResults"]["results"][i_count_hotel]\
                ["ratePlan"]["price"]["current"]
            name_hotels = response_user["data"]["body"]["searchResults"]["results"][i_count_hotel]["name"]
            address = response_user["data"]["body"]["searchResults"]["results"][i_count_hotel]["address"]
            city_center = response_user["data"]["body"]["searchResults"]["results"][i_count_hotel]\
                ["landmarks"][0]["distance"]
            web_address = f'https://hotels.com/ho' \
                          f'{response_user["data"]["body"]["searchResults"]["results"][i_count_hotel]["id"]}'
            id_hotel = response_user["data"]["body"]["searchResults"]["results"][i_count_hotel]["id"]

            text_hotel = (
                f"{i_count_hotel + 1}." +
                f"Отель - '{name_hotels}';\n" +
                f"Aдрес - {address['locality']}," +
                f"{address['streetAddress']};\n" +
                f"Pасположение от цента - {city_center};\n" +
                f"Цена - {price_current};\n" +
                f"Ссылка для бронирования - {web_address}"
            )
            history.set_history_append(id_user=id, value=text_hotel, time=history_time(id=id))
            dict_hotel = {}
            dict_hotel[id_hotel] = "Нажми для просмотра фото"
            keyboard.get_markup(id_chat=id, text=text_hotel, user_message=dict_hotel)
        main.del_status(id=id, text="Еще запрос?")
    except Exception as error:
        logger.exception(error)
        main.print_user(id=id, text="Это все выбранные отели!")
        main.del_status(id=id, text="Еще запрос?")


@logger.catch
def photo_hotels(id_user: str, id_hotel: str) -> None:
    '''
    Функция получает json файл, обрабатывает его и выдает пользователю фотографии отеля.
    '''
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    querystring = {"id": id_hotel}
    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': os.environ.get("RAPIDAPI_KEY")
    }
    try:
        response = requests.request("GET", url, headers=headers, params=querystring, timeout=10)
    except Exception as error:
        logger.exception(error)
        return False

    if response.status_code == 200:
        response_user = response.json()
    else:
        main.print_user(id=id, text="Ошибка соединения")
        logger.error("Ошибка search_city_id response(debug)")
        return False

    for i_count in range(5):
        result = response_user["hotelImages"][i_count]["baseUrl"].replace("{size}", "z")
        main.photo(id=id_user, img=result)
