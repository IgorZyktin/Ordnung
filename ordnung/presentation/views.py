# -*- coding: utf-8 -*-

"""Views.
"""
from itertools import chain

from starlette.authentication import requires
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from ordnung import settings
from ordnung.core.access import check_token, token_is_too_old
from ordnung.core.date_and_time import get_offset_dates, form_month
from ordnung.core.localisation import get_day_names
from ordnung.presentation.access import (
    get_date, get_gettext, get_translate
)
from ordnung.presentation.email_sending import (
    send_restore_email, send_verification_email
)
from ordnung.presentation.forms import PasswordRestoreForm, RegisterForm
from ordnung.presentation.rendering import render_template
from ordnung.storage.access import (
    get_user_by_email_or_login, change_user_password,
    confirm_registration, register_user,
)
from ordnung.storage.database import get_records


async def index(request: Request) -> RedirectResponse:
    """Starting page.
    """
    if request.user.is_authenticated:
        return RedirectResponse(request.url_for('month'))
    return RedirectResponse(request.url_for('login'))


async def login(request: Request) -> HTMLResponse:
    """Login page.
    """
    if request.user.is_authenticated:
        return RedirectResponse(request.url_for('index'))

    _ = get_gettext(request.user.lang)

    context = {
        'request': request,
        'header': _('You may gain access only after login'),
        'retry': _('Try log in once again'),
        'register': _('Register'),
        'restore': _('Restore password'),
    }
    return render_template(
        "login.html", context, status_code=401,
        headers={"WWW-Authenticate": 'Basic realm="Ordnung"'}
    )


@requires('authenticated', redirect='unauthorized')
async def month(request: Request) -> HTMLResponse:
    """Main page, navigation starts from here. Shows single month.
    """
    current_date = get_date(request)
    _ = get_translate(request.user.lang)

    (leap_back, step_back,
     step_forward, leap_forward) = get_offset_dates(current_date)

    records = get_records(target_date=current_date,
                          offset_left=settings.MONTH_OFFSET,
                          offset_right=settings.MONTH_OFFSET)

    tasks = get_records(target_date=current_date,
                        offset_left=0,
                        offset_right=2)
    context = {
        'request': request,
        'header': _(f'month_{current_date.month}') + f' ({current_date})',
        'month': form_month(current_date),
        'records': records,
        'tasks': tasks,  # FIXME
        'menu_is_visible': int(request.query_params.get('menu', '0')),
        'current_date': current_date,
        'day_names': get_day_names(request.user.lang),
        'leap_back_url': f'/month?date={leap_back}',
        'step_back_url': f'/month?date={step_back}',
        'step_forward_url': f'/month?date={step_forward}',
        'leap_forward_url': f'/month?date={leap_forward}',
    }
    return render_template('month.html', context)


# @requires('authenticated', redirect='unauthorized')
# async def day(request: Request):
#     """Single day navigation.
#     """
#     lang = get_lang(request)
#     current_date = get_date(request)
#     header = translate(lang,
#                        f'month_{current_date.month}') + f' ({current_date})'
#     tasks = get_records(target_date=current_date,
#                         offset_left=0,
#                         offset_right=0)
#     context = {
#         'request': request,
#         'header': header,
#         'current_date': current_date,
#         'month_url': f'/month?date={current_date}',
#         'tasks': tasks[str(current_date)]
#     }
#     return render_template("day.html", context)


# async def show_record(request: Request):
#     """Single record modification or creation.
#     """
#     at_date = extract_date(request)
#     #     chosen_date_str, chosen_date = extract_date(request)
#     #     record_id = request.path_params.get('record_id')
#     #     record, sub_context = get_or_create_record(record_id, chosen_date_str, request.user)
#     #
#     context = {
#         'request': request,
#         #         'creator_name': request.user.name,
#         #         'chosen_date': chosen_date,
#         #         'chosen_date_str': chosen_date_str,
#         #         'record': record,
#         #         **sub_context,
#         #         **request.state.context_extensions,
#     }
#     return HTMLResponse(f'day - {at_date}')


async def register(request: Request):
    """Register page.
    """
    if request.user.is_authenticated:
        return RedirectResponse(request.url_for('index'))

    _ = get_gettext(request.user.lang)
    form = await request.form()
    form = RegisterForm(form)

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
            errors = [_('Login "{login}" '
                        'is already in use').format(login=form.login.data)]
    else:
        errors = chain(*form.errors.values())

    context = {
        'request': request,
        'header': 'Registration',
        'form': form,
        'errors': errors,
        'retry': _('Go to login page'),
    }
    return render_template("register.html", context)


async def register_note(request: Request):
    """Register page. Message about e-mail confirmation.
    """
    _ = get_gettext(request.user.lang)

    email = request.session.get('email_for_confirm', '')
    if email:
        header = _('Confirmation link was '
                   'sent to "{email}"').format(email=email)
    else:
        header = _("You haven't asked for registration")

    context = {
        'request': request,
        'header': header,
        'retry': _("Go to login page"),
    }
    return render_template("login_note.html", context)


async def register_confirm(request: Request):
    """Registration confirmation page.
    """
    _ = get_gettext(request.user.lang)
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
        'retry': _("Go to login page"),
        'errors': errors,
    }
    return render_template("login_note.html", context)


async def restore(request: Request):
    """Password restore page.
    """
    errors = []
    _ = get_gettext(request.user.lang)
    user_contact = ''
    if request.method == 'POST':
        form = await request.form()

        if (user_contact := form.get('user_contact')) is None:
            errors = ['User contact information required']

        elif (user := get_user_by_email_or_login(user_contact)) is None:
            errors = ['There is no user with supplied contact information']

        elif send_restore_email(request, user.id, user.email):
            request.session['email_for_restore'] = user.email
            return RedirectResponse(request.url_for('restore_note'),
                                    status_code=303)
        else:
            errors = [_('Credentials are correct, but we could not send you '
                        'confirmation email. Please try again later.')]

    context = {
        'request': request,
        'user_contact': user_contact,
        'header': _('Enter your email or login'),
        'retry': _('Go to login page'),
        'errors': errors,
    }
    return render_template("restore.html", context)


async def restore_note(request: Request):
    """Password restore page (just message about email).
    """
    _ = get_gettext(request.user.lang)

    email = request.session.get('email_for_restore', '')
    if email:
        header = _('Password restore link was '
                   'sent to "{email}"').fomat(email=email)
    else:
        header = _("You haven't asked for password restore")

    context = {
        'request': request,
        'header': header,
        'retry': _("Go to login page"),
    }
    return render_template("login_note.html", context)


async def restore_confirm(request: Request):
    """Password restore page (actual form).
    """
    _ = get_gettext(request.user.lang)
    token = request.path_params.get('token')
    sig_okay, payload = check_token(token, 'restore_password')

    form = await request.form()
    form = PasswordRestoreForm(form)

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
        'retry': _('Go to login page'),
        'form': form,
        'sig_okay': sig_okay,
        'errors': errors,
    }
    return render_template('restore_password.html', context)


async def unauthorized(request: Request) -> HTMLResponse:
    """When user is not yet authorised but tries to get something.
    """
    _ = get_gettext(request.user.lang)

    context = {
        'request': request,
        'header': _('You have no access to this resource'),
        'retry': _('Go to login page'),
    }
    return render_template('unauthorized.html', context, status_code=403)


@requires('authenticated', redirect='unauthorized')
async def logout(request: Request) -> HTMLResponse:
    """Logout page.
    """
    _ = get_gettext(request.user.lang)

    context = {
        'request': request,
        'header': _('You have been successfully logged out'),
        'retry': _('Go to login page'),
    }
    return render_template('login_note.html', context, status_code=401)
