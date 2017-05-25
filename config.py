import os
SALT_API = 'http://192.168.1.71:8000'
USERNAME = 'test'
PASSWORD = 'test'
SECRET_KEY = b'\xba\x03\xc7\xdd\xa3\x14\x8e\xc9\x07"\x82\xb3\x0fK\xe8u\x19k\xcd\xc3\x00\x1f\xf0a'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ButterSalt:ButterSalt@192.168.1.73/ButterSalt'
SQLALCHEMY_TRACK_MODIFICATIONS = True
MAIL_SERVER = 'smtp.163.com'
MAIL_USE_SSL = True
MAIL_PORT = '465'
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_SUBJECT_PREFIX = '[ButterSalt] '
MAIL_SENDER = os.environ.get('MAIL_SENDER')
