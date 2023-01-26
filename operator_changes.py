import requests
import time


def changes(name):
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
    request_operator = {
        "query": 'query operatorsArchive($filters: OperatorsFilter){operators(filters: $filters){edges{node{shortName source{uuid}}}}}',
        'variables': {
            'filters': {
                "shortNameIlike": name
            }
        }
    }
    if token is not None:
        uuid = requests.post('https://fsgs.cgkipd.ru/federation/graphql', headers={'Authorization': token},
                             json=request_operator).json()
    else:
        exit()

    uuid = uuid['data']['operators']['edges'][0]['node']['source']['uuid']
    request_source_change = {
        "query": 'query operatorsArchive($filters: SourceArchiveFilter){sourcesArchive(filters: $filters){edges{node{action available bernesePathUuid connectionType description encoding filename host jdata login mask password port required state type timestamp modifiedUser{login name}}}}}',
        'variables': {
            'filters': {
                "uuid": uuid
            }
        }
    }

    response = requests.post('https://fsgs.cgkipd.ru/federation/graphql', headers={'Authorization': token},
                             json=request_source_change).json()
    response = response['data']['sourcesArchive']['edges']

    change_list = []

    for index, nodes in enumerate(response):

        next_index = index + 1
        node = {}
        if next_index != len(response):

            i = 0
            if response[index]['node']['available'] != response[next_index]['node']['available']:
                i += 1
                node['available'] = str(response[index]['node']['available']) + ' to ' + str(
                    response[next_index]['node']['available'])

            if response[index]['node']['bernesePathUuid'] != response[next_index]['node']['bernesePathUuid']:
                i += 1
                node['bernesePathUuid'] = response[index]['node']['bernesePathUuid'] + ' to ' + \
                                          response[next_index]['node']['bernesePathUuid']

            if response[index]['node']['connectionType'] != response[next_index]['node']['connectionType']:
                i += 1
                node['connectionType'] = response[index]['node']['connectionType'] + ' to ' + \
                                         response[next_index]['node']['connectionType']

            if response[index]['node']['description'] != response[next_index]['node']['description']:
                i += 1
                node['description'] = response[index]['node']['description'] + ' to ' + response[next_index]['node'][
                    'description']

            if response[index]['node']['encoding'] != response[next_index]['node']['encoding']:
                i += 1
                node['encoding'] = response[index]['node']['encoding'] + ' to ' + response[next_index]['node'][
                    'encoding']

            if response[index]['node']['filename'] != response[next_index]['node']['filename']:
                i += 1
                node['filename'] = response[index]['node']['filename'] + ' to ' + response[next_index]['node'][
                    'filename']

            if response[index]['node']['host'] != response[next_index]['node']['host']:
                i += 1
                node['host'] = response[index]['node']['host'] + ' to ' + response[next_index]['node']['host']

            if response[index]['node']['jdata'] != response[next_index]['node']['jdata']:
                i += 1
                node['jdata'] = response[index]['node']['jdata'] + ' to ' + response[next_index]['node']['jdata']

            if response[index]['node']['login'] != response[next_index]['node']['login']:
                i += 1
                node['login'] = response[index]['node']['login'] + ' to ' + response[next_index]['node']['login']

            if response[index]['node']['mask'] != response[next_index]['node']['mask']:
                i += 1
                node['mask'] = response[index]['node']['mask'] + ' to ' + response[next_index]['node']['mask']

            if response[index]['node']['password'] != response[next_index]['node']['password']:
                i += 1
                node['password'] = response[index]['node']['password'] + ' to ' + response[next_index]['node'][
                    'password']

            if response[index]['node']['port'] != response[next_index]['node']['port']:
                i += 1
                node['port'] = response[index]['node']['port'] + ' to ' + response[next_index]['node']['port']

            if response[index]['node']['required'] != response[next_index]['node']['required']:
                i += 1
                node['required'] = response[index]['node']['required'] + ' to ' + response[next_index]['node'][
                    'required']

            if response[index]['node']['state'] != response[next_index]['node']['state']:
                i += 1
                node['state'] = str(response[index]['node']['state']) + ' to ' + str(
                    response[next_index]['node']['state'])

            if response[index]['node']['type'] != response[next_index]['node']['type']:
                i += 1
                node['type'] = response[index]['node']['type'] + ' to ' + response[next_index]['node']['type']

            if response[index]['node']['modifiedUser'] is not None and response[next_index]['node'][
                'modifiedUser'] is not None and response[index]['node']['modifiedUser']['name'] != \
                    response[next_index]['node']['modifiedUser']['name']:
                i += 1
                node['type'] = response[index]['node']['modifiedUser']['name'] + ' to ' + \
                               response[next_index]['node']['modifiedUser']['name']

            if i != 0:
                node['timestamp'] = response[next_index]['node']['timestamp']
                if response[next_index]['node']['modifiedUser'] is not None:
                    node['modifiedUser'] = response[next_index]['node']['modifiedUser']['name']
                else:
                    node['modifiedUser'] = 'Unknown'
                change_list.append(node)

    return change_list
