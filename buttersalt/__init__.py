import logging
from logging import FileHandler, Formatter
from flask import Flask, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from flask_babel import Babel
from buttersalt_saltapi import saltapi
from config import config


bootstrap = Bootstrap()
moment = Moment()
csrfprotect = CSRFProtect()
db = SQLAlchemy()
mail = Mail()
salt = saltapi.SaltApi()
babel = Babel()
login_manager = LoginManager()
login_manager.login_view = "user.login"
login_manager.session_protection = 'basic'


file_handler = FileHandler('ButterSalt.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)


@babel.localeselector
def get_locale():
    locale = request.accept_languages.best_match(['zh-cn', 'zh-tw', 'en'])
    if locale == 'zh-cn' or 'zh-tw':
        return 'zh'
    else:
        return 'en'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    salt.init_app(app)
    login_manager.init_app(app)
    csrfprotect.init_app(app)
    babel.init_app(app)

    app.logger.addHandler(file_handler)
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)

    from .views.home import home
    from .views.saltstack import saltstack
    from .views.user import user
    from .views.error import error
    app.register_blueprint(home)
    app.register_blueprint(saltstack)
    app.register_blueprint(user)
    app.register_blueprint(error)

    return app
