from . import db
from werkzeug.security import generate_password_hash, check_password_hash


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False, index=True)
    password = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    role = db.Column(db.Integer, db.ForeignKey('user_role.id'))

    def password_hash(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<Users" \
               "(username=%s, password=%s, email=%s, role=%s)>" % \
               (self.username, self.password, self.email, self.role)


class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    salt_username = db.Column(db.String(128))
    salt_password = db.Column(db.String(128))

    def __repr__(self):
        return "<UserRole" \
               "(name=%s, salt_username=%s, salt_password=%s)>" % \
               (self.name, self.salt_username, self.salt_password, )


class UserRoleAuthority(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    role = db.Column(db.Integer, db.ForeignKey('user_role.id'))
    resources = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<authority %r in role_id %r>' % (self.name, self.role)


class SaltExecuteHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tgt = db.Column(db.String(128), nullable=False)
    fun = db.Column(db.String(128), nullable=False)
    args = db.Column(db.String(128))
    kwargs = db.Column(db.String(128))
    user = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return "<SaltExecuteHistory" \
               "(tgt=%s, fun=%s, args=%s, kwargs=%s, user=%s)>" % \
               (self.tgt, self.fun, self.args, self.kwargs, self.user)

