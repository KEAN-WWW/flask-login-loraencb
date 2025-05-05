from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            InputRequired(),
            Email(message='Invalid email address'),
            Length(max=128)
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            InputRequired()
        ]
    )
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            InputRequired(),
            Email(message='Invalid email address'),
            Length(max=128)
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            InputRequired(),
            Length(min=6)
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            InputRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    submit = SubmitField('Register')