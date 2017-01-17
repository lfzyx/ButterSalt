from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
import requests


url = 'http://192.168.1.71:8000'


session = requests.Session()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'uiJaX!N>ZlHq5d)XjQ|EJb9/Fr'
bootstrap = Bootstrap(app)
moment = Moment(app)


class ModulesForm(FlaskForm):
    target = StringField('目标', validators=[DataRequired()])
    modules = StringField('执行模块', validators=[DataRequired()])
    submit = SubmitField('提交')


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('提交')

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
        data = session.post(url + '/login/', json={
            'username': username,
            'password': password,
            'eauth': 'pam',
        }).json()
        return render_template('index.html', Data=data)
    data = session.get(url + '/login').json()
    return render_template('login.html', Data=data, form=form)


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    data = session.post(url + '/logout').json()
    return render_template('index.html', Data=data)


@app.route('/')
def index():
    data = session.get(url + '/').json()
    return render_template('index.html', Data=data)


@app.route('/minions/', methods=['GET', 'POST'])
@app.route('/minions/<mid>')
def minions(mid=None):
    form = ModulesForm()
    if mid:
        data = session.get(url + '/minions/%s' % mid).json()
        return render_template('minion.html', Data=data)
    if form.validate_on_submit():
        flash('执行完成!')
        target = form.target.data
        modules = form.modules.data
        jid = session.post(url + '/minions/', json={
            'tgt': target,
            'fun': modules,
        }).json()['return'][0]['jid']
        return redirect(url_for('job', jid=jid))
    data = session.get(url + '/minions').json()
    return render_template('minions.html', Data=data, form=form)


@app.route('/jobs/')
@app.route('/jobs/<jid>')
def job(jid=None):
    if jid:
        data = session.get(url + '/jobs/%s' % jid).json()
        return render_template('job.html', Data=data)
    data = session.get(url + '/jobs').json()
    return render_template('jobs.html', Data=data)


@app.route('/keys/')
@app.route('/keys/<mid>')
def key(mid=None):
    if mid:
        data = session.get(url + '/keys/%s' % mid).json()
        return render_template('key.html', Data=data)
    data = session.get(url + '/keys').json()
    return render_template('keys.html', Data=data)


@app.route('/stats/')
def stats():
    data = session.get(url + '/stats').json()
    return render_template('stats.html', Data=data)


if __name__ == "__main__":
    app.run(debug=True)

