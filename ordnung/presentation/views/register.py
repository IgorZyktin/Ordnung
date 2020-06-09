# -*- coding: utf-8 -*-

"""Views.
"""
from itertools import chain

from starlette.requests import Request
from starlette.responses import RedirectResponse

from ordnung.core.access import check_token, token_is_too_old
from ordnung.presentation.access import get_gettext, get_lang, get_errors
from ordnung.presentation.email_sending import (
    send_verification_email, send_restore_email
)
from ordnung.presentation.forms import (
    RegisterForm, UserContactForm, PasswordRestoreForm
)
from ordnung.presentation.rendering import render_template
from ordnung.storage.access import (
    register_user, confirm_registration,
    get_user_by_email_or_login, change_user_password
)


async def register(request: Request):
    """Register page.
    """
    if request.user.is_authenticated:
        return RedirectResponse(request.url_for('index'))

    _ = get_gettext(get_lang(request))
    form = await request.form()
    form = RegisterForm(form,
                        lang=get_lang(request),
                        meta={'csrf_context': request.session})

    if request.method == 'POST' and form.validate():
        new_user_id = register_user(form.username, form.login, form.email,
                                    form.password, form.language)

        if new_user_id:
            if send_verification_email(request, new_user_id, form.email.data):
                request.session['email_for_confirm'] = form.email.data
                return RedirectResponse(request.url_for('register_note'),
                                        status_code=303)
            else:
                errors = [_('You were successfully registered, but for some '
                            'reasons we could not send you confirmation email.'
                            ' Please request for this email later.')]
        else:
            errors = [_('Login "%(login)s" '
                        'is already in use') % dict(login=form.login.data)]
    else:
        errors = get_errors(get_lang(request), form.errors)

    context = {
        'request': request,
        'header': _('Registration'),
        'form': form,
        'errors': errors,
        'retry': _('To the start page'),
    }
    return render_template('register.html', context)


async def register_note(request: Request):
    """Register page. Message about e-mail confirmation.
    """
    _ = get_gettext(get_lang(request))

    email = request.session.get('email_for_confirm', '')
    if email:
        header = _('Confirmation link was '
                   'sent to "%(email)s"') % dict(email=email)
    else:
        header = _("You haven't asked for registration")

    context = {
        'request': request,
        'header': header,
        'retry': _("To the start page"),
    }
    return render_template("login_note.html", context)


async def register_confirm(request: Request):
    """Registration confirmation page.
    """
    _ = get_gettext(get_lang(request))
    errors = []
    token = request.path_params.get('token')
    sig_okay, payload = check_token(token, 'confirm_registration')

    if not sig_okay:
        header = _('Confirmation link is incorrect')

    elif token_is_too_old(payload):
        header = _('Confirmation link is correct, but too old')
        sig_okay = False

    elif confirm_registration(payload['user_id']):
        header = _('Registration confirmed')

    else:
        header = _('Registration is not confirmed')
        errors = [_('Something bad happened '
                    'during registration confirmation')]

    context = {
        'request': request,
        'header': header,
        'sig_okay': sig_okay,
        'retry': _("To the start page"),
        'errors': errors,
    }
    return render_template("login_note.html", context)


async def restore(request: Request):
    """Password restore page.
    """
    errors = []
    _ = get_gettext(get_lang(request))

    form = await request.form()
    form = UserContactForm(form,
                           lang=get_lang(request),
                           meta={'csrf_context': request.session})

    if request.method == 'POST':
        if (user := get_user_by_email_or_login(form.contact.data)) is None:
            errors = [_('There is no user with supplied contact information.')]

        elif send_restore_email(request, user.id, user.email):
            request.session['email_for_restore'] = user.email
            return RedirectResponse(request.url_for('restore_note'),
                                    status_code=303)
        else:
            errors = [_('Credentials are correct, but we could not send you '
                        'confirmation email. Please try again later.')]

    context = {
        'request': request,
        'header': _('Enter your email or login'),
        'retry': _('To the start page'),
        'form': form,
        'errors': errors,
    }
    return render_template("restore.html", context)


async def restore_note(request: Request):
    """Password restore page (just message about email).
    """
    _ = get_gettext(get_lang(request))

    email = request.session.get('email_for_restore', '')
    if email:
        header = _('Password restore link was '
                   'sent to "%(email)s"') % dict(email=email)
    else:
        header = _("You haven't asked for password restore")

    context = {
        'request': request,
        'header': header,
        'retry': _("To the start page"),
    }
    return render_template("login_note.html", context)


async def restore_confirm(request: Request):
    """Password restore page (actual form).
    """
    _ = get_gettext(get_lang(request))
    token = request.path_params.get('token')
    sig_okay, payload = check_token(token, 'restore_password')

    form = await request.form()
    form = PasswordRestoreForm(form,
                               lang=get_lang(request),
                               meta={'csrf_context': request.session})

    if not sig_okay:
        header = _('Password restore link is incorrect')

    elif token_is_too_old(payload):
        header = _('Password restore link is correct but too old')
        sig_okay = False

    else:
        header = _('Password restore')

    if sig_okay and request.method == 'POST' and form.validate():
        if change_user_password(payload['user_id'], form.password.data):
            return RedirectResponse(request.url_for('login'),
                                    status_code=303)
        errors = [_('An error happened during password change. '
                    'Please try again later.')]
    else:
        errors = chain(*form.errors.values())

    context = {
        'request': request,
        'header': header,
        'retry': _('To the start page'),
        'form': form,
        'sig_okay': sig_okay,
        'errors': errors,
    }
    return render_template('restore_password.html', context)
