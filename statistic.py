import requests
import json


url = 'https://preprod.fsgs2.sitronics-kt.dev/federation/graphql'


source = {
    "operationName": "sources",
    "query": "query sources{operators{edges{node{shortName source{host login password}}}}}"
}



a = "anonymous"
resp = requests.post('https://preprod.fsgs2.sitronics-kt.dev/auth/login', json={'password': '12345678', 'username': 'user'}).json()
print(resp)
