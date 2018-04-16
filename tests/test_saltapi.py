import unittest
import os
from buttersalt_saltapi import saltapi


url = os.environ.get('SALT_API_URI') or "http://buttersalt:buttersalt@127.0.0.1:8000"


class App(object):
    class config(object):
        @classmethod
        def get(self, SALT_API_URI):
            return url


app = App()
salt = saltapi.SaltApi()
salt.init_app(app)


class ServerTestCase(unittest.TestCase):

    def test_login(self):
        re = salt.login()
        self.assertTrue(re)

    def test_get_keys(self):
        re = salt.get_keys()
        self.assertIsInstance(re.get('minions'), list)

    def test_get_jobs(self):
        re = salt.get_jobs()
        self.assertIsInstance(re, dict)

    def test_get_minions(self):
        re = salt.get_minions()
        self.assertIsInstance(re, dict)

    def test_get_stats(self):
        re = salt.get_stats()
        self.assertIsInstance(re, dict)

