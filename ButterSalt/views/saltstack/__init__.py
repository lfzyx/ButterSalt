from flask import Blueprint, render_template, request, current_app
from flask_login import login_required
import json
from ButterSalt.saltapi import SaltApi

saltstack = Blueprint('saltstack', __name__, url_prefix='/salt')


salt = SaltApi(
    current_app.config.get('SALT_API'),
    current_app.config.get('USERNAME'),
    current_app.config.get('PASSWORD')
)


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
        pretty = json.dumps(data["Result"], indent=4)
        return render_template('saltstack/job.html', Data=data, pretty=pretty)
    return render_template('saltstack/jobs.html', Data=data)


@saltstack.route('/keys/',  methods=['GET', 'POST'])
@saltstack.route('/keys/<mid>')
@login_required
def keys(mid=None):
    data = salt.get_keys(mid)
    if mid:
        return render_template('saltstack/key.html', Data=data)
    if request.method == 'POST':
        if 'delete' in request.form:
            salt.delete_key(request.form.get('delete'))
        elif 'accept' in request.form:
            salt.accept_key(request.form.get('accept'))
        data = salt.get_keys(mid)
    return render_template('saltstack/keys.html', Data=data)


@saltstack.route('/stats/')
@login_required
def stats():
    data = salt.get_stats()
    return render_template('saltstack/stats.html', Data=data)
