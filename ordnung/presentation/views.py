# -*- coding: utf-8 -*-

"""Regular views.
"""
from itsdangerous import URLSafeSerializer
from starlette.authentication import requires
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from ordnung import settings
from ordnung.core.access import get_monotonic
from ordnung.core.date_and_time import get_offset_dates, form_month
from ordnung.core.localisation import translate, get_day_names, gettext
from ordnung.presentation.access import get_date, get_lang, send_restore_link, \
    change_user_password
from ordnung.presentation.rendering import render_template, extract_date
from ordnung.storage.access import get_user_by_email_or_login
from ordnung.storage.database import get_records

HTTP_OK = 200
HTTP_POST_REDIRECT_GET = 303
HTTP_UNAUTHORIZED = 401
HTTP_FORBIDDEN = 403


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

    lang = get_lang(request)

    context = {
        'request': request,
        'lang': lang,
        'header': gettext(lang, "You may gain access only after login"),
        'retry': gettext(lang, "Try log in once again"),
        'register': gettext(lang, "Register"),
        'restore': gettext(lang, "Restore password"),
        'errors': {},
    }
    return render_template(
        "login.html", context, status_code=HTTP_UNAUTHORIZED,
        headers={"WWW-Authenticate": 'Basic realm="Ordnung"'}
    )


@requires('authenticated', redirect='unauthorized')
async def month(request: Request) -> HTMLResponse:
    """Main page, navigation starts from here. Shows single month.
    """
    lang = get_lang(request)
    current_date = get_date(request)
    header = translate(lang,
                       f'month_{current_date.month}') + f' ({current_date})'

    (leap_back,
     step_back,
     step_forward,
     leap_forward) = get_offset_dates(current_date)

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
        'lang': lang,
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
        'lang': lang,
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
    # if request.user.is_authenticated:
    #     return RedirectResponse(request.url_for('index'))
    #
    # errors = {}
    # form = await request.form()
    #
    # if request.method == 'POST':
    #     if not (errors := registration_form_is_invalid(form)):
    #         register_new_user('s')
    #         send_verification_email()
    #         return RedirectResponse(request.url_for('register_confirm'),
    #                                 status_code=HTTP_POST_REDIRECT_GET)
    #
    # context = {
    #     'request': request,
    #     'header': translate(request.user.namespace, 'generic', '$register'),
    #     'entered_name': form.get('username', ''),
    #     'entered_login': form.get('login', ''),
    #     'entered_email': form.get('email', ''),
    #     'errors': errors,
    # }
    # return render_template("register.html", context)
    raise


# TODO
async def register_confirm(request: Request):
    """Register page. Message about e-mail confirmation.
    """
    errors = []
    lang = get_lang(request)
    context = {
        'request': request,
        'lang': lang,
        'header': gettext(lang,
                          'Password confirm link was sent to %(email)s'),
        'retry': gettext(lang, "Try log in once again"),
        'index_url': request.url_for('index'),
        'errors': errors,
    }
    return render_template("restore_note.html", context)


async def restore(request: Request):
    """Password restore page.
    """
    errors = []
    lang = get_lang(request)
    user_contact = ''
    if request.method == 'POST':
        form = await request.form()

        if not (user_contact := form.get('user_contact')):
            errors = ['укажи хоть что нибудь']

        elif (user := get_user_by_email_or_login(user_contact)) is not None:
            restore_url = send_restore_link(request, user.id, user.email)
            request.session['email_for_restore'] = user.email
            request.session['restore_url'] = restore_url  # FIXME
            return RedirectResponse(request.url_for('restore_note'),
                                    status_code=HTTP_POST_REDIRECT_GET)
        else:
            errors = [f'нет пользователя с конктктом {user_contact}']

    context = {
        'request': request,
        'lang': lang,
        'user_contact': user_contact,
        'header': gettext(lang, 'Enter your email or login'),
        'errors': errors,
    }
    return render_template("restore.html", context)


async def restore_note(request: Request):
    """Password restore page (just message about email).
    """
    errors = []
    lang = get_lang(request)

    email = request.session.get('email_for_restore', '')
    if email:
        header = gettext(lang, 'Password restore link was sent to %(email)s')
        header = header % dict(email=email)
    else:
        header = 'Вы не запрашивали смену пароля.'

    context = {
        'request': request,
        'lang': lang,
        'header': header,
        'retry': gettext(lang, "Try log in once again"),
        'index_url': request.url_for('index'),
        'x': request.session['restore_url'],
        'errors': errors,
    }
    return render_template("restore_note.html", context)


async def restore_password(request: Request):
    """Password restore page (actual form).
    """
    errors = []
    lang = get_lang(request)
    auth_s = URLSafeSerializer(settings.SECRET_KEY, salt="restore_password")
    token = request.path_params.get('token')
    sig_okay, payload = auth_s.loads_unsafe(token)
    print(payload)
    if not sig_okay:
        header = 'вы не можете восстановить пароль'
    else:
        delta = get_monotonic() - payload['monotonic']
        if delta > settings.MAX_PASSWORD_RESTORE_INTERVAL:
            header = 'ссылка восстановления пароля протухла'
            sig_okay = False
        else:
            header = 'password restore'

    if sig_okay and request.method == 'POST':
        form = await request.form()
        password_1 = form.get('password_1')
        password_2 = form.get('password_2')
        if password_1 != password_2:
            errors = ['Пароли не совпадают']
        elif change_user_password(payload['user_id'], password_1):
            return RedirectResponse(request.url_for('login'),
                                    status_code=HTTP_POST_REDIRECT_GET)
        else:
            errors = ['не удалось']

    context = {
        'request': request,
        'header': header,
        'retry': gettext(lang, "Try log in once again"),
        'index_url': request.url_for('index'),
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
        'lang': lang,
        'header': gettext(lang, "You have no access to this resource"),
        'retry': gettext(lang, "Try log in once again"),
        'index_url': request.url_for('index'),
        'errors': {},
    }
    return render_template("unauthorized.html", context,
                           status_code=HTTP_FORBIDDEN)


@requires('authenticated', redirect='unauthorized')
async def logout(request: Request) -> HTMLResponse:
    """Logout page.
    """
    lang = get_lang(request)

    context = {
        'request': request,
        'lang': lang,
        'header': gettext(lang, "You have been successfully logged out"),
        'retry': gettext(lang, "Try log in once again"),
        'index_url': request.url_for('index'),
        'errors': {},
    }
    return render_template("logout.html", context,
                           status_code=HTTP_UNAUTHORIZED)
