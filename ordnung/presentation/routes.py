# -*- coding: utf-8 -*-

"""Access endpoints.
"""
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

# from view.api import ajax_update_record, ajax_delete_record, ajax_create_record
from ordnung.presentation.views import index, login, logout, show_month, register, restore, \
    unauthorized, show_day

routes = [
    # regular
    Route('/', index),

    # auth
    Route('/login', login, methods=['GET', 'POST']),
    Route('/logout', logout, methods=['GET', 'POST']),
    Route('/register', register, methods=['GET', 'POST']),
    Route('/restore', restore, methods=['GET', 'POST']),
    Route('/unauthorized', unauthorized),

    # usage
    Route('/show_month/{at_date}', show_month),
    # Route('/add_record/{chosen_date}', show_record, methods=['GET']),
    # Route('/add_record/{chosen_date}', ajax_create_record, methods=['PUT']),

    Route('/show_day/{chosen_date}', show_day),

    # Route('/show_record/{chosen_date}/{record_id}', show_record, methods=['GET']),
    # Route('/show_record/{chosen_date}/{record_id}', ajax_update_record, methods=['PATCH']),
    # Route('/show_record/{chosen_date}/{record_id}', ajax_delete_record, methods=['DELETE']),

    # static files
    Mount('/static', app=StaticFiles(directory='ordnung/presentation/static'), name='static'),
]
