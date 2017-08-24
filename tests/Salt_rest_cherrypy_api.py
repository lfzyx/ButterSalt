import requests
from config import config

url = config['test'].SALT_API
username = config['test'].SALT_USERNAME
password = config['test'].SALT_PASSWORD

session = requests.Session()

# /
print(session.get(url + '/').json())

# /LOGIN
print(session.get(url + '/login').json())

print(session.post(url + '/login', json={
    'username': username,
    'password': password,
    'eauth': 'pam',
}).json())

print(session.post(url + '/hook/').json())

# /MINIONS
print(session.get(url + '/minions/').json())


# /JOBS
print(session.get(url + '/jobs/').json())

# /KEYS
print(session.get(url + '/keys/').json())

print(session.post(url, json={
  "client": "runner",
  "fun": "manage.up"
}).json())


# /LOGOUT
print(session.post(url + '/logout').json())