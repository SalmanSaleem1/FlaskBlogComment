from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, InputRequired
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import TextAreaField, TextField, SubmitField, StringField


class NewPostForm(FlaskForm):
    title = TextField('Title', validators=[DataRequired(), Length(min=5, max=50)])
    content = TextAreaField('Content', validators=[DataRequired()])
    image_file = FileField('Upload Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Post')


class AddCommentForm(FlaskForm):
    body = StringField("Comments", validators=[InputRequired()])
    submit = SubmitField("Post")
