""" This is a wrapper for remote salt rest_cherrypy API!

Salt API have two interface used for execution command.
The one is LowDataAdapter, the other is Minions.
LowDataAdapter execution command and response contains the result of those function calls.
LowDataAdapter allow choose a client interface(local,runner,wheel).
Minions execution command and immediately return the job id.
Minions use local client enforce.
"""

import requests
import json


class LoginError(Exception):
    def __init__(self, value):
        self.value = value


class SaltApiBase(object):
    """ Salt api Base object.

    """

    def __init__(self, app=None, baseurl=None, username=None, password=None, eauth='pam'):
        if app is not None:
            self.init_app(app)

        """ Instantiation SaltApiBase class.

        :param baseurl: salt api address
        :param username: salt eauth username
        :param password: salt eauth password
        :param eauth: the salt eauth backend configured for the user
        """
        self.address = baseurl
        self.username = username
        self.password = password
        self.eauth = eauth
        self.Token = requests.Session()

    def __repr__(self):
        return "[address=%s, username=%s, password=%s, eauth=%s, Token=%s]" % \
               (self.address, self.username, self.password, self.eauth, self.Token)

    def init_app(self, app):
        self.address = app.config.get('SALT_API')
        self.username = app.config.get('SALT_USERNAME')
        self.password = app.config.get('SALT_PASSWORD')

    def login(self):
        """ salt.netapi.rest_cherrypy.app.Login!

        :return: True
        """
        try:
            responseinfo = self.Token.post(self.address + '/login', json={
                'username': self.username,
                'password': self.password,
                'eauth': self.eauth,
            })
        except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError, requests.exceptions.Timeout,
                requests.exceptions.TooManyRedirects, requests.exceptions.RequestException) as err:
            raise LoginError('Requests Failed')
        except TypeError as err:
            raise LoginError('Requests Failed {}'.format(err))

        else:
            if responseinfo.status_code == 200:
                return True
            else:
                raise LoginError('Login Failed')

    def get_keys(self, key=None):
        """ salt.netapi.rest_cherrypy.app.Keys!

        :param key: a specific key
        :return: Show the list of minion keys or detail on a specific key
        """
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

    def delete_key(self, key):
        """ salt.wheel.key.delete!
        
        """
        try:
            self.login()
        except LoginError:
            return False
        else:
            responseinfo = self.Token.post(self.address + '/', json={
                'client': "wheel",
                'fun': "key.delete",
                'match': key,
            })
            return responseinfo.json()['return'][0]['data']['success']

    def accept_key(self, key):
        """ salt.wheel.key.delete!

        """
        try:
            self.login()
        except LoginError:
            return False
        else:
            responseinfo = self.Token.post(self.address + '/', json={
                'client': "wheel",
                'fun': "key.accept",
                'match': key,
            })
            return responseinfo.json()['return'][0]['data']['success']

    def get_jobs(self, jid=None):
        """ salt.netapi.rest_cherrypy.app.Jobs！

        :param jid: job id
        :return: List jobs or show a single job from the job cache.
        """
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
        """ salt.netapi.rest_cherrypy.app.Minions!

        :param mid: minion id
        :return: lists of minions or  minion details
        """
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
        """ salt.netapi.rest_cherrypy.app.Stats!

        :return: Return a dump of statistics collected from the CherryPy server
        """
        try:
            self.login()
        except LoginError:
            return False
        else:
            responseinfo = self.Token.get(self.address + '/stats')
            return responseinfo.json()

    def execution_command_minions(self, tgt=None, expr_form='glob', fun=None, args=None, kwargs=None):
        """ execution command and immediately return the job id.

        :param tgt: The minions
        :param expr_form: Targets match rules
        :param fun: The command
        :param args: The args
        :param kwargs: The kwargs
        :return: The job id
        """
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
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

    def execution_command_low(self, client='local', tgt=None, expr_form='glob', fun=None,  args=None, kwargs=None):
        """ execution command and response contains the result of those function calls.

        :param client: Thr client
        :param tgt: The minions
        :param expr_form: Targets match rules
        :param fun: The command
        :param args: The args
        :param kwargs: The kwargs
        :return: Response contains the result of the function calls
        """
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        try:
            self.login()
        except LoginError:
            return False
        else:
            if tgt is None:
                # Generally the client is runner
                responseinfo = self.Token.post(self.address + '/', json={
                    'client': client,
                    'expr_form': expr_form,
                    'fun': fun,
                    'arg': args,
                    'kwarg': kwargs,
                })
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

    def read_pillar_file(self, path):
        try:
            self.login()
        except LoginError as e:
            return e
        else:
            responseinfo = self.execution_command_low(client='wheel', fun='pillar_roots.read', args=[path])
            return responseinfo['data']

    def write_pillar_file(self, data, path):
        try:
            self.login()
        except LoginError as e:
            return e
        else:
            responseinfo = self.execution_command_low(client='wheel', fun='pillar_roots.write', args=[data, path])
            return responseinfo['data']

    def read_state_file(self, path):
        try:
            self.login()
        except LoginError as e:
            return e
        else:
            responseinfo = self.execution_command_low(client='wheel', fun='file_roots.read', args=[path])
            return responseinfo['data']

    def write_state_file(self, data, path):
        try:
            self.login()
        except LoginError as e:
            return e
        else:
            responseinfo = self.execution_command_low(client='wheel', fun='file_roots.write', args=[data, path])
            return responseinfo['data']
