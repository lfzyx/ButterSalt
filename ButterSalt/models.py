from . import db


class HostManagement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    bind_product_application = db.Column(db.String(128))
    bind_system_application = db.Column(db.String(128))
    creator = db.Column(db.String(128), nullable=False)
    modifer = db.Column(db.String(128))
    last_modify_time = db.Column(db.String(128))


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    role = db.Column(db.String(128), nullable=False)

    def __init__(self, username, password, email, role):
        self.username = username
        self.password = password
        self.email = email
        self.role = role

    def __repr__(self):
        return '<User %r with email %r role %r>' % (self.username, self.email, self.role)


class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    salt_username = db.Column(db.String(128))
    salt_password = db.Column(db.String(128))

    def __init__(self, name, salt_username, salt_password):
        self.name = name
        self.salt_username = salt_username
        self.salt_password = salt_password

    def __repr__(self):
        return '<UserRole is saltstack pam user %r>' % (self.salt_username,)


class UserRoleAuthority(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    role = db.Column(db.String(128), nullable=False)
    resources = db.Column(db.String(128), nullable=False)

    def __init__(self, name, role):
        self.name = name
        self.role = role

    def __repr__(self):
        return '<authority %r in role_id %r>' % (self.name, self.role)


class SaltExecuteHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tgt = db.Column(db.String(128), nullable=False)
    fun = db.Column(db.String(128), nullable=False)
    args = db.Column(db.String(128))
    kwargs = db.Column(db.String(128))
    user = db.Column(db.String(128), nullable=False)

    def __init__(self, tgt, fun, args, kwargs, user):
        self.tgt = tgt
        self.fun = fun
        self.args = args
        self.kwargs = kwargs
        self.user = user

    def __repr__(self):
        return '<Target %r Execute %r with args %r , kwargs %r by user %r>' % \
               (self.tgt, self.fun, self.args, self.kwargs, self.user)


class ProductApplications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    online_version = db.Column(db.String(128))
    bind_host = db.Column(db.String(128))
    creator = db.Column(db.String(128), nullable=False)
    modifer = db.Column(db.String(128))
    last_modify_time = db.Column(db.String(128))

    def __init__(self, name, online_version, bind_host, creator, modifer, last_modify_time):
        self.name = name
        self.online_version = online_version
        self.bind_host = bind_host
        self.creator = creator
        self.modifer = modifer
        self.last_modify_time = last_modify_time

    def __repr__(self):
        return '<%r deploy number is %r>' % (self.name, self.online_version)


class ProductApplicationsConfigurations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    bind_application = db.Column(db.String(128))
    version = db.Column(db.String(128), nullable=False)
    creator = db.Column(db.String(128), nullable=False)
    modifer = db.Column(db.String(128))
    last_modify_time = db.Column(db.String(128))

    def __init__(self, name, bind_application, version, creator, modifer, last_modify_time):
        self.name = name
        self.bind_application = bind_application
        self.version = version
        self.creator = creator
        self.modifer = modifer
        self.last_modify_time = last_modify_time


class SystemApplications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    bind_host = db.Column(db.String(128))
    creator = db.Column(db.String(128), nullable=False)
    modifer = db.Column(db.String(128))
    last_modify_time = db.Column(db.String(128))

    def __init__(self, name, bind_host, creator, modifer, last_modify_time):
        self.name = name
        self.bind_host = bind_host
        self.creator = creator
        self.modifer = modifer
        self.last_edit_time = last_modify_time


class SystemApplicationsConfigurations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    bind_application = db.Column(db.String(128))
    version = db.Column(db.String(128), nullable=False)
    creator = db.Column(db.String(128), nullable=False)
    modifer = db.Column(db.String(128))
    last_modify_time = db.Column(db.String(128))

    def __init__(self, name, bind_application, version, creator, modifer, last_modify_time):
        self.name = name
        self.bind_application = bind_application
        self.version = version
        self.creator = creator
        self.modifer = modifer
        self.last_modify_time = last_modify_time
