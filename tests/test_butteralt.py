import unittest
import manage


class ButterSaltTestCase(unittest.TestCase):

    testapp = manage.app.test_client()
    manage.app.config['TESTING'] = True
    manage.app.config['WTF_CSRF_ENABLED'] = False
    manage.app.config['DASHBOARD_ADMIN'] = 'admin:admin'

    def login(self, username, password):
        return self.testapp.post('/user/login', data=dict(
            username=username,
            password=password,
        ), follow_redirects=True)

    def logout(self):
        return self.testapp.get('/user/logout', follow_redirects=True)

    def test_login_logout_signup(self):
        rv = self.login('admin', 'admin')
        assert 'Logged in successfully' in rv.data.decode()
        rv = self.logout()
        assert 'You have been logged out.' in rv.data.decode()
        rv = self.login('adminx', 'default')
        assert 'Invalid usename or password.' in rv.data.decode()
        rv = self.login('admin', 'defaultx')
        assert 'Invalid usename or password.' in rv.data.decode()

    def test_dashboard(self):
        self.login('admin', 'admin')
        rv = self.testapp.get('/', follow_redirects=True)
        assert 'Job status' in rv.data.decode()

    def test_run(self):
        self.login('admin', 'admin')
        rv = self.testapp.get('/run/', follow_redirects=True)
        assert '<label class="control-label" for="tgt">' in rv.data.decode()

    def test_salt_jobs(self):
        self.login('admin', 'admin')
        rv = self.testapp.get('/salt/jobs/', follow_redirects=True)
        assert '<table class="table table-striped">' in rv.data.decode()

    def test_salt_minions(self):
        self.login('admin', 'admin')
        rv = self.testapp.get('/salt/minions/', follow_redirects=True)
        assert '<table class="table table-striped">' in rv.data.decode()

    def test_salt_keys(self):
        self.login('admin', 'admin')
        rv = self.testapp.get('/salt/keys/', follow_redirects=True)
        assert '<table class="table table-hover">' in rv.data.decode()

    def test_salt_stats(self):
        self.login('admin', 'admin')
        rv = self.testapp.get('/salt/stats/', follow_redirects=True)
        assert '<table class="table table-striped">' in rv.data.decode()


if __name__ == '__main__':
    unittest.main()
