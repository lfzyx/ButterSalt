import requests
import jenkins
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from ButterSalt.saltapi import SaltApi


app = Flask(__name__)
app.config.from_object('config')
bootstrap = Bootstrap(app)
moment = Moment(app)
CSRFProtect(app)
Token = requests.Session()
db = SQLAlchemy(app)


salt = SaltApi(
    app.config.get('SALT_API'),
    app.config.get('USERNAME'),
    app.config.get('PASSWORD')
)


J_server = jenkins.Jenkins(
    app.config.get('JENKINS_API'),
    username=app.config.get('J_USERNAME'),
    password=app.config.get('J_PASSWORD')
)

Token.post(app.config.get('SALT_API') + '/login', json={
    'username': app.config.get('USERNAME'),
    'password': app.config.get('PASSWORD'),
    'eauth': 'pam',
})


from ButterSalt.views.cmdb import cmdb
from ButterSalt.views.saltstack import saltstack
from ButterSalt.views.user import user
from ButterSalt.views.deployment import deployment
from ButterSalt.views.home import home
app.register_blueprint(cmdb)
app.register_blueprint(saltstack)
app.register_blueprint(user)
app.register_blueprint(deployment)
app.register_blueprint(home)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500
