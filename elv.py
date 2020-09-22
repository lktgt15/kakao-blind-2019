import requests

url = 'http://localhost:8000'

def start(user_key, problem_id, number_of_elevators):
    return requests.post(url + '/start/' + user_key + '/' + str(problem_id) + '/' + str(number_of_elevators)).json()

def allelvs(Dict):
    ret = []
    for elv in Dict['elevators']:
        ret.append(elv)
    return ret


def elvStat(i, elvs):
    return elvs[i]

def onCall(token):
    return requests.get(url + '/oncalls', headers={'X-Auth-Token': token}).json()

def Action(token,cmds):
    requests.post(url + '/action', headers={'X-Auth-Token': token, 'Content-Type': 'application/json'}, json={'commands':cmds}).json()

