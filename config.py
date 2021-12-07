from enum import Enum
import main
from sqlitedict import SqliteDict


status_file = SqliteDict("cache.sqlite3", autocommit=True)


class Status_user_base(Enum):
    S_START = "0"
    S_LOWPRICE = "PRICE"
    S_HIGHPRICE = "PRICE_HIGHEST_FIRST"
    S_BESTDEAL = "DISTANCE_FROM_LANDMARK"
    S_HELP = "help"
    S_HISTORY = "history"


text_user = {
    Status_user_base.S_LOWPRICE.value: "● /lowprice — вывод самых дешёвых отелей в городе.",
    Status_user_base.S_HIGHPRICE.value: "● /highprice — вывод самых дорогих отелей в городе.",
    Status_user_base.S_BESTDEAL.value: "● /bestdeal — вывод отелей, наиболее подходящих по цене "
                                       "и расположению от центра.",
    Status_user_base.S_HELP.value: "●/help — помощь.",
    Status_user_base.S_START.value: "●/stop — начать с начала.",
    Status_user_base.S_HISTORY.value: "●/history — история поиска."
}
