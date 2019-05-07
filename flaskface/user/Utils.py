import secrets
import os
from flask import url_for
from flaskface import app, mail
from flask_mail import Message


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pic', picture_fn)
    form_picture.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password reset message', sender='noreply@gmail.com', recipients=[user.email])
    msg.body = f'''This is rest password email\
{url_for('user.reset_token', token=token, _external=True)}'''
    mail.send(msg)
    return "sent"