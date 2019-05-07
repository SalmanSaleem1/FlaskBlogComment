from flaskface import db, login_manager, ma, bcrypt, app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serelizer


@login_manager.user_loader
def get_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    username = db.Column(db.String(60), nullable=False, unique=True)
    email = db.Column(db.String(60), nullable=False, unique=True)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60))
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expire_time=1800):
        s = Serelizer(app.config['SECRET_KEY'], expire_time)
        token = s.dumps({'user_id': self.id}).decode('utf-8')
        return token

    @staticmethod
    def verify_reset_token(token):
        s = Serelizer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __init__(self, name, username, email, password):
        self.name = name
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return "User('{self.username}','{self.email}','{self.image_file}','{self.password}')".format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.create_at}', '{self.user_id}')"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, body=None, timestamp=None, post_id=None, user_id=None):
        self.body = body
        self.timestamp = timestamp
        self.post_id = post_id
        self.user_id = user_id

    def __repr__(self):
        return f"Comment('{self.body}', '{self.timestamp}', '{self.post_id}', '{self.user_id}')"


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User


class PostSchema(ma.ModelSchema):
    class Meta:
        model = Post
