from flaskface.test.testbase import BaseTestCase
import unittest
import os



class TestPost(BaseTestCase):

    def test_post(self):
        with self.client:
            self.client.post('/login', data=dict(
                email='junaid@gmail.com', password='salmanmayo'
            ), follow_redirects=True)
            self.client.post('/newpost', data=dict(
                title='Salman Saleem', content='salman saleem is a good developer'
            ))

            response = self.client.get('/', data=dict(
                title='Salman Saleem', content='salman saleem is a good developer'
            ))
            self.assertIn(b'Post Successfully', response.data)
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()

