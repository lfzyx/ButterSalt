from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

session = requests.Session()

rp = session.post('http://192.168.1.71:8000/login', json={
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


@app.route('/', methods=['GET', 'POST'])
def index():
    form = ModulesForm()
    if form.validate_on_submit():
        flash('开始执行: '+form.name.data)
        return redirect(url_for('index'))

    jobs = session.get('http://192.168.1.71:8000/jobs/20170112144945138666').json()

    return render_template('index.html', form=form, Data=rp, jobs=jobs)


if __name__ == "__main__":
    app.run(debug=True)

