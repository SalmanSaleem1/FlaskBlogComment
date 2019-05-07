from flaskface.test.testbase import BaseTestCase
import unittest


class TestMain(BaseTestCase):

    def test_home(self):
        response = self.client.post('/login')
        assert response.status_code == 200

    def test_home_route_requires_login(self):
        response = self.client.post('/', follow_redirects=True)
        self.assertIn(b'Please log in to access this page.', response.data)
        assert response.status_code == 200

    def test_posts_show_up_on_main_page(self):
        response = self.client.post('/', data=dict(email='junaid@gmail.com', password='salmanmayo'),
                                    follow_redirects=True)

        self.assertIn(b'', response.data)
        assert response.status_code == 200


if __name__ == '__main__':
    unittest.main()
