import requests

session = requests.Session()

# 登陆拿到 Token
print(session.post('http://192.168.1.71:8000/login', json={
    'username': 'test',
    'password': 'test',
    'eauth': 'pam',
}))

# 执行一条测试命令
resp = session.post('http://192.168.1.71:8000', json=[{
    'client': 'local',
    'tgt': 'HX*',
    'fun': 'test.ping',
}])

print(resp.json())

# 登出
print(session.post('http://192.168.1.71:8000/logout'))
