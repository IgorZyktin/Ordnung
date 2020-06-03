# -*- coding: utf-8 -*-

"""Regular views.
"""
from itertools import chain

from starlette.authentication import requires
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from ordnung import settings
from ordnung.core.access import (
    check_token, token_is_too_old
)
from ordnung.core.date_and_time import get_offset_dates, form_month
from ordnung.core.localisation import translate, get_day_names, gettext
from ordnung.presentation.access import (
    get_date, get_lang, send_restore_email,
    send_verification_email, url_for
)
from ordnung.presentation.forms import PasswordRestoreForm, RegisterForm
from ordnung.presentation.rendering import render_template, extract_date
from ordnung.storage.access import (
    get_user_by_email_or_login, change_user_password,
    confirm_registration, register_new_user,
)
from ordnung.storage.database import get_records


async def index(request: Request) -> RedirectResponse:
    """Starting page.
    """
    if request.user.is_authenticated:
        return RedirectResponse(url_for(request, 'month'))
    return RedirectResponse(url_for(request, 'login'))


async def login(request: Request) -> HTMLResponse:
    """Login page.
    """
    if request.user.is_authenticated:
        return RedirectResponse(url_for(request, 'index'))

    lang = get_lang(request)

    context = {
        'request': request,
        'header': gettext(lang, "You may gain access only after login"),
        'retry': gettext(lang, "Try log in once again"),
        'register': gettext(lang, "Register"),
        'restore': gettext(lang, "Restore password"),
    }
    return render_template("login.html", context, status_code=401,
                           headers={"WWW-Authenticate": 'Basic '
                                                        'realm="Ordnung"'})


@requires('authenticated', redirect='unauthorized')
async def month(request: Request) -> HTMLResponse:
    """Main page, navigation starts from here. Shows single month.
    """
    lang = get_lang(request)
    current_date = get_date(request)
    header = translate(lang,
                       f'month_{current_date.month}') + f' ({current_date})'

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
        'header': header,
        'month': form_month(current_date),
        'records': records,
        'tasks': tasks,  # FIXME
        'menu_is_visible': int(request.query_params.get('menu', '0')),
        'current_date': current_date,
        'day_names': get_day_names(lang),
        'leap_back_url': f'/month?date={leap_back}',
        'step_back_url': f'/month?date={step_back}',
        'step_forward_url': f'/month?date={step_forward}',
        'leap_forward_url': f'/month?date={leap_forward}',
    }
    print(context['records'])
    return render_template("month.html", context)


@requires('authenticated', redirect='unauthorized')
async def day(request: Request):
    """Single day navigation.
    """
    lang = get_lang(request)
    current_date = get_date(request)
    header = translate(lang,
                       f'month_{current_date.month}') + f' ({current_date})'
    tasks = get_records(target_date=current_date,
                        offset_left=0,
                        offset_right=0)
    context = {
        'request': request,
        'header': header,
        'current_date': current_date,
        'month_url': f'/month?date={current_date}',
        'tasks': tasks[str(current_date)]
    }
    return render_template("day.html", context)


async def show_record(request: Request):
    """Single record modification or creation.
    """
    at_date = extract_date(request)
    #     chosen_date_str, chosen_date = extract_date(request)
    #     record_id = request.path_params.get('record_id')
    #     record, sub_context = get_or_create_record(record_id, chosen_date_str, request.user)
    #
    context = {
        'request': request,
        #         'creator_name': request.user.name,
        #         'chosen_date': chosen_date,
        #         'chosen_date_str': chosen_date_str,
        #         'record': record,
        #         **sub_context,
        #         **request.state.context_extensions,
    }
    return HTMLResponse(f'day - {at_date}')


async def register(request: Request):
    """Register page.
    """
    if request.user.is_authenticated:
        return RedirectResponse(url_for(request, 'index'))

    lang = get_lang(request)
    form = await request.form()
    form = RegisterForm(form)

    if request.method == 'POST' and form.validate():
        new_user_id = register_new_user(form)

        if new_user_id:
            if send_verification_email(request, new_user_id, form.email.data):
                request.session['email_for_confirm'] = form.email.data
                return RedirectResponse(url_for(request, 'register_note'),
                                        status_code=303)
            else:
                errors = [gettext(lang, 'Something bad happened '
                                        'during registration confirmation')]
        else:
            errors = [gettext(lang, f'Login "{form.login.data}" '
                                    f'is already in use')]
    else:
        errors = chain(*form.errors.values())

    context = {
        'request': request,
        'header': 'Registration',
        'form': form,
        'errors': errors,
        'retry': gettext(lang, "Go to login page"),
    }
    return render_template("register.html", context)


async def register_note(request: Request):
    """Register page. Message about e-mail confirmation.
    """
    lang = get_lang(request)

    email = request.session.get('email_for_confirm', '')
    if email:
        header = gettext(lang, 'Confirmation link was sent to %(email)s')
        header = header % dict(email=email)
    else:
        header = gettext(lang, "You haven't asked for registration")

    context = {
        'request': request,
        'header': header,
        'retry': gettext(lang, "Go to login page"),
    }
    return render_template("login_note.html", context)


async def register_confirm(request: Request):
    """Registration confirmation page.
    """
    errors = []
    token = request.path_params.get('token')
    sig_okay, payload = check_token(token, 'confirm_registration')

    lang = get_lang(request)

    if not sig_okay:
        header = gettext(lang, 'Confirmation link seems to be incorrect')

    elif token_is_too_old(payload):
        header = gettext(lang, 'Confirmation link seems to be outdated')
        sig_okay = False

    else:
        if confirm_registration(payload['user_id']):
            header = gettext(lang, 'Registration confirmed')

        else:
            header = gettext(lang, 'Registration is not confirmed')
            errors = [gettext(lang, 'Something bad happened '
                                    'during registration confirmation')]

    context = {
        'request': request,
        'header': header,
        'retry': gettext(lang, "Go to login page"),
        'sig_okay': sig_okay,
        'errors': errors
    }
    return render_template("login_note.html", context)


async def restore(request: Request):
    """Password restore page.
    """
    errors = []
    lang = get_lang(request)
    user_contact = ''
    if request.method == 'POST':
        form = await request.form()

        if not (user_contact := form.get('user_contact')):
            errors = ['User contact information required']

        elif (user := get_user_by_email_or_login(user_contact)) is not None:
            if send_restore_email(request, user.id, user.email):
                request.session['email_for_restore'] = user.email
                return RedirectResponse(url_for(request, 'restore_note'),
                                        status_code=303)

            errors = [gettext(lang, 'Something bad happened '
                                    'during restoring email delivery')]
        else:
            errors = ['There is no user with supplied contact information']

    context = {
        'request': request,
        'user_contact': user_contact,
        'header': gettext(lang, 'Enter your email or login'),
        'retry': gettext(lang, "Go to login page"),
        'errors': errors,
    }
    return render_template("restore.html", context)


async def restore_note(request: Request):
    """Password restore page (just message about email).
    """
    lang = get_lang(request)

    email = request.session.get('email_for_restore', '')
    if email:
        header = gettext(lang, 'Password restore link was sent to %(email)s')
        header = header % dict(email=email)
    else:
        header = gettext(lang, "You haven't asked for password restore")

    context = {
        'request': request,
        'header': header,
        'retry': gettext(lang, "Go to login page"),
    }
    return render_template("login_note.html", context)


async def restore_confirm(request: Request):
    """Password restore page (actual form).
    """
    token = request.path_params.get('token')
    sig_okay, payload = check_token(token, 'restore_password')

    lang = get_lang(request)

    form = await request.form()
    form = PasswordRestoreForm(form)
    form.password.label.text = gettext(lang, 'New password')
    form.password_repeat.label.text = gettext(lang, 'Repeat new password')

    if not sig_okay:
        header = gettext(lang, 'Password restore link seems to be incorrect')

    elif token_is_too_old(payload):
        header = gettext(lang, 'Password restore link seems to be outdated')
        sig_okay = False

    else:
        header = gettext(lang, 'Password restore')

    if sig_okay and request.method == 'POST' and form.validate():

        if change_user_password(payload['user_id'], form.password.data):
            return RedirectResponse(url_for(request, 'login'),
                                    status_code=303)
        errors = [gettext(lang, 'Something bad happened '
                                'during password change')]
    else:
        errors = chain(*form.errors.values())

    context = {
        'request': request,
        'header': header,
        'retry': gettext(lang, "Go to login page"),
        'form': form,
        'sig_okay': sig_okay,
        'errors': errors,
    }
    return render_template("restore_password.html", context)


async def unauthorized(request: Request) -> HTMLResponse:
    """When user is not yet authorised but tries to get something.
    """
    lang = get_lang(request)

    context = {
        'request': request,
        'header': gettext(lang, "You have no access to this resource"),
        'retry': gettext(lang, "Go to login page"),
    }
    return render_template("unauthorized.html", context, status_code=403)


@requires('authenticated', redirect='unauthorized')
async def logout(request: Request) -> HTMLResponse:
    """Logout page.
    """
    lang = get_lang(request)

    context = {
        'request': request,
        'header': gettext(lang, "You have been successfully logged out"),
        'retry': gettext(lang, "Go to login page"),
    }
    return render_template("login_note.html", context, status_code=401)
