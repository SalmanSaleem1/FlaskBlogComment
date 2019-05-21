from flask import Flask
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel, _, lazy_gettext as _l
from flask_migrate import Migrate

from flaskface.config import BaseConfig

app = Flask(__name__, template_folder='template')

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

app.config.from_object(BaseConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
moment = Moment(app)
bootstrap = Bootstrap(app)
babel = Babel(app)

login_manager = LoginManager(app)
login_manager.login_view = 'user.login'
login_manager.login_message_category = _l(f'Please log in to access this page.')

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
