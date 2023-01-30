import requests, json, time
from pathlib import Path

# Авторизация
def auth(login, passw):
    # Авторизация
    while True:
        try:
            resp = requests.post("https://fsgs.cgkipd.ru/auth/login", json={"password": passw, "username": login})
            resp = resp.json()
            return "Bearer " + resp["data"]["access_token"]
        except KeyError:
            print("Данные не верны!")
            exit()
        except:
            time.sleep(10)
            continue

# Запрос
def request(json_request, token):
    # Запросы
    while True:
        try:
            resp = requests.post("https://fsgs.cgkipd.ru/federation/graphql", headers={"Authorization": token},
                                 json=json_request)
            resp = resp.json()
            return resp
        except:
            time.sleep(10)
            continue



# Данные по операторам
def get_op_data(tok):
    with open("JSON Requests/get_operators_data.json") as file:
        req = json.load(file)
    resp = request(req, tok)
    operators_data = {}
    for node in resp["data"]["operators"]["edges"]:
        operators_data.update({
            node["node"]["shortName"]: {
                "name": node["node"]["fullName"],
                "uuid": node["node"]["uuid"],
                "host": node["node"]["source"]["host"],
                "login": node["node"]["source"]["login"],
                "password": node["node"]["source"]["password"],
                "filename": node["node"]["source"]["filename"],
                "mask": node["node"]["source"]["mask"]
            }
        })
    data_path = Path("Data")
    data_path.mkdir(parents=True, exist_ok=True)
    with open("Data/operators_data.json", "w") as op_data:
        json.dump(operators_data, op_data, indent=4, ensure_ascii=False)