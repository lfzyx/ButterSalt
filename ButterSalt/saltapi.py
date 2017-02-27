""" This is a wrapper for remote salt rest_cherrypy API!

Salt API have two interface used for execution command.
The one is LowDataAdapter, the other is Minions.
LowDataAdapter execution command and response contains the result of those function calls.
Minions execution command and immediately return the job id.

LowDataAdapter allow choose a client interface(local,runner,wheel), Minions use local enforce.
"""

import requests
import json


class LoginError(Exception):
    def __init__(self, value):
        self.value = value


class SaltApiBase(object):
    """ Salt api Base object.

    """

    def __init__(self, baseurl, username, password, eauth='pam'):
        self.address = baseurl
        self.username = username
        self.password = password
        self.eauth = eauth
        self.Token = requests.Session()

    def login(self):
        responseinfo = self.Token.post(self.address + '/login', json={
            'username': self.username,
            'password': self.password,
            'eauth': self.eauth,
        })
        if responseinfo.status_code == 200:
            return True
        else:
            raise LoginError('Login Failed')

    def get_keys(self, key=None):
        try:
            self.login()
        except LoginError:
            return False
        else:
            if key:
                responseinfo = self.Token.get(self.address + '/keys/%s' % key)
                return responseinfo.json()['return']['minions']
            else:
                responseinfo = self.Token.get(self.address + '/keys')
                return responseinfo.json()['return']

    def get_jobs(self, jid=None):
        try:
            self.login()
        except LoginError:
            return False
        else:
            if jid:
                responseinfo = self.Token.get(self.address + '/jobs/%s' % jid)
                return responseinfo.json()['info'][0]
            else:
                responseinfo = self.Token.get(self.address + '/jobs')
                return responseinfo.json()['return'][0]

    def get_minions(self, mid=None):
        try:
            self.login()
        except LoginError:
            return False
        else:
            if mid:
                responseinfo = self.Token.get(self.address + '/minions/%s' % mid)
                return responseinfo.json()['return'][0]
            else:
                responseinfo = self.Token.get(self.address + '/minions')
                return responseinfo.json()['return'][0]

    def get_stats(self):
        try:
            self.login()
        except LoginError:
            return False
        else:
            responseinfo = self.Token.get(self.address + '/stats')
            return responseinfo.json()

    def execution_command_minions(self, *args, tgt=None, expr_form='glob', fun=None,  **kwargs):
        try:
            self.login()
        except LoginError:
            return False
        else:
            responseinfo = self.Token.post(self.address + '/minions/', json={
                'tgt': tgt,
                'expr_form': expr_form,
                'fun': fun,
                'arg': args,
                'kwarg': kwargs,
            })
            return responseinfo.json()['return'][0]['jid']

    def execution_command_low(self, *args, client='local', tgt=None, expr_form='glob', fun=None,  **kwargs):
        try:
            self.login()
        except LoginError:
            return False
        else:
            responseinfo = self.Token.post(self.address + '/', json={
                'client': client,
                'tgt': tgt,
                'expr_form': expr_form,
                'fun': fun,
                'arg': args,
                'kwarg': kwargs,
            })
            return responseinfo.json()['return'][0]


class SaltApi(SaltApiBase):
    """ Salt api advanced object.

    """

    def get_accepted_keys(self):
        return json.dumps(self.get_keys()['minions'])
















