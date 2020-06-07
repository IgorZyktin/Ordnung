# -*- coding: utf-8 -*-

"""Views.
"""
from itertools import chain

from starlette.authentication import requires
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from ordnung import settings
from ordnung.core.access import check_token, token_is_too_old
from ordnung.core.date_and_time import get_offset_dates, get_month
from ordnung.core.localisation import get_day_names
from ordnung.presentation.access import (
    get_date, get_gettext, get_translate, get_errors, get_lang
)
from ordnung.presentation.email_sending import (
    send_restore_email, send_verification_email
)
from ordnung.presentation.forms import PasswordRestoreForm, RegisterForm, \
    UserContactForm, GoalForm
from ordnung.presentation.rendering import render_template
from ordnung.storage.access import (
    get_user_by_email_or_login, change_user_password,
    confirm_registration, register_user,
)


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

    _ = get_gettext(get_lang(request))

    context = {
        'request': request,
        'header': _('You could get access only after login'),
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
    _ = get_translate(get_lang(request))

    (leap_back, step_back,
     step_forward, leap_forward) = get_offset_dates(current_date)

    context = {
        'request': request,
        'header': _(f'month_{current_date.month}') + f' ({current_date})',
        'month': get_month(current_date),
        'menu_is_visible': int(request.query_params.get('menu', '0')),
        'current_date': current_date,
        'day_names': get_day_names(get_lang(request)),
        'leap_back_url': f'/month?date={leap_back}',
        'step_back_url': f'/month?date={step_back}',
        'step_forward_url': f'/month?date={step_forward}',
        'leap_forward_url': f'/month?date={leap_forward}',
    }
    return render_template('month.html', context)


@requires('authenticated', redirect='unauthorized')
async def day(request: Request):
    """Single day navigation.
    """
    _ = get_translate(get_lang(request))
    current_date = get_date(request)
    # tasks = get_records(target_date=current_date,
    #                     offset_left=0, offset_right=0)
    context = {
        'request': request,
        'header': _(f'month_{current_date.month}') + f' ({current_date})',
        'current_date': current_date,
        'month_url': f'/month?date={current_date}',
        'tasks': []
    }
    return render_template("day.html", context)


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

async def create_goal(request: Request):
    """Create new goal.
    """
    form = await request.form()
    lang = get_lang(request)
    _ = get_gettext(lang)
    form = GoalForm(form, lang=lang, meta={'csrf_context': request.session})
    errors = get_errors(lang, form.errors)

    context = {
        'request': request,
        'header': _('Create new goal'),
        'form': form,
        'errors': errors,
        'back': _('Back to month'),
    }
    return render_template('create_goal.html', context)


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


async def unauthorized(request: Request) -> HTMLResponse:
    """When user is not yet authorised but tries to get something.
    """
    _ = get_gettext(get_lang(request))

    context = {
        'request': request,
        'header': _('You have no access to this resource'),
        'retry': _('To the start page'),
    }
    return render_template('unauthorized.html', context, status_code=403)


@requires('authenticated', redirect='unauthorized')
async def logout(request: Request) -> HTMLResponse:
    """Logout page.
    """
    _ = get_gettext(get_lang(request))

    context = {
        'request': request,
        'header': _('You have been successfully logged out'),
        'retry': _('To the start page'),
    }
    return render_template('login_note.html', context, status_code=401)
