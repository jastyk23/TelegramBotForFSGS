import datetime
import json


from operator_stat import apk_storage
from operator_stat import get_op_data as god
from operator_stat import get_succeed_st
from operator_stat import operator_server_st as oss
from operator_stat import unsucceed_st


def check_op(name, r_date):
    # Данные входа
    login = "poshivailo_au"
    password = "a0587448"

    # Получение токена для входа
    token = god.auth(login, password)
    # Получение данных по опреторам
    god.get_op_data(token)

    # Общие данные
    max_thread = 8
    date = datetime.date.fromisoformat(r_date)
    with open("Data/operators_data.json") as data_file:
        operator_data = json.load(data_file)

    # Сбор станций на сервере оператора
    num_serv_st = oss.get_st(name, date, token)

    # Сбор обработанных станций и получение даты запуска berbese
    st_data = get_succeed_st.start_parse(name, token, date,
                                         operator_data)  # st_dict = {'all_st': int, 's_st': int, 'real_date': date}

    # Сбор станций не попавших в финальное уравнивание
    f_st = unsucceed_st.start_parse(name, st_data['real_date'], get_succeed_st.get_all_st(name, token,
                                                                                          operator_data))  # noti_st = {'er_st': int, 'lost_st': int}

    # Сбор станций из хранилища АПК
    apk_st = apk_storage.apk_raw(operator_data, date)

    return f"Оператор: {name}\nВсего станций: {st_data['all_st']}\nСтанций на сервере оператора: {num_serv_st}\nСтацний собрано АПК: {len(apk_st)}\nСтанций обработал АПК: {st_data['s_st']}\nСтанций не попавших в уравнивание: {f_st}\nСтанций не найдено: {f_st}"
