import os

import requests
from flask import Flask, render_template, redirect, url_for, flash, session, g, request
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_user, logout_user, UserMixin, login_required
from flask_moment import Moment
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Optional

import schema

app = Flask(__name__)
app.config.from_pyfile('config.cfg', silent=True)
bootstrap = Bootstrap(app)
moment = Moment(app)
CSRFProtect(app)
Token = requests.Session()
Token2 = requests.Session()
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

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


# 登陆相关函数和类
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('提交')


class ModulesForm(FlaskForm):
    tgt = StringField('目标', validators=[DataRequired()])
    fun = StringField('执行模块', validators=[DataRequired()])
    arg = StringField('顺序参数', validators=[Optional()])
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


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username == password:
            user = User(username)
            login_user(user)
            session['logins'] = True
            flash('Logged in successfully.')
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    session['logins'] = False
    return redirect(url_for('index'))


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
        print(kwarg)
        schema.add_modules_history(tgt, fun, str(arg), str(kwarg))
        jid = Token.post(app.config.get('SALT_API') + '/minions/', json={
            'tgt': tgt,
            'fun': fun,
            'arg': arg,
            'kwarg': kwarg,
        }).json()['return'][0]['jid']
        return redirect(url_for('jobs', jid=jid))
    data = Token.get(app.config.get('SALT_API') + '/').json()
    return render_template('index.html', Data=data, form=form)


@app.route('/minions/')
@app.route('/minions/<mid>')
@login_required
def minions(mid=None):
    if mid:
        data = Token.get(app.config.get('SALT_API') + '/minions/%s' % mid).json()
        return render_template('minion.html', Data=data['return'][0])

    data = Token.get(app.config.get('SALT_API') + '/minions').json()
    return render_template('minions.html', Data=data['return'][0])


@app.route('/jobs/')
@app.route('/jobs/<jid>')
@login_required
def jobs(jid=None):
    if jid:
        data = Token.get(app.config.get('SALT_API') + '/jobs/%s' % jid).json()
        return render_template('job.html', Data=data['info'][0])
    data = Token.get(app.config.get('SALT_API') + '/jobs').json()
    return render_template('jobs.html', Data=data['return'][0])


@app.route('/keys/')
@app.route('/keys/<mid>')
@login_required
def keys(mid=None):
    if mid:
        data = Token.get(app.config.get('SALT_API') + '/keys/%s' % mid).json()
        return render_template('key.html', Data=data['return']['minions'])
    data = Token.get(app.config.get('SALT_API') + '/keys').json()
    return render_template('keys.html', Data=data['return'])


@app.route('/stats/')
@login_required
def stats():
    data = Token.get(app.config.get('SALT_API') + '/stats').json()
    return render_template('stats.html', Data=data)


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


if __name__ == "__main__":
    app.run()

