import os

DEBUG = True
SALT_API = 'http://192.168.1.71:8000'
USERNAME = 'test'
PASSWORD = 'test'
SECRET_KEY = os.urandom(24)
SQLALCHEMY_DATABASE_URI = 'sqlite:///../database/schema.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
