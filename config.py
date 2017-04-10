import os

DEBUG = True
SALT_API = 'http://192.168.1.71:8000'
USERNAME = 'test'
PASSWORD = 'test'
SECRET_KEY = os.urandom(24)
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ButterSalt:ButterSalt@192.168.1.73/ButterSalt'
SQLALCHEMY_TRACK_MODIFICATIONS = True
JENKINS_API = 'http://192.168.1.72:8080'
J_USERNAME = 'lfzyx'
J_PASSWORD = 'ac2365e7cd8ec7cb994b4547ead537da'

