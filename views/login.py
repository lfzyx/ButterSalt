from flask import Blueprint, render_template, session, flash, redirect, request, url_for, g
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired
from flask_login import LoginManager, login_user, logout_user, UserMixin, login_required
from index import app

login_manager = LoginManager()
login_manager.login_view = "login.index"
login_manager.init_app(app)


# 登陆相关函数和类
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[InputRequired('用户名是必须的')])
    password = PasswordField('密码', validators=[InputRequired('密码是必须的')])
    submit = SubmitField('提交')

login = Blueprint('login', __name__, url_prefix='/login')
logout = Blueprint('logout', __name__, url_prefix='/logout')


@login.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username == password:
            user = User(username)
            login_user(user)
            session['logins'] = True
            session['username'] = username
            flash('Logged in successfully.')
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html', form=form)


@logout.route('/')
@login_required
def index():
    logout_user()
    session['logins'] = False
    return redirect(url_for('index'))



