import requests
import time


def check(name, date):
    while True:
        try:
            resp = requests.post("https://fsgs.cgkipd.ru/auth/login",
                                 json={"username": "anonymous", "password": "anonymous"}).json()
            token = "Bearer " + resp["data"]["access_token"]
            break
        except KeyError:
            print("Данные не верны!")
            exit()
        except:
            print('Ups')
            time.sleep(2)
            token = None
            continue


