from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField, FileField, PasswordField, EmailField, SubmitField, IntegerField, HiddenField
from wtforms.validators import DataRequired, length, equal_to
from flask_wtf.file import FileField, FileAllowed, FileSize, FileRequired

class PostFrom(FlaskForm):
    title = StringField(validators=[DataRequired()])
    comment = TextAreaField()
    post_pic = FileField(validators=[FileAllowed(["png", "jpg","webp","svg"])])
    submit = SubmitField("Create")
    
class SignupForm(FlaskForm):
    name = StringField()
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired(), length(min=8, max=20)])
    submit = SubmitField("SIGN UP")

    
class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField("LOG IN")

class PostCommentForm(FlaskForm):
    sub = StringField("Subtitle of your Comment")
    text = TextAreaField(validators=[DataRequired()])
    submit = SubmitField("SUBMIT")
    
class LikeForm(FlaskForm):
    like = SubmitField("Like")
    post_id = IntegerField("post_id")