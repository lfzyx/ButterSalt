from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

session = requests.Session()

session.post('http://192.168.1.71:8000/login', json={
    'username': 'test',
    'password': 'test',
    'eauth': 'pam',
}).json()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'uiJaX!N>ZlHq5d)XjQ|EJb9/Fr'
bootstrap = Bootstrap(app)
moment = Moment(app)


class ModulesForm(FlaskForm):
    name = StringField('输入要执行的模块', validators=[DataRequired()])
    submit = SubmitField('提交')


@app.errorhandler(404)
def page_not_found(a):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(a):
    return render_template('500.html'), 500


@app.route('/')
def index():
    data = session.get('http://192.168.1.71:8000/').json()
    return render_template('index.html', Data=data)


@app.route('/minions/')
def minions():
    data = session.get('http://192.168.1.71:8000/minions').json()
    return render_template('index.html', Data=data)


@app.route('/minions/<mid>')
def minion(mid):
    data = session.get('http://192.168.1.71:8000/minions/%s' % mid).json()
    return render_template('index.html', Data=data)


@app.route('/jobs/')
def jobs():
    data = session.get('http://192.168.1.71:8000/jobs').json()
    return render_template('index.html', Data=data)


@app.route('/jobs/<jid>')
def job(jid):
    data = session.get('http://192.168.1.71:8000/jobs/%s' % jid).json()
    return render_template('index.html', Data=data)


@app.route('/keys/')
def keys():
    data = session.get('http://192.168.1.71:8000/keys').json()
    return render_template('index.html', Data=data)


@app.route('/keys/<mid>')
def key(mid):
    data = session.get('http://192.168.1.71:8000/keys/%s' % mid).json()
    return render_template('index.html', Data=data)


@app.route('/stats/')
def stats():
    data = session.get('http://192.168.1.71:8000/stats').json()
    return render_template('index.html', Data=data)


if __name__ == "__main__":
    app.run(debug=True)

