from flask import Blueprint, render_template, request, flash, abort, redirect, url_for
from flask_login import login_required
import json
import requests
from ... import salt
from buttersalt_saltapi.saltapi import LoginError
import ipaddress

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
def minions():
    data = salt.get_minions()

    return render_template('saltstack/minions.html', Data=data)


@saltstack.route('/minions/<mid>')
def minion(mid=None):
    data = salt.get_minions(mid).get(mid)
    network = data.get('ip4_interfaces')

    def removelocalhost(network):
        localhost = []
        for k, v in network.items():
            if v == ['127.0.0.1']:
                localhost.append(k)

        for i in localhost:
            network.pop(i)

        return network

    def ip_private_or_public(network):
        iplist = {'private': [], 'public': []}
        for k, v in list(network.items()):
            if ipaddress.IPv4Address(v[0]).is_private:
                iplist['private'].append(v[0])
            elif ipaddress.IPv4Address(v[0]).is_global:
                iplist['public'].append(v[0])

        return iplist

    network = removelocalhost(network)
    network = ip_private_or_public(network)

    return render_template('saltstack/minion.html', Data=data, Network=network)


@saltstack.route('/jobs/')
def jobs():
    data = salt.get_jobs()
    return render_template('saltstack/jobs.html', Data=data)


@saltstack.route('/jobs/<jid>')
def job(jid=None):
    data = salt.get_jobs(jid)
    pretty = json.dumps(data["Result"], indent=4)
    return render_template('saltstack/job.html', Data=data, pretty=pretty)


@saltstack.route('/keys/',  methods=['GET', 'POST'])
def keys():
    if request.method == 'POST':
        if 'delete' in request.form:
            salt.delete_key(request.form.get('delete'))
        elif 'accept' in request.form:
            salt.accept_key(request.form.get('accept'))
        elif 'reject' in request.form:
            salt.reject_key(request.form.get('reject'))
        return redirect(url_for('saltstack.keys'))
    data = salt.get_keys()
    return render_template('saltstack/keys.html', Data=data)


@saltstack.route('/stats/')
def stats():
    data = salt.get_stats()
    return render_template('saltstack/stats.html', Data=data)
