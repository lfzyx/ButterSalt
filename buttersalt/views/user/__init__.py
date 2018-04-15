from flask import Blueprint, render_template, flash, redirect, request, url_for, current_app
from flask_login import login_user, logout_user, login_required, UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length, Regexp
from ... import login_manager
from flask_babel import lazy_gettext


class Me(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        if self.username == current_app.config['DASHBOARD_ADMIN'].split(':')[0]:
            self.id = 0
        else:
            self.id = 1


@login_manager.user_loader
def load_user(user_id):
    if user_id == '0':
        return Me(current_app.config['DASHBOARD_ADMIN'].split(':')[0],
                  current_app.config['DASHBOARD_ADMIN'].split(':')[1])
    else:
        return None


class LoginForm(FlaskForm):
    username = StringField(lazy_gettext('Username'),
                           validators=[InputRequired('Username required'), Length(1, 64),
                                       Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'Usernames must have only letters, numbers, dots or underscores')])
    password = PasswordField(lazy_gettext('Password'), validators=[InputRequired('Password required')])
    remember_me = BooleanField(lazy_gettext('Remember Me'))
    submit = SubmitField('Log In')


user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        me = Me(username, password)
        if me.username == current_app.config['DASHBOARD_ADMIN'].split(':')[0] and \
           me.password == current_app.config['DASHBOARD_ADMIN'].split(':')[1]:
            login_user(me, form.remember_me.data)
            flash(lazy_gettext('Logged in successfully.'))
            current_app.logger.info('A successful login attempt (%s)', username)
            return redirect(request.args.get('next') or url_for('home.index'))
        flash('Invalid usename or password.')
        current_app.logger.warning('A warning login attempt (%s)', username)
    return render_template('user/login.html', form=form)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('home.index'))
