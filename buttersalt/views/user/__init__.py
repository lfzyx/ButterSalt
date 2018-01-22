from flask import Blueprint, render_template, flash, redirect, request, url_for, current_app
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import InputRequired, Length, Email, Regexp, EqualTo
from ... import models, db
from ...sendmail import send_email


class Avatar(FlaskForm):
    file = FileField('filename', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('upload')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired('Username required'), Length(1, 64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                   'Usernames must have only letters, numbers, dots or underscores')])
    password = PasswordField('Password', validators=[InputRequired('Password required')])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired('Username required'), Length(1, 64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                   'Usernames must have only letters, numbers, dots or underscores')])
    email = StringField('Email', validators=[InputRequired('Email required'), Length(1, 64), Email()])
    password0 = PasswordField('Password', validators=[InputRequired('Password required'),
                                                      EqualTo('password1', message='Passwords must match.')])
    password1 = PasswordField('Confirm password', validators=[InputRequired('Password required')])
    submit = SubmitField('Sign up')

    @staticmethod
    def validate_email(self, field):
        if models.User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    @staticmethod
    def validate_username(self, field):
        if models.User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[InputRequired('Password required')])
    password0 = PasswordField('New password', validators=[
        InputRequired('Password required'), EqualTo('password1', message='Passwords must match')])
    password1 = PasswordField('Confirm new password', validators=[InputRequired('Password required')])
    submit = SubmitField('Update Password')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired('Email required'), Length(1, 64), Email()])
    submit = SubmitField('Reset Password')


class PasswordResetForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired('Email required'), Length(1, 64), Email()])
    password0 = PasswordField('New Password', validators=[
        InputRequired('Password required'), EqualTo('password1', message='Passwords must match')])
    password1 = PasswordField('Confirm new password', validators=[InputRequired('Password required')])
    submit = SubmitField('Reset Password')

    @staticmethod
    def validate_email(self, field):
        if models.Users.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')


class ChangeEmailForm(FlaskForm):
    email = StringField('New Email', validators=[InputRequired('Email required'), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[InputRequired('Password required')])
    submit = SubmitField('Update Email Address')

    @staticmethod
    def validate_email(self, field):
        if models.Users.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


user = Blueprint('user', __name__, url_prefix='/user')


@user.before_app_request
def before_request():
    if current_user.is_authenticated \
                and not current_user.confirmed \
                and request.endpoint \
                and request.endpoint[:5] != 'user.' \
                and request.endpoint != 'static':
            return redirect(url_for('user.unconfirmed'))


@user.route('/login', methods=['GET', 'POST'])
def login():
    if not models.User.query.all():
        return redirect(url_for('user.signup', next=request.args.get('next')))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        me = models.User.query.filter_by(username=username).one_or_none()
        if me is not None and me.verify_password(password):
            login_user(me, form.remember_me.data)
            flash('Logged in successfully.')
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


@user.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        me = models.User(email=form.email.data, username=form.username.data, password=form.password0.data)
        db.session.add(me)
        db.session.commit()
        token = me.generate_confirmation_token()
        send_email(me.email, 'Confirm Your Account',
                   'mail/user/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(request.args.get('next') or url_for('home.index'))
    return render_template('user/signup.html', form=form)


@user.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('home.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('home.index'))


@user.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'mail/user/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('home.index'))


@user.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('home.index'))
    return render_template('user/unconfirmed.html')


@user.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password0.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('home.index'))
        else:
            flash('Invalid password.')
    return render_template("user/change_password.html", form=form)


@user.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('home.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        me = models.User.query.filter_by(email=form.email.data).first()
        if me:
            token = me.generate_reset_token()
            send_email(me.email, 'Reset Your Password',
                       'mail/user/reset_password',
                       user=me, token=token,
                       next=request.args.get('next'))
        flash('An email with instructions to reset your password has been '
              'sent to you.')
        return redirect(url_for('user.login'))
    return render_template('user/reset_password.html', form=form)


@user.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('home.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        me = models.User.query.filter_by(email=form.email.data).first()
        if me is None:
            return redirect(url_for('home.index'))
        if me.reset_password(token, form.password0.data):
            flash('Your password has been updated.')
            return redirect(url_for('user.login'))
        else:
            return redirect(url_for('home.index'))
    return render_template('user/reset_password.html', form=form)


@user.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Confirm your email address',
                       'mail/user/change_email',
                       user=current_user, token=token)
            flash('An email with instructions to confirm your new email '
                  'address has been sent to you.')
            return redirect(url_for('home.index'))
        else:
            flash('Invalid password.')
    return render_template("user/change_email.html", form=form)


@user.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash('Your email address has been updated.')
    else:
        flash('Invalid request.')
    return redirect(url_for('home.index'))

