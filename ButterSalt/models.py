from . import db


class HostManagement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    bind_product_application = db.Column(db.Integer, db.ForeignKey('product_applications.id'))
    bind_system_application = db.Column(db.Integer, db.ForeignKey('system_applications.id'))
    creator = db.Column(db.String(128), nullable=False)
    modifer = db.Column(db.String(128))
    last_modify_time = db.Column(db.String(128))

    def __repr__(self):
        return "<HostManagement" \
               "(name=%s, bind_product_application=%s, bind_system_application=%s, creator=%s)>" % \
               (self.name, self.bind_product_application, self.bind_system_application, self.creator)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    role = db.Column(db.Integer, db.ForeignKey('user_role.id'))

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
    user = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return "<SaltExecuteHistory" \
               "(tgt=%s, fun=%s, args=%s, kwargs=%s, user=%s)>" % \
               (self.tgt, self.fun, self.args, self.kwargs, self.user)


class ProductApplications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    creator = db.Column(db.String(128), nullable=False)
    modifer = db.Column(db.String(128))
    last_modify_time = db.Column(db.String(128))
    integration_version = db.Column(db.String(128))
    delivery_version = db.Column(db.String(128))
    deployment_version = db.Column(db.String(128))
    configurations = db.relationship("ProductApplicationsConfigurations", backref="applications", lazy='dynamic')

    def __repr__(self):
        return "<ProductApplications" \
               "(name=%s, creator=%s, integration_version=%s, delivery_version=%s, deployment_version=%s)>" % \
               (self.name, self.creator, self.integration_version, self.delivery_version, self.deployment_version)


class ProductApplicationsConfigurations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    bind_application = db.Column(db.Integer, db.ForeignKey('product_applications.id'))
    bind_host = db.Column(db.String(128))
    version = db.Column(db.String(128), nullable=False)
    creator = db.Column(db.String(128), nullable=False)
    modifer = db.Column(db.String(128))
    last_modify_time = db.Column(db.String(128))

    def __repr__(self):
        return "<ProductApplicationsConfigurations" \
               "(name=%s, bind_application=%s, bind_host=%s, version=%s,creator=%s)>" % \
               (self.name, self.bind_application, self.bind_host, self.version, self.creator)


class SystemApplications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    creator = db.Column(db.String(128), nullable=False)
    modifer = db.Column(db.String(128))
    last_modify_time = db.Column(db.String(128))
    configurations = db.relationship("SystemApplicationsConfigurations", backref="applications", lazy='dynamic')

    def __repr__(self):
        return "<SystemApplications(name=%s, creator=%s)>" % (self.name, self.creator)


class SystemApplicationsConfigurations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    bind_application = db.Column(db.Integer, db.ForeignKey('system_applications.id'))
    bind_host = db.Column(db.String(128))
    version = db.Column(db.String(128), nullable=False)
    creator = db.Column(db.String(128), nullable=False)
    modifer = db.Column(db.String(128))
    last_modify_time = db.Column(db.String(128))

    def __repr__(self):
        return "<SystemApplicationsConfigurations" \
               "(name=%s, bind_application=%s, bind_host=%s, version=%s, creator=%s)>" % \
               (self.name, self.bind_application, self.bind_host, self.version, self.creator)
