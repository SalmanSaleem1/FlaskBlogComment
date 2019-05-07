from flaskface.test.testbase import BaseTestCase
import unittest
from flaskface.Models import User, UserSchema
from flaskface import bcrypt



class TestUser(BaseTestCase):

    def test_check_password(self):
        user = User.query.filter_by(email='testm@gmail.com').first()
        self.assertTrue(bcrypt.check_password_hash(user.password, 'salmanmayo'))
        self.assertFalse(bcrypt.check_password_hash(user.password, 'salman'))

    def test_user_registeration(self):
        print('test_user_registeration\n')
        with self.client:
            response = self.client.post('/registers', data=dict(
                name='TestM', username='testm2', email='testm@gmail.com',
                password='salmanmayo'
            ), follow_redirects=True)
            self.assertIn(b'', response.data)
            self.assertEqual(response.status_code, 200)

    def test_user_incorrect_registeration(self):
        with self.client:
            response = self.client.post('http://127.0.0.1:5000/registers', data=dict(
                name='TestM', usernname='testm2', email='testmgmail.com',
                password='salmanmayo'
            ), follow_redirects=True)
            self.assertIn(b'Invalid email address.', response.data)
            self.assertEqual(response.status_code, 200)


class TestUserLogin(BaseTestCase):

    def test_login_user(self):
        with self.client:
            response = self.client.post('http://127.0.0.1:5000/login', data=dict(
                email='testm@gmail.com', password='salmanmayo'
            ), follow_redirects=True)
            self.assertIn(b'Login Successfully', response.data)
            assert response.status_code == 200

    def test_invalid_login_user(self):
        print('test_invalid_login_user\n')
        with self.client:
            response = self.client.post('http://127.0.0.1:5000/login', data=dict(
                email='hamzagmail.com', password='salmanmayo'
            ), follow_redirects=True)
            self.assertIn(b'Invalid email or password', response.data)
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
