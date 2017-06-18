from flask import Blueprint, render_template, session, flash, redirect, request, url_for
from flask_login import login_user, logout_user, UserMixin, login_required
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import InputRequired, Length, Email, Regexp, EqualTo
from werkzeug.utils import secure_filename
import os
from ButterSalt import models, db, login_manager


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
    username = StringField('用户名', validators=[InputRequired('用户名是必须的'), Length(1, 64),
                                              Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                     '用户名只能包含字母，数字，点或下划线')])
    password = PasswordField('密码', validators=[InputRequired('密码是必须的')])
    remember_me = BooleanField('保持登陆')
    submit = SubmitField('提交')


class SignupForm(FlaskForm):
    username = StringField('用户名', validators=[InputRequired('用户名是必须的'), Length(1, 64),
                                              Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                     '用户名只能包含字母，数字，点或下划线')])
    email = StringField('Email', validators=[InputRequired('Email是必须的'), Length(1, 64), Email()])
    password0 = PasswordField('密码', validators=[InputRequired('密码是必须的'),
                                               EqualTo('password1', message='密码必须相同.')])
    password1 = PasswordField('验证密码', validators=[InputRequired('验证密码是必须的')])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if models.Users.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if models.Users.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/login', methods=['GET', 'POST'])
def login():
    if not models.Users.query.all():
        return redirect(url_for('user.signup', next=request.args.get('next')))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        me = models.Users.query.filter_by(username=username).one_or_none()
        if me is not None and me.verify_password(password):
            login_user(User(me), form.remember_me.data)
            session['username'] = username
            flash('Logged in successfully.')
            return redirect(request.args.get('next') or url_for('home.index'))
        flash('Invalid usename or password.')
        # app.logger.warning('A warning login attempt (%s)', username)
    return render_template('user/login.html', form=form)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('home.index'))


@user.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        me = models.Users(email=form.email.data, username=form.username.data)
        me.password_hash(form.password0.data)
        db.session.add(me)
        db.session.commit()
        flash('Sign up Successfully!')
        return redirect(request.args.get('next') or url_for('home.index'))
    return render_template('user/signup.html', form=form)


@user.route('/avatar/', methods=['GET', 'POST'])
@login_required
def avatar():
    form = Avatar()
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        form.file.data.save(os.path.join(
            # app.root_path, 'uploadfile', filename
        ))
    return render_template('upload.html', form=form)
