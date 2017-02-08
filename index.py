import os

import requests
from flask import Flask, render_template, redirect, url_for, flash, session, g
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_moment import Moment
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

import schema

app = Flask(__name__)
app.config.from_pyfile('config.cfg', silent=True)
bootstrap = Bootstrap(app)
moment = Moment(app)
Token = requests.Session()
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


class ModulesForm(FlaskForm):
    target = StringField('目标', validators=[DataRequired()])
    modules = StringField('执行模块', validators=[DataRequired()])
    submit = SubmitField('提交')


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
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


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        data = Token.post(app.config.get('SALT_API') + '/login/', json={
            'username': username,
            'password': password,
            'eauth': 'pam',
        }).json()
        session['cookies'] = Token.cookies.items()
        if session.get('cookies') == Token.cookies.items():
            session['logins'] = True
            flash('You were logged in')
        else:
            session['logins'] = False
        return render_template('login.html', Data=data, form=form)
    data = Token.get(app.config.get('SALT_API') + '/login').json()
    return render_template('login.html', Data=data, form=form)


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    data = Token.post(app.config.get('SALT_API') + '/logout').json()
    if session.get('cookies') == Token.cookies.items():
        session['logins'] = True
    else:
        session['logins'] = False
        flash('You were logged out')
    return render_template('index.html', Data=data)


@app.route('/')
def index():
    data = Token.get(app.config.get('SALT_API') + '/').json()
    return render_template('index.html', Data=data)


@app.route('/minions/', methods=['GET', 'POST'])
@app.route('/minions/<mid>')
def minions(mid=None):
    form = ModulesForm()
    if mid:
        data = Token.get(app.config.get('SALT_API') + '/minions/%s' % mid).json()
        return render_template('minion.html', Data=data['return'][0])
    if form.validate_on_submit():
        flash('执行完成!')
        target = form.target.data
        modules = form.modules.data
        schema.add_modules_history(target, modules)
        jid = Token.post(app.config.get('SALT_API') + '/minions/', json={
            'tgt': target,
            'fun': modules,
        }).json()['return'][0]['jid']
        return redirect(url_for('jobs', jid=jid))
    data = Token.get(url + '/minions').json()
    return render_template('minions.html', Data=data['return'][0], form=form)


@app.route('/jobs/')
@app.route('/jobs/<jid>')
def jobs(jid=None):
    if jid:
        data = Token.get(app.config.get('SALT_API') + '/jobs/%s' % jid).json()
        return render_template('job.html', Data=data['info'][0])
    data = Token.get(app.config.get('SALTAPI') + '/jobs').json()
    return render_template('jobs.html', Data=data['return'][0])


@app.route('/keys/')
@app.route('/keys/<mid>')
def keys(mid=None):
    if mid:
        data = Token.get(app.config.get('SALT_API') + '/keys/%s' % mid).json()
        return render_template('key.html', Data=data['return']['minions'])
    data = Token.get(app.config.get('SALT_API') + '/keys').json()
    return render_template('keys.html', Data=data['return'])


@app.route('/stats/')
def stats():
    data = Token.get(app.config.get('SALT_API') + '/stats').json()
    return render_template('stats.html', Data=data)


@app.route('/upload/', methods=['GET', 'POST'])
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


if __name__ == "__main__":
    app.run()

