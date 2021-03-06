# -*- coding: utf-8 -*-

"""Application forms.
"""
from starlette.requests import Request
from wtforms import (
    PasswordField, SelectField, StringField, HiddenField,
    BooleanField, TextAreaField, Form
)
from wtforms.csrf.session import SessionCSRF
from wtforms.fields.html5 import EmailField
from wtforms.meta import DefaultMeta
from wtforms.validators import Length, DataRequired, EqualTo

from ordnung import settings
from ordnung.core.localisation import gettext
from ordnung.presentation.access import get_gettext, get_lang


async def get_form(request: Request, form_type: type, obj=None):
    """Shorthand for form creation.
    """
    form = await request.form()
    form = form_type(formdata=form,
                     obj=obj,
                     lang=get_lang(request),
                     meta={'csrf_context': request.session})
    return form


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
        print(string)
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
            field.label.text = gettext(lang, field.label.text) + ':'


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
        'New password',
        validators=[
            DataRequired(),
            Length(min=4, max=100)
        ]
    )
    password_repeat = PasswordField(
        'Repeat new password',
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
        'Displayed name',
        validators=[DataRequired(), Length(min=2, max=30)])
    login = StringField(
        'Login',
        validators=[DataRequired(), Length(min=2, max=30)])
    email = EmailField(
        'E-mail',
        validators=[DataRequired(), Length(min=3, max=50)]
    )
    language = SelectField(
        'Language',
        validators=[DataRequired()],
        choices=[('RU', 'Русский'), ('EN', 'English')]
    )
    password = PasswordField(
        'New password',
        validators=[DataRequired(), Length(min=4, max=100)]
    )
    password_repeat = PasswordField(
        'Repeat new password',
        validators=[DataRequired(), Length(min=4, max=100),
                    EqualTo('password')]
    )


class GoalForm(OrdnungForm):
    """Goal creating and altering form.
    """
    id = HiddenField()
    user_id = HiddenField()

    title = StringField('Title')
    description = TextAreaField('Description')
    group = SelectField('Goal group')

    target_date = StringField('Target date')
    target_time = SelectField('Target time')
    persistence = SelectField('Persistence')
    status = SelectField('Status')

    created = StringField('Goal created at')
    last_edit = StringField('Goal last edit at')

    start_time = StringField('Start time')
    end_time = StringField('End time')

    has_metric = BooleanField('Has measurable metric?', default='checked')
    metric_name = StringField('Metric name',
                              render_kw={'disabled': 'disabled'})
    metric_objective = StringField('Metric objective',
                                   render_kw={'disabled': 'disabled'})
    metric_step = StringField('Metric step',
                              render_kw={'disabled': 'disabled'})
