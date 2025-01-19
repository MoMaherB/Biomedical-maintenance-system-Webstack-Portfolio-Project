from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from maintenance_system.models import User


class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(message='Please Enter valid email address!')])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')],)
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data.strip()).first()
        if user:
            raise ValidationError('This username already taken. Please choose another one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.strip()).first()
        if user:
            raise ValidationError('This email already taken. Please choose another one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Please Enter valid email address!')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
