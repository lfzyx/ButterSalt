import ButterSalt
import unittest


class ButterSaltTestCase(unittest.TestCase):

    def setUp(self):
        ButterSalt.app.config['TESTING'] = True
        ButterSalt.app.config['WTF_CSRF_ENABLED'] = False
        ButterSalt.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        ButterSalt.app.config['SQLALCHEMY_ECHO'] = False
        self.app = ButterSalt.app.test_client()
        ButterSalt.db.create_all()

    def login(self, username, password):
        return self.app.post('/user/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/user/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('admin', 'default')
        assert '/user/logout' in str(rv.data)
        assert 'Logged in successfully.' in str(rv.data)
        rv = self.logout()
        assert 'Please log in to access this page.' in str(rv.data)
        assert '/user/logout' not in str(rv.data)

    def test_index(self):
        self.login('admin', 'default')
        rv = self.app.get('/', follow_redirects=True)
        assert 'id="tgt" name="tgt" type="text" value="" placeholder="Required"' in str(rv.data)
        assert '/user/logout' in str(rv.data)

    def test_deployment(self):
        self.login('admin', 'default')
        rv = self.app.get('/deployment/operation', follow_redirects=True)
        assert '<table class="table table-hover">' in str(rv.data)
        assert '/user/logout' in str(rv.data)

    def test_salt_jobs(self):
        self.login('admin', 'default')
        rv = self.app.get('/salt/jobs/', follow_redirects=True)
        assert '<table class="table table-striped">' in str(rv.data)
        assert '/user/logout' in str(rv.data)

    def test_execution_command_testping(self):
        self.login('admin', 'default')
        rv = self.app.post('/', data=dict(
            tgt='HXtest3',
            fun='test.ping',
        ), follow_redirects=True)
        assert '[&#39;HXtest3&#39;]' in str(rv.data)

    def test_execution_command_testarg(self):
        self.login('admin', 'default')
        rv = self.app.post('/', data=dict(
            tgt='HXtest3',
            fun='test.arg',
            arg="/proc lol"
        ), follow_redirects=True)
        assert '<th> Arguments </th>' in str(rv.data)
        assert '__kwarg__' not in str(rv.data)

    def test_execution_command_testkwarg(self):
        self.login('admin', 'default')
        rv = self.app.post('/', data=dict(
            tgt='HXtest3',
            fun='test.arg',
            arg="/proc lol",
            kwarg='lol=wow'
        ), follow_redirects=True)
        assert '__kwarg__' in str(rv.data)


if __name__ == '__main__':
    unittest.main()
