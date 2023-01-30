import json
from get_op_data import request


def get_all_st(name, token, op_data):
    with open("JSON Requests/get_stations.json") as st_req:
        st_req = json.load(st_req)
    all_st_list = []
    st_req["variables"]["filters"]["operatorUuidIn"] = op_data[name]["uuid"]
    st_resp = request(st_req, token)
    stations = st_resp["data"]["stations"]["edges"]
    for node in stations:
        all_st_list.append([node["node"]["name"], node["node"]["uuid"]])
    return all_st_list


def get_date_info(token, date, st_list):
    # Поиск даты запуска
    with open("JSON Requests/get_date.json") as bernese_req:
        bernese_req = json.load(bernese_req)
    bernese_req["variables"]["filters"]["dateCreatedLte"] = str(date) + "T23:59:59+00:00"
    bernese_req["variables"]["filters"]["dateCreatedGte"] = str(date) + "T00:00:00+00:00"
    date_resp = request(bernese_req, token)
    real_date = date_resp["data"]["files"]["edges"][0]["node"]["dateCreatedReal"][:10]

    # Поиск обработанных станций
    with open("JSON Requests/notification.json") as noti:
        noti_req = json.load(noti)

    noti_req["variables"]["filters"]["creationDateLte"] = real_date + "T23:59:59+00:00"
    noti_req["variables"]["filters"]["creationDateGte"] = real_date + "T00:00:00+00:00"
    noti_req["variables"]["filters"].update({"messageIlike": "кластер_snx2snx на"})
    noti_resp = request(noti_req, token)
    full_snx_mes = ""
    for node in noti_resp["data"]["notifications"]["edges"]:
        full_snx_mes += str(node["node"]["jdata"])
    succeed_st = []

    for station in st_list:
        if station[1] in full_snx_mes:
            succeed_st.append(station[0])

    data = {'num_s_st': len(succeed_st), 'real_date': real_date}

    return data


# Запуск сбора всех данных и возвращает дату запуска
def start_parse(name, token, date, op_data):
    st_dict = {'all_st': None, 's_st': None, 'real_date': None}
    all_st = get_all_st(name, token, op_data)
    data = get_date_info(token, date, all_st)
    st_dict['all_st'] = len(all_st)
    st_dict['s_st'] = data['num_s_st']
    st_dict['real_date'] = data['real_date']
    return st_dict
