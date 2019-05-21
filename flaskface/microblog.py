from flaskface import app, db

from flaskface.Models import User, Post, Comment, PostLike, Message, Notifications


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Comment': Comment, 'PostLike': PostLike, 'Message': Message,
            'Notifications': Notifications}
