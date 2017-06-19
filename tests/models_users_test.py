import unittest
from models import Users


class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = Users(password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = Users(password='cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = Users(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u = Users(password='cat')
        u2 = Users(password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)