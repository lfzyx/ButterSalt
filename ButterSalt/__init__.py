import json

import requests
from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_login import login_required
from flask_moment import Moment
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Optional
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')
bootstrap = Bootstrap(app)
moment = Moment(app)
CSRFProtect(app)
Token = requests.Session()
Token2 = requests.Session()
db = SQLAlchemy(app)

from .models import MoudleExecuteHistory

from ButterSalt.views.cmdb import cmdb
from ButterSalt.views.saltstack import saltstack
from ButterSalt.views.user import user
from ButterSalt.views.deployment import deployment
app.register_blueprint(cmdb)
app.register_blueprint(saltstack)
app.register_blueprint(user)
app.register_blueprint(deployment)

Token.post(app.config.get('SALT_API') + '/login', json={
    'username': app.config.get('USERNAME'),
    'password': app.config.get('PASSWORD'),
    'eauth': 'pam',
})

Token2.post(app.config.get('SALT_API') + '/login', json={
    'username': app.config.get('USERNAME'),
    'password': app.config.get('PASSWORD'),
    'eauth': 'pam',
})


class ModulesForm(FlaskForm):
    tgt = StringField('目标', validators=[InputRequired('目标是必须的')])
    fun = StringField('模块', validators=[InputRequired('模块是必须的')])
    arg = StringField('参数', validators=[Optional()])
    keyarg = StringField('键', validators=[Optional()])
    wordarg = StringField('值', validators=[Optional()])
    submit = SubmitField('提交')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500


from . import models


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = ModulesForm()
    if form.validate_on_submit():
        tgt = form.tgt.data
        fun = form.fun.data
        arg = form.arg.data.split()
        keyarg = form.keyarg.data
        wordarg = form.wordarg.data
        if wordarg == 'True':
            wordarg = True
        elif wordarg == 'False':
            wordarg = False
        if keyarg:
            kwarg = {keyarg: wordarg}
        else:
            kwarg = {}
        jid = Token.post(app.config.get('SALT_API') + '/minions/', json={
            'tgt': tgt,
            'fun': fun,
            'arg': arg,
            'kwarg': kwarg,
        }).json()['return'][0]['jid']
        flash('执行完成')
        execute = MoudleExecuteHistory(tgt, fun, str(arg), str(kwarg), 1)
        db.session.add(execute)
        db.session.commit()
        return redirect(url_for('saltstack.jobs', jid=jid))
    data = Token.get(app.config.get('SALT_API') + '/').json()
    minions = Token.get(app.config.get('SALT_API') + '/keys').json()
    return render_template('home/index.html', Data=data, Minions=json.dumps(minions['return']['minions']), form=form)
