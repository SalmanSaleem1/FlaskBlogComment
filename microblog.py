from flaskface import app, db

from flaskface.Models import User, Post, Comment, PostLike


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Comment': Comment, 'PostLike': PostLike}
