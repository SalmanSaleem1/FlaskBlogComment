from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError, TextAreaField, TextField
from flask_wtf.file import FileAllowed, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flaskface.Models import User
from flaskface.constant.app_constant import constants
from flask_babel import lazy_gettext as _l


class RegisterForm(FlaskForm):
    name = StringField(_l('Name'), validators=[DataRequired(), Length(min=2, max=25)])
    username = StringField(_l('User Name'), validators=[DataRequired(), Length(min=2, max=15)])
    email = StringField(_l('Email'), validators=[DataRequired(), Length(min=2, max=25), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired(), Length(min=2, max=25)])
    confirm_password = PasswordField(_l('Confirm Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Submit'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(f"{constants.USER_ALREADY_EXIST}")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(f"{constants.EMAIL_ALREADY_EXIST}")


class LoginForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    submit = SubmitField('Login')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(f"{constants.FIRST_REGISTER_EMAIL}")


class AccountForm(FlaskForm):
    name = StringField(_l('Name'), validators=[DataRequired(), Length(min=2, max=25)])
    username = StringField(_l('User Name'), validators=[DataRequired(), Length(min=2, max=25)])
    email = StringField(_l('Email'), validators=[DataRequired(), Length(min=2, max=35), Email()])
    picture = FileField(_l('Upload Image'), validators=[FileAllowed(['jpg', 'jpeg', 'png'])])

    update = SubmitField('Update')


class RequestResetForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Length(min=2, max=25), Email()])
    submit = SubmitField(_l('Request Reset Password'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError


class RequestPasswordForm(FlaskForm):
    password = StringField(_l('Password'), validators=[DataRequired(), Length(min=2, max=25), Email()])
    confirm_password = StringField(_l('Confirm Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Request Reset Password'))


class MessageForm(FlaskForm):
    message = TextAreaField(_l('Message'), validators=[
        DataRequired(), Length(min=0, max=140), ])
    submit = SubmitField(_l('Submit'))
