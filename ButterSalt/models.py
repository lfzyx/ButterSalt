from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(120), unique=True)
    role_id = db.Column(db.Integer)


class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    salt_username = db.Column(db.String(128))
    salt_password = db.Column(db.String(128))


class RoleAuthority(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    authority_name = db.Column(db.String(128))
    role_id = db.Column(db.Integer)


class MoudleExecuteHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tgt = db.Column(db.String(128))
    fun = db.Column(db.String(128))
    args = db.Column(db.String(128))
    kwargs = db.Column(db.String(128))
    user_id = db.Column(db.Integer)

