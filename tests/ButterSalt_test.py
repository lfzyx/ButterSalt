import os
import unittest
import tempfile
import ButterSalt


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        ButterSalt.app.config['TESTING'] = True
        ButterSalt.app.config['WTF_CSRF_ENABLED'] = False
        ButterSalt.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ButterSalt:ButterSalt@192.168.1.73/test'
        self.app = ButterSalt.app.test_client()
        ButterSalt.db.create_all()

    def tearDown(self):
        ButterSalt.db.drop_all()

    def signup(self, username, email, password):
        return self.app.post('/user/signup', data=dict(
            username=username,
            email=email,
            password0=password,
            password1=password,
        ), follow_redirects=True)

    def login(self, username, password):
        return self.app.post('/user/login', data=dict(
            username=username,
            password=password,
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/user/logout', follow_redirects=True)

    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'Redirecting' in rv.data.decode()
        rv = self.app.get('/', follow_redirects=True)
        assert 'Sign up' in rv.data.decode()

    def test_signup(self):
        rv = self.signup('admin', 'admin@admin.com', '123456')
        assert 'Sign up Successfully!' in rv.data.decode()
        rv = self.signup('admin', 'admin@admin.com', '123456')
        assert 'Username already in use.' in rv.data.decode()
        assert 'Email already registered.' in rv.data.decode()

    def test_login_logout(self):
        self.signup('admin', 'admin@admin.com', '123456')
        rv = self.login('admin', '123456')
        assert 'Logged in successfully.' in rv.data.decode()
        rv = self.logout()
        assert 'You have been logged out.' in rv.data.decode()
        rv = self.login('adminx', 'default')
        assert 'Invalid usename or password.' in rv.data.decode()
        rv = self.login('admin', 'defaultx')
        assert 'Invalid usename or password.' in rv.data.decode()

    def test_home(self):
        self.signup('admin', 'admin@admin.com', '123456')
        self.login('admin', '123456')
        rv = self.app.get('/', follow_redirects=True)
        assert 'id="tgt" name="tgt" type="text" value="" placeholder="Required"' in rv.data.decode()


if __name__ == '__main__':
    unittest.main()