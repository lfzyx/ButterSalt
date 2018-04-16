from flask import Blueprint, render_template, request, flash, abort
from flask_login import login_required
import json
import requests
from ... import salt
from buttersalt_saltapi.saltapi import LoginError

saltstack = Blueprint('saltstack', __name__, url_prefix='/salt')


@saltstack.before_app_request
def before_request():
    try:
        salt.login()
    except LoginError as e:
        flash('Salt API Login Fail : status {}'.format(e))
        abort(500)
    except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError, requests.exceptions.Timeout,
            requests.exceptions.TooManyRedirects, requests.exceptions.RequestException) as e:
        flash('Salt API Connection Error : status {}'.format(e))
        abort(500)


@saltstack.before_request
@login_required
def before_request():
    pass


@saltstack.route('/minions/')
@saltstack.route('/minions/<mid>')
def minions(mid=None):
    data = salt.get_minions(mid)
    if mid:
        return render_template('saltstack/minion.html', Data=data)
    return render_template('saltstack/minions.html', Data=data)


@saltstack.route('/jobs/')
@saltstack.route('/jobs/<jid>')
def jobs(jid=None):
    data = salt.get_jobs(jid)
    if jid:
        pretty = json.dumps(data["Result"], indent=4)
        return render_template('saltstack/job.html', Data=data, pretty=pretty)
    return render_template('saltstack/jobs.html', Data=data)


@saltstack.route('/keys/',  methods=['GET', 'POST'])
@saltstack.route('/keys/<mid>')
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
def stats():
    data = salt.get_stats()
    return render_template('saltstack/stats.html', Data=data)
