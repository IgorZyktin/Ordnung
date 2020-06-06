# -*- coding: utf-8 -*-

"""Application forms.
"""
from wtforms.csrf.session import SessionCSRF

from wtforms import Form, PasswordField, SelectField, StringField
from wtforms.validators import Length, DataRequired, EqualTo
from wtforms.fields.html5 import EmailField
from wtforms.meta import DefaultMeta

from ordnung import settings
from ordnung.core.localisation import gettext
from ordnung.presentation.access import get_gettext


class OrdnungFormTranslator:
    """Custom form translator.
    """
    def __init__(self, lang: str):
        """Initialize instance.
        """
        self.lang = lang
        self._gettext = get_gettext(self.lang)

    def gettext(self, string):
        """Custom gettext wrapper.
        """
        return self._gettext(string)

    def ngettext(self, singular, plural, n):
        """Not yet implemented.
        """
        raise NotImplementedError


class OrdnungMeta(DefaultMeta):
    """Custom metaclass.
    """

    def get_translations(self, form):
        """Custom translator getter, handles WTForms localisation cycle.
        """
        return OrdnungFormTranslator(form.lang)


class OrdnungForm(Form):
    """Custom form class that allows to handle localisation.
    """
    class Meta(OrdnungMeta):
        csrf = True
        csrf_secret = settings.SECRET_KEY.encode('utf-8')
        csrf_class = SessionCSRF

    def __init__(self, *args, lang: str, **kwargs):
        """Initialize instance.
        """
        self.lang = lang
        super().__init__(*args, **kwargs)
        for field in self._fields.values():
            field.label.text = gettext(lang, field.label.text)


class UserContactForm(OrdnungForm):
    """Form for user email or login on password restore procedure.
    """
    contact = StringField(
        '',
        validators=[DataRequired(), Length(min=2, max=30)])


class PasswordRestoreForm(OrdnungForm):
    """PasswordRestoreForm.
    """
    password = PasswordField(
        'New password:',
        validators=[
            DataRequired(),
            Length(min=4, max=100)
        ]
    )
    password_repeat = PasswordField(
        'Repeat new password:',
        validators=[
            DataRequired(),
            Length(min=4, max=100),
            EqualTo('password'),
        ]
    )


class RegisterForm(OrdnungForm):
    """Registration form.
    """
    username = StringField(
        'Displayed name:',
        validators=[DataRequired(), Length(min=2, max=30)])
    login = StringField(
        'Login:',
        validators=[DataRequired(), Length(min=2, max=30)])
    email = EmailField(
        'E-mail:',
        validators=[DataRequired(), Length(min=3, max=50)]
    )
    language = SelectField(
        'Language:',
        validators=[DataRequired()],
        choices=[('RU', 'Russian'), ('EN', 'English')]
    )
    password = PasswordField(
        'New password:',
        validators=[DataRequired(), Length(min=4, max=100)]
    )
    password_repeat = PasswordField(
        'Repeat new password:',
        validators=[DataRequired(), Length(min=4, max=100),
                    EqualTo('password')]
    )
