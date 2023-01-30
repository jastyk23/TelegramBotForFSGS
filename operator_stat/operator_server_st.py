import ftplib, json, time, re

import get_op_data as god

with open("JSON Requests/get_stations.json") as st_req:
    station_request = json.load(st_req)




# Получение станций по маске
def get_st(operator_name, date, token):
    with open('Data/operators_data.json') as file:
        operator_data = json.load(file)

    op_list = []
    station_request["variables"]["filters"]["operatorUuidIn"] = operator_data[operator_name]["uuid"]
    station_list = god.request(station_request, token)
    station_list = station_list["data"]["stations"]["edges"]
    pattern = {
        "YYYY": date.strftime("%Y"),
        "YY": date.strftime("%y"),
        "MM": date.strftime("%m"),
        "DD": date.strftime("%d"),
        "day_of_the_year_z_padded": date.strftime("%j"),
        "short_month": date.strftime("%m")
    }
    path = operator_data[operator_name]["filename"]
    path = path.format(**pattern)
    mask = operator_data[operator_name]["mask"]
    mask = mask.format(**pattern)
    try:
        connect = ftplib.FTP(host=operator_data[operator_name]["host"], user=operator_data[operator_name]["login"],
                             passwd=operator_data[operator_name]["password"], timeout=20)
    except (ftplib.error_perm, TimeoutError, ConnectionRefusedError):

        op_list.append("can't connect")

        return
    except ConnectionResetError:
        print(operator_name)
        return
    for station_node in station_list:
        station_path_up = path
        station_path_lw = path

        if "stations_name" in path:
            station_path_up = path.format(**{"stations_name": station_node["node"]["name"]})
            station_path_lw = path.format(**{"stations_name": station_node["node"]["name"].lower()})
        station_mask = mask.format(**{"stations_name": station_node["node"]["name"]})
        try:
            connect.cwd(station_path_up)
        except ftplib.error_perm:
            try:
                connect.cwd(station_path_lw)
            except ftplib.error_perm:
                continue

        try:
            files_list = connect.nlst()
            for elements in files_list:
                station_up = re.match(station_mask, elements)
                station_lw = re.match(station_mask.lower(), elements)
                if station_up is not None:
                    op_list.append(station_up.group(0)[:4])
                    break
                elif station_lw is not None:
                    op_list.append(station_lw.group(0)[:4].upper())
                    break
        except ftplib.error_temp:
            files_list = connect.mlsd()

            for elements in files_list:
                station_up = re.match(station_mask, elements[0])
                station_lw = re.match(station_mask.lower(), elements[0])
                if station_up is not None:

                    op_list.append(station_up.group(0)[:4])
                    break
                elif station_lw is not None:
                    op_list.append(station_lw.group(0)[:4].upper())
                    break
        except TimeoutError:
            print("Неизвестная ошибка ", operator_name)
    connect.close()
    op_list = list(set(op_list))
    return len(op_list) if len(op_list) > 1 else op_list[0]
