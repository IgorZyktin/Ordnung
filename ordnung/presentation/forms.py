# -*- coding: utf-8 -*-

"""Application forms.
"""
from wtforms import Form, PasswordField, SelectField, StringField
from wtforms.validators import Length, DataRequired, EqualTo
from wtforms.fields.html5 import EmailField


class PasswordRestoreForm(Form):
    """PasswordRestoreForm.
    """
    password = PasswordField(
        'New password',
        validators=[
            DataRequired(message='Password is required'),
            Length(
                min=4,
                max=100,
                message='Password must be of 4 to 100 symbols long'
            )
        ]
    )
    password_repeat = PasswordField(
        'Repeat new password',
        validators=[
            DataRequired(message='Password repeat is required'),
            Length(
                min=4,
                max=100,
                message='Password repeat must be of 4 to 100 symbols long'
            ),
            EqualTo(
                'password',
                message='Password fields do not match'
            ),
        ]
    )


class RegisterForm(Form):
    """Registration form.
    """
    username = StringField(
        'Displayed name',
        validators=[
            DataRequired(message='Name is required'),
            Length(
                min=2,
                max=30,
                message='Name must be of 2 to 30 symbols long'
            ),
        ])
    login = StringField('Login', validators=[
        DataRequired(message='Login is required'),
        Length(
            min=2,
            max=30,
            message='Login must be of 2 to 30 symbols long'
        ),
    ])
    email = EmailField('E-mail', validators=[
        DataRequired(message='Login is required'),
        Length(
            min=3,
            max=50,
            message='E-mail must be of 3 to 50 symbols long'
        ),
    ])
    language = SelectField(
        'Language',
        validators=[DataRequired(message='Login is required')],
        choices=[('RU', 'Russian'), ('EN', 'English')]
    )
    password = PasswordField(
        'New password',
        validators=[
            DataRequired(message='Password is required'),
            Length(
                min=4,
                max=100,
                message='Password must be of 4 to 100 symbols long'
            ),
        ]
    )
    password_repeat = PasswordField(
        'Repeat new password',
        validators=[
            DataRequired(message='Password repeat is required'),
            Length(
                min=4,
                max=100,
                message='Password repeat must be of 4 to 100 symbols long'
            ),
            EqualTo(
                'password',
                message='Password fields do not match'
            ),
        ]
    )
