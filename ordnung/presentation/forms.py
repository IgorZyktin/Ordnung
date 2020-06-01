# -*- coding: utf-8 -*-

"""Application forms.
"""
from wtforms import Form, PasswordField
from wtforms.validators import Length, DataRequired, EqualTo

v_length = Length(min=4, max=100, message='sdasd')
v_req = DataRequired(message='sda')


class PasswordRestoreForm(Form):
    """PasswordRestoreForm.
    """
    password = PasswordField('', validators=[v_req, v_length])
    password_repeat = PasswordField('', validators=[
        v_req, v_length, EqualTo('password', message='ppp')])
