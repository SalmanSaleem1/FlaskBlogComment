from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from flask_wtf.file import FileAllowed, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flaskface.Models import User
from flaskface.constant.app_constant import Constants


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=25)])
    username = StringField('User Name', validators=[DataRequired(), Length(min=2, max=15)])
    email = StringField('Email', validators=[DataRequired(), Length(min=2, max=25), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=25)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(f"{Constants.USER_ALREADY_EXIST}")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(f"{Constants.EMAIL_ALREADY_EXIST}")


class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField('Login')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(f"{Constants.FIRST_REGISTER_EMAIL}")


class AccountForm(FlaskForm):
    name = StringField(validators=[DataRequired(), Length(min=2, max=25)])
    username = StringField(validators=[DataRequired(), Length(min=2, max=25)])
    email = StringField(validators=[DataRequired(), Length(min=2, max=35), Email()])
    picture = FileField('Upload Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])

    update = SubmitField('Update')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(min=2, max=25), Email()])
    submit = SubmitField('Request Reset Password')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError


class RequestPasswordForm(FlaskForm):
    password = StringField('Password', validators=[DataRequired(), Length(min=2, max=25), Email()])
    confirm_password = StringField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Reset Password')
