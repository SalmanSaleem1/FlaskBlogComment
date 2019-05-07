from flask_testing import TestCase
from flaskface.config import TestConfig
from flaskface import app, db


class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object(TestConfig)
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()


    # def tearDown(self):
    #     db.session.drop_all()
    #     db.session.commit()