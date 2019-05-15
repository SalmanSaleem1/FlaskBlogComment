from flask import Flask
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from pusher import Pusher
from flask_babel import Babel

from flaskface.config import BaseConfig

app = Flask(__name__, template_folder='template')

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'


pusher_client = Pusher(
    app_id='771243',
    key='ca7c12f18787cfa7312a',
    secret='d9592f46e61154b944ec',
    cluster='ap2',
    ssl=True)

app.config['SECRET_KEY'] = 'lablam.2017'
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Le-lKIUAAAAAJBMVig-TrLnqIz0Eu0q6vvIXXRo'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Le-lKIUAAAAADiEhXqGkzbIy5fccpu-DZ9oXhZJ'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'black'}

app.config.from_object(BaseConfig)
db = SQLAlchemy(app)

ma = Marshmallow(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
moment = Moment(app)
bootstrap = Bootstrap(app)
babel = Babel(app)

login_manager = LoginManager(app)
login_manager.login_view = 'user.login'
login_manager.login_message_category = 'info'

from flaskface.user.Routes import user
from flaskface.post.Routes import post
from flaskface.main.Routes import main
from flaskface.error.CustomeError import errors
from flaskface.comments.route import comment

app.register_blueprint(user)
app.register_blueprint(post)
app.register_blueprint(main)
app.register_blueprint(errors)
app.register_blueprint(comment)
