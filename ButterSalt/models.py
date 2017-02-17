from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(120), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('user_role.id'))

    def __init__(self, username, password, email, role_id):
        self.username = username
        self.password = password
        self.email = email
        self.role_id = role_id

    def __repr__(self):
        return '<User %r with email %r role %r>' % (self.username, self.email, self.role_id)


class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    salt_username = db.Column(db.String(128))
    salt_password = db.Column(db.String(128))

    def __init__(self, salt_username, salt_password):
        self.salt_username = salt_username
        self.salt_password = salt_password

    def __repr__(self):
        return '<UserRole is saltstack pam user %r>' % (self.salt_username,)


class RoleAuthority(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    authority_name = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('user_role.id'))

    def __init__(self, authority_name, role_id):
        self.authority_name = authority_name
        self.role_id = role_id

    def __repr__(self):
        return '<authority %r in role_id %r>' % (self.authority_name, self.role_id)


class MoudleExecuteHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tgt = db.Column(db.String(128))
    fun = db.Column(db.String(128))
    args = db.Column(db.String(128))
    kwargs = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, tgt, fun, args, kwargs, user_id):
        self.tgt = tgt
        self.fun = fun
        self.args = args
        self.kwargs = kwargs
        self.user_id = user_id

    def __repr__(self):
        return '<Target %r Execute %r with args %r , kwargs %r by user_id %r>' % \
               (self.tgt, self.fun, self.args, self.kwargs, self.user_id)
