import json
import os

import requests
from flask import Flask, render_template, redirect, url_for, flash, g
from flask_bootstrap import Bootstrap
from flask_login import login_required
from flask_moment import Moment
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Optional

app = Flask(__name__)
app.config.from_pyfile('config.cfg', silent=True)
bootstrap = Bootstrap(app)
moment = Moment(app)
CSRFProtect(app)
Token = requests.Session()
Token2 = requests.Session()

from views.cmdb import cmdb
from views.saltstack import saltstack
from views.login import login
from views.login import logout
app.register_blueprint(cmdb)
app.register_blueprint(saltstack)
app.register_blueprint(login)
app.register_blueprint(logout)

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


class FileForm(FlaskForm):
    file = FileField('文件名', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('上传')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500


import schema


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = ModulesForm()
    if form.validate_on_submit():
        flash('执行完成!')
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
        schema.add_modules_history(tgt, fun, str(arg), str(kwarg))
        jid = Token.post(app.config.get('SALT_API') + '/minions/', json={
            'tgt': tgt,
            'fun': fun,
            'arg': arg,
            'kwarg': kwarg,
        }).json()['return'][0]['jid']
        return redirect(url_for('jobs', jid=jid))
    data = Token.get(app.config.get('SALT_API') + '/').json()
    minions = Token.get(app.config.get('SALT_API') + '/keys').json()
    return render_template('index.html', Data=data, Minions=json.dumps(minions['return']['minions']), form=form)


@app.route('/upload/', methods=['GET', 'POST'])
@login_required
def upload():
    form = FileForm()
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        form.file.data.save(os.path.join(
            app.root_path, 'uploadfile', filename
        ))
    return render_template('upload.html', form=form)


@app.route('/user')
def show_user():
    cur = g.sqlite_db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_user.html', entries=entries)



