from flask import Blueprint, render_template
from flask_login import login_required
from ButterSalt import salt

saltstack = Blueprint('saltstack', __name__, url_prefix='/salt')


@saltstack.route('/minions/')
@saltstack.route('/minions/<mid>')
@login_required
def minions(mid=None):
    data = salt.get_minions(mid)
    if mid:
        return render_template('saltstack/minion.html', Data=data)
    return render_template('saltstack/minions.html', Data=data)


@saltstack.route('/jobs/')
@saltstack.route('/jobs/<jid>')
@login_required
def jobs(jid=None):
    data = salt.get_jobs(jid)
    if jid:
        return render_template('saltstack/job.html', Data=data)
    return render_template('saltstack/jobs.html', Data=data)


@saltstack.route('/keys/')
@saltstack.route('/keys/<mid>')
@login_required
def keys(mid=None):
    data = salt.get_keys(mid)
    if mid:
        return render_template('saltstack/key.html', Data=data)
    return render_template('saltstack/keys.html', Data=data)


@saltstack.route('/stats/')
@login_required
def stats():
    data = salt.get_stats()
    return render_template('saltstack/stats.html', Data=data)
