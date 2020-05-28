# -*- coding: utf-8 -*-

"""Access endpoints.
"""
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from ordnung.presentation.views import (
    index, login, logout, month, register, restore,
    unauthorized, day, restore_note, register_confirm, restore_password
)

routes = [
    # regular
    Route('/', index),

    # auth
    Route('/login', login, methods=['GET', 'POST']),
    Route('/logout', logout, methods=['GET', 'POST']),
    Route('/register', register, methods=['GET', 'POST']),
    Route('/register_confirm', register_confirm),

    Route('/restore', restore, methods=['GET', 'POST']),
    Route('/restore_note', restore_note),
    Route('/restore_password', restore_password, methods=['GET', 'POST']),

    Route('/unauthorized', unauthorized),

    # usage
    Route('/month', month),
    Route('/day', day),

    # Route('/add_record/{chosen_date}', show_record, methods=['GET']),
    # Route('/add_record/{chosen_date}', ajax_create_record, methods=['PUT']),

    # Route('/show_record/{chosen_date}/{record_id}', show_record, methods=['GET']),
    # Route('/show_record/{chosen_date}/{record_id}', ajax_update_record, methods=['PATCH']),
    # Route('/show_record/{chosen_date}/{record_id}', ajax_delete_record, methods=['DELETE']),

    # static files
    Mount('/static', app=StaticFiles(directory='ordnung/presentation/static'), name='static'),
]
