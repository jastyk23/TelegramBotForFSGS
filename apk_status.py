import requests
import time
from urllib3.exceptions import ProtocolError


def stat():
    status = []
    '''try:
        req = requests.get(url='https://fsgs.cgkipd.ru/', timeout=5)
    except requests.exceptions.Timeout:
        status.append('Фронт отлетел')'''

    url = "https://fsgs.cgkipd.ru/auth/login"
    data = {
        "username": "anonymous",
        "password": "anonymous"
    }

    success = False
    i = 0
    while not success:

        try:
            req = requests.post(url=url, json=data, timeout=2)
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

    while not state:
        try:
            resp = requests.post(url='https://fsgs.cgkipd.ru/federation/graphql', json={"operationName": "Operators", "query": "query Operators($filters: OperatorsFilter){operators(filters: $filters){edges{node{fullName}}}}", "variables": {"fileters": {"shortName": "EFT"}}}, timeout=2).json()
            if 'errors' not in resp:
                state = True
            else:
                raise ResourceWarning
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout, ResourceWarning) as er:
            if i > 10:
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
