import requests
import time
from urllib3.exceptions import ProtocolError


def stat(username: str = 'anonymous', password: str = 'anonymous') -> list:
    """
    Проверка работы сервисов АПК ФСГС
    :param username: имя пользователя
    :param password: пароль пользователя
    :return: Состоянии ФСГС
    """
    status = []

    url = "https://fsgs.cgkipd.ru/auth/login"
    data = {
        "username": username,
        "password": password
    }

    success = False
    i = 0
    while not success: # Проверка работы авторизации
        try:
            req = requests.post(url=url, json=data, timeout=2)
            if req.status_code != 200:
                break
            success = True

        except (OSError, ProtocolError, requests.exceptions.ConnectionError) as er:
            if i > 5:
                print(er)
                break
            i += 1

            time.sleep(10)
            continue

    state = False
    i = 0

    while not state: # Проверка работы федерации
        try:
            resp = requests.post(url='https://fsgs.cgkipd.ru/federation/graphql', json={"operationName": "Operators", "query": "query Operators($filters: OperatorsFilter){operators(filters: $filters){edges{node{fullName}}}}", "variables": {"fileters": {"shortName": "EFT"}}}, timeout=2).json()
            if 'errors' not in resp:
                state = True
            else:
                raise ResourceWarning
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout, ResourceWarning) as er:
            if i > 5:
                print(er)
                break
            i += 1

            time.sleep(1)
            continue

    if not state and not success:
        status.append('Федерация не отвечает')
        status.append('Авторизация не работает')
    elif not state:
        status.append('Федерация не отвечает')
    elif not success:
        status.append('Авторизация не работает')


    return status
