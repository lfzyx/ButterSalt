from flask import Flask, render_template, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_login import LoginManager
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
import requests
import os


url = 'http://192.168.1.71:8000'

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
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
def page_not_found(a):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(a):
    return render_template('500.html'), 500


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        data = Token.post(url + '/login/', json={
            'username': username,
            'password': password,
            'eauth': 'pam',
        }).json()
        session['cookies'] = Token.cookies.items()
        if session.get('cookies') == Token.cookies.items():
            logins = True
        else:
            logins = False
        return render_template('index.html', Data=data, logins=logins)
    data = Token.get(url + '/login').json()
    if session.get('cookies') == Token.cookies.items():
        logins = True
    else:
        logins = False
    return render_template('login.html', Data=data, form=form, logins=logins)


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    data = Token.post(url + '/logout').json()
    if session.get('cookies') == Token.cookies.items():
        logins = True
    else:
        logins = False
    return render_template('index.html', Data=data, logins=logins)


@app.route('/')
def index():
    data = Token.get(url + '/').json()
    if session.get('cookies') == Token.cookies.items():
        logins = True
    else:
        logins = False
    return render_template('index.html', Data=data, logins=logins)


@app.route('/minions/', methods=['GET', 'POST'])
@app.route('/minions/<mid>')
def minions(mid=None):
    form = ModulesForm()
    if mid:
        data = Token.get(url + '/minions/%s' % mid).json()
        return render_template('minion.html', Data=data)
    if form.validate_on_submit():
        flash('执行完成!')
        target = form.target.data
        modules = form.modules.data
        jid = Token.post(url + '/minions/', json={
            'tgt': target,
            'fun': modules,
        }).json()['return'][0]['jid']
        return redirect(url_for('jobs', jid=jid))
    data = Token.get(url + '/minions').json()
    if session.get('cookies') == Token.cookies.items():
        logins = True
    else:
        logins = False
    return render_template('minions.html', Data=data, form=form, logins=logins)


@app.route('/jobs/')
@app.route('/jobs/<jid>')
def jobs(jid=None):
    if jid:
        data = Token.get(url + '/jobs/%s' % jid).json()
        if session.get('cookies') == Token.cookies.items():
            logins = True
        else:
            logins = False
        return render_template('job.html', Data=data, logins=logins)
    data = Token.get(url + '/jobs').json()
    if session.get('cookies') == Token.cookies.items():
        logins = True
    else:
        logins = False
    return render_template('jobs.html', Data=data, logins=logins)


@app.route('/keys/')
@app.route('/keys/<mid>')
def keys(mid=None):
    if mid:
        data = Token.get(url + '/keys/%s' % mid).json()
        if session.get('cookies') == Token.cookies.items():
            logins = True
        else:
            logins = False
        return render_template('key.html', Data=data, logins=logins)
    data = Token.get(url + '/keys').json()
    if session.get('cookies') == Token.cookies.items():
        logins = True
    else:
        logins = False
    return render_template('keys.html', Data=data, logins=logins)


@app.route('/stats/')
def stats():
    data = Token.get(url + '/stats').json()
    if session.get('cookies') == Token.cookies.items():
        logins = True
    else:
        logins = False
    return render_template('stats.html', Data=data, logins=logins)


@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    form = FileForm()
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        form.file.data.save(os.path.join(
            app.root_path, 'uploadfile', filename
        ))
    return render_template('upload.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)

