import os


class Config:
    SALT_API = os.environ.get('SALT_API')
    USERNAME = os.environ.get('SALT_USERNAME')
    PASSWORD = os.environ.get('SALT_PASSWORD')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_USE_SSL = True
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SUBJECT_PREFIX = '[ButterSalt] '
    MAIL_SENDER = os.environ.get('MAIL_SENDER')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'default': ProductionConfig
}
