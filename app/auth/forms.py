from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    """User Login Form"""

    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Length(1, 64),
            Email()
        ]
    )

    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )

    remember_me = BooleanField('Keep me logged in')

    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    """User Registration Form"""

    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Length(1, 64),
            Email()
        ]
    )

    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(1, 64),
            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                   'Usernames must have only letters'
                   ', numbers, dots or underscores')
        ]
    )

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            EqualTo('password2', message='Password must match.')
        ]
    )

    password2 = PasswordField(
        'Confirm password',
        validators=[DataRequired()]
    )

    submit = SubmitField('Register')

    def validate_email(self, field):
        """Validate Unique Email"""

        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Username already in use.')

    def validate_username(self, field):
        """Validate Unique Username"""

        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class ChangePasswordForm(FlaskForm):

    old_password = PasswordField(
        label='Old Password',
        validators=[DataRequired()]
    )

    password = PasswordField(
        label='New Password',
        validators=[
            DataRequired(),
            EqualTo('password2', message='Password must match.')
        ]
    )

    password2 = PasswordField(
        label='Confirm new password',
        validators=[DataRequired()]
    )

    submit = SubmitField('Update Password')


class PasswordResetRequestForm(FlaskForm):

    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Length(1, 64),
            Email()
        ]
    )
    submit = SubmitField('Reset Password')


class PasswordResetForm(FlaskForm):

    password = PasswordField(
        'New Password',
        validators=[
            DataRequired(),
            EqualTo('password2', message='Password must match')
        ]
    )

    password2 = PasswordField(
        'Confirm password',
        validators=[DataRequired()]
    )

    submit = SubmitField('Reset Password')


class ChangeEmailForm(FlaskForm):

    email = StringField(
        'New Email',
        validators=[
            DataRequired(),
            Length(1, 64),
            Email()
        ]
    )

    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )

    submit = SubmitField('Update Email Address')
