from get_op_data import request, auth
import json, threading

error_st_list = []
lost_st_list = []


def get_failed_stations(op_name, op_uuid, st_name, st_uuid, date, token, lock):
    with open("JSON Requests/notification.json") as good_noti:
        good_noti = json.load(good_noti)
    with open("JSON Requests/notification.json") as bad_noti:
        bad_noti = json.load(bad_noti)
    good_noti["variables"]["filters"]["creationDateLte"] = date + "T23:59:59+00:00"
    good_noti["variables"]["filters"]["creationDateGte"] = date + "T00:00:00+00:00"
    bad_noti["variables"]["filters"]["creationDateLte"] = date + "T23:59:59+00:00"
    bad_noti["variables"]["filters"]["creationDateGte"] = date + "T00:00:00+00:00"
    good_noti["variables"]["filters"].update({"and":
        [
            {"jdataUltimateFilter": {
                "containmentPath": "'station' -> 'uuid'",
                "containmentValue": "[\"" + st_uuid + "\"]"}},
            {"jdataUltimateFilter": {
                "containmentPath": "'operator' -> 'uuid'",
                "containmentValue": "[\"" + op_uuid + "\"]"}}]})
    bad_noti["variables"]["filters"].update({"and": [{"or": [{"jdataUltimateFilter": {
        "containmentPath": "'station' -> 'code'", "containmentValue": "[\"" + st_name + "\"]"}},
        {"jdataUltimateFilter": {
            "containmentPath": "'station' -> 'uuid'", "containmentValue": "[\"" + st_uuid + "\"]"}}],
        "jdataUltimateFilter": {"containmentPath": "'operator' -> 'uuid'",
                                "containmentValue": "[\"" + op_uuid + "\"]"}}]})
    good_noti["variables"]["filters"].update({"messageIlike": "кластер_snx2snx на"})

    bad_noti["variables"]["filters"]["priority"] = ["IMPORTANT", "CRITICAL"]
    good_noti["variables"]["filters"]["priority"] = ["REGULAR"]

    good_resp = request(good_noti, token)

    if good_resp["data"]["notifications"]["totalCount"] == 0:
        bad_resp = request(bad_noti, token)

        if bad_resp["data"]["notifications"]["totalCount"] != 0:

            lock.acquire()
            error_st_list.append(st_name)
            lock.release()

        else:
            lock.acquire()
            lost_st_list.append(st_name)
            lock.release()


def start_parse(name, all_st, date):
    with open("Data/operators_data.json") as oper_data:
        operators_data = json.load(oper_data)

    failed_st = []
    lost_st = []
    max_threads = 4
    login = "poshivailo_au"
    password = "a0587448"

    # Получение токена для входа
    token = auth(login, password)


    threads = []
    processed_op = []
    lock = threading.Lock()
    i = 0
    while True:
        for index, thread in enumerate(threads):
            if not thread.is_alive():
                threads.remove(thread)
                i += 1

        if len(threads) < max_threads:
            for el in all_st:
                if len(threads) == max_threads:
                    break

                if el[0] not in processed_op:
                    thread = threading.Thread(target=get_failed_stations, args=(
                    name, operators_data[name]["uuid"], el[0], el[1], date, token, lock),
                                              name="Thread_" + el[0])

                    threads.append(thread)
                    thread.start()

                    processed_op.append(el[0])
        if len(threads) == 0:
            break

    with open("Data/errors_stations.json", "w") as er_st:
        json.dump(error_st_list, er_st, indent=4, ensure_ascii=False)

    with open("Data/lost_stations.json", "w") as l_st:
        json.dump(lost_st_list, l_st, indent=4, ensure_ascii=False)
    noti_st = {'er_st': len(error_st_list), 'lost_st': len(lost_st_list)}

    return noti_st


