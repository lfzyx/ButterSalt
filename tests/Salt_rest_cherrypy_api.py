import requests

session = requests.Session()

# 登陆拿到 Token
print(session.post('http://192.168.1.71:8000/login', json={
    'username': 'test',
    'password': 'test',
    'eauth': 'pam',
}).json())

print(session.post('http://192.168.1.71:8000/minions', json={
    'tgt': 'HX*',
    'fun': 'test.ping',
}).json())


# 登出
print(session.post('http://192.168.1.71:8000/logout').json())