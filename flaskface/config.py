

class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = '123456789987456321'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///blog.db'
    POSTS_PER_PAGE = 3
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'idreesrehan234@gmail.com'
    MAIL_PASSWORD = 'salmanmayo321'
    LANGUAGES = ['en', 'es']


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
