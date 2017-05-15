from . import db
from werkzeug.security import generate_password_hash, check_password_hash


class HostManagement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(128))
    creator = db.Column(db.String(128), nullable=False)
    modifer = db.Column(db.String(128))
    last_modify_time = db.Column(db.String(128))
    applicationhost = db.relationship("ProductApplications", backref="applicationhost", lazy='dynamic')

    def __repr__(self):
        return "<HostManagement(name=%s, role=%s)>" % \
               (self.name, self.role)


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


class ProductApplications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    bind_host = db.Column(db.Integer, db.ForeignKey('host_management.id'))
    delivery_version = db.Column(db.String(128))
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))
    modifer = db.Column(db.Integer, db.ForeignKey('users.id'))
    last_modify_time = db.Column(db.String(128))
    configurations = db.relationship("ProductApplicationsConfigurations", backref="productapplication", lazy='dynamic')

    def __repr__(self):
        return "<ProductApplications(name=%s, bind_host=%s, delivery_version=%s)>" % \
               (self.name, self.bind_host, self.delivery_version)


class ProductApplicationsConfigurations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bind_application = db.Column(db.Integer, db.ForeignKey('product_applications.id'))
    file = db.Column(db.String(128))
    content = db.Column(db.String(1024))
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))
    modifer = db.Column(db.Integer, db.ForeignKey('users.id'))
    last_modify_time = db.Column(db.String(128))

    def __repr__(self):
        return "<ProductApplicationsConfigurations(bind_application=%s, file=%s, content=%s)>" % \
               (self.bind_application, self.file, self.content)


class SystemApplications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))
    modifer = db.Column(db.Integer, db.ForeignKey('users.id'))
    last_modify_time = db.Column(db.String(128))
    configurations = db.relationship("SystemApplicationsConfigurations", backref="applications", lazy='dynamic')

    def __repr__(self):
        return "<SystemApplications(name=%s)>" % (self.name,)


class SystemApplicationsConfigurations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bind_host = db.Column(db.String(128))
    bind_application = db.Column(db.Integer, db.ForeignKey('system_applications.id'))
    version = db.Column(db.String(128), nullable=False)
    pillar = db.Column(db.String(128))
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))
    modifer = db.Column(db.Integer, db.ForeignKey('users.id'))
    last_modify_time = db.Column(db.String(128))

    def __repr__(self):
        return "<SystemApplicationsConfigurations(bind_application=%s, bind_host=%s, version=%s)>" % \
               (self.bind_application, self.bind_host, self.version)
