import requests

url = 'http://192.168.1.71:8000'

session = requests.Session()

# /
print(session.get(url + '/').json())

# /LOGIN
print(session.get(url + '/login').json())

print(session.post(url + '/login', json={
    'username': 'test',
    'password': 'test',
    'eauth': 'pam',
}).json())

# /MINIONS
print(session.get(url + '/minions/').json())

print(session.post('http://192.168.1.71:8000/minions', json={
    'tgt': ['HXtest2', 'HXtest3'],
    'fun': 'test.ping',
    'expr_form': 'list',
}).json())

# /JOBS
print(session.get(url + '/jobs/').json())

# /KEYS
print(session.get(url + '/keys/').json())

print(session.post(url, json={
  "client": "runner",
  "fun": "manage.up"
}).json())


# /LOGOUT
print(session.post('http://192.168.1.71:8000/logout').json())