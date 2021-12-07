import requests
import json
import os
import keyboard
import main
from dotenv import load_dotenv
import re
import status_base
from loguru import logger

logger.add("debug.log", format="{time} {message}")
load_dotenv()
token = os.environ.get("RAPIDAPI_KEY")


@logger.catch
def id_user_city(id: str, user_city: str) -> str:
    '''
    Функция получает json файл, обрабатывает его. Возвращает id города
    '''
    main.print_user(id=id, text="Ищу. Поиск может занять время.")
    dict_id = {}
    url = "https://hotels4.p.rapidapi.com/locations/search"
    city = user_city.lower()
    language = "ru_RU" if re.match(r"[А-Яа-яЁё]+", city) else "en_US"
    status_base.set_append_value(id_user=id, value=language)
    querystring = {"query": city, "locale": language}
    headers = {
        'x-rapidapi-key': token,
        'x-rapidapi-host': "hotels4.p.rapidapi.com"
        }
    try:
        response = requests.request("GET", url, headers=headers, params=querystring, timeout=10)
    except requests.Timeout as error:
        logger.exception(error)
        return False
    print(response.status_code)

    if response.status_code == 200:
        response_id_city = response.json()
    else:
        main.print_user(id=id, text="Ошибка соединения")
        logger.error("Ошибка id_user_city response_id_city(debug)")
        return False

    for i_id_city in response_id_city["suggestions"][0]["entities"]:
        title = i_id_city["caption"]
        name_city = re.sub(r"<[^>]*>|h", "", title)
        dict_id[i_id_city['destinationId']] = name_city
    keyboard.get_markup(id_chat=id, text="Совпадения по названию города. Нажми на нужный.", user_message=dict_id)
    return dict_id
