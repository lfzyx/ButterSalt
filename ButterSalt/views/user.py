from flask import Blueprint, render_template, session, flash, redirect, request, url_for, g
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired
from flask_login import LoginManager, login_user, logout_user, UserMixin, login_required
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from ButterSalt import app
import os

login_manager = LoginManager()
login_manager.login_view = "user.login"
login_manager.init_app(app)


class Avatar(FlaskForm):
    file = FileField('文件名', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('上传')


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

user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username == password:
            me = User(username)
            login_user(me)
            session['logins'] = True
            session['username'] = username
            flash('Logged in successfully.')
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('user/login.html', form=form)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    session['logins'] = False
    return redirect(url_for('index'))


@user.route('/avatar/', methods=['GET', 'POST'])
@login_required
def avatar():
    form = Avatar()
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        form.file.data.save(os.path.join(
            app.root_path, 'uploadfile', filename
        ))
    return render_template('upload.html', form=form)



