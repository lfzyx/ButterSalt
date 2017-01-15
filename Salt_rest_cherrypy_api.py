import requests

session = requests.Session()

# 登陆拿到 Token
print(session.post('http://192.168.1.71:8000/login', json={
    'username': 'test',
    'password': 'test',
    'eauth': 'pam',
}).json())

# 执行测试命令
print(session.post('http://192.168.1.71:8000', json=[{
    'client': 'local',
    'tgt': 'HX*',
    'fun': 'test.ping',
}]).json())

# minions 接口
print(session.get('http://192.168.1.71:8000/minions/HXtest3').json())

print(session.get('http://192.168.1.71:8000/jobs/20170115181824429759').json())

# 登出
print(session.post('http://192.168.1.71:8000/logout').json())