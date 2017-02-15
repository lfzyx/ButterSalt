from flask import Blueprint, render_template
from flask_login import login_required
from index import app, Token

saltstack = Blueprint('saltstack', __name__, url_prefix='/salt')


@saltstack.route('/minions/')
@saltstack.route('/minions/<mid>')
@login_required
def minions(mid=None):
    if mid:
        data = Token.get(app.config.get('SALT_API') + '/minions/%s' % mid).json()
        return render_template('saltstack/minion.html', Data=data['return'][0])

    data = Token.get(app.config.get('SALT_API') + '/minions').json()
    return render_template('saltstack/minions.html', Data=data['return'][0])


@saltstack.route('/jobs/')
@saltstack.route('/jobs/<jid>')
@login_required
def jobs(jid=None):
    if jid:
        data = Token.get(app.config.get('SALT_API') + '/jobs/%s' % jid).json()
        return render_template('saltstack/job.html', Data=data['info'][0])
    data = Token.get(app.config.get('SALT_API') + '/jobs').json()
    return render_template('saltstack/jobs.html', Data=data['return'][0])


@saltstack.route('/keys/')
@saltstack.route('/keys/<mid>')
@login_required
def keys(mid=None):
    if mid:
        data = Token.get(app.config.get('SALT_API') + '/keys/%s' % mid).json()
        return render_template('saltstack/key.html', Data=data['return']['minions'])
    data = Token.get(app.config.get('SALT_API') + '/keys').json()
    return render_template('saltstack/keys.html', Data=data['return'])


@saltstack.route('/stats/')
@login_required
def stats():
    data = Token.get(app.config.get('SALT_API') + '/stats').json()
    return render_template('saltstack/stats.html', Data=data)
