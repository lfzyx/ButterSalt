from flask import Blueprint
from flask_login import login_required
from flask import render_template
from ButterSalt import app, Token


class Mid:
    def __init__(self, tgt):
        self.tgt = tgt

    def get_uptime(self):
        data = Token.post(app.config.get('SALT_API') + '/', json={
                "client": "local",
                "tgt": self.tgt,
                "fun": "status.uptime"
            }).json()
        return data

    def get_grains(self):
        data = Token.post(app.config.get('SALT_API') + '/', json={
            "client": "local",
            "tgt": self.tgt,
            "fun": "grains.items"
        }).json()
        return data


cmdb = Blueprint('cmdb', __name__, url_prefix='/cmdb')


@cmdb.route('/')
@login_required
def index():
    data = Token.post(app.config.get('SALT_API') + '/', json={
            "client": "runner",
            "fun": "manage.status"
        }).json()
    return render_template('cmdb/index.html', up=data['return'][0]['up'], down=data['return'][0]['down'])


@cmdb.route('/manage/')
@cmdb.route('/manage/<mid>')
@login_required
def manage(mid=None):
    mid_grains = Mid(mid)
    return render_template('cmdb/manage.html', uptime=mid_grains.get_uptime()['return'][0][mid],
                           grains=mid_grains.get_grains()['return'][0][mid])
