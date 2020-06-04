# -*- coding: utf-8 -*-

"""Access endpoints.
"""
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from ordnung.presentation.views import (
    index, login, logout, month, register,
    restore, unauthorized, restore_note,
    register_note, restore_confirm, register_confirm,
)

routes = [
    # regular

    Route('/', index),
    Route('/month', month),
    # Route('/day', day),

    # CRUD --------------------------------------------------------------------

    # usage

    # Route('/add_record/{chosen_date}', show_record, methods=['GET']),
    # Route('/add_record/{chosen_date}', ajax_create_record, methods=['PUT']),

    # Route('/show_record/{chosen_date}/{record_id}', show_record, methods=['GET']),
    # Route('/show_record/{chosen_date}/{record_id}', ajax_update_record, methods=['PATCH']),
    # Route('/show_record/{chosen_date}/{record_id}', ajax_delete_record, methods=['DELETE']),
    # auth --------------------------------------------------------------------
    Route('/login', login),
    Route('/logout', logout, methods=['GET', 'POST']),

    Route('/register', register, methods=['GET', 'POST']),
    Route('/register_note', register_note),
    Route('/register_confirm/{token}', register_confirm),

    Route('/restore', restore, methods=['GET', 'POST']),
    Route('/restore_note', restore_note),
    Route('/restore_confirm/{token}',
          restore_confirm, methods=['GET', 'POST']),

    Route('/unauthorized', unauthorized),

    # static ------------------------------------------------------------------

    Mount('/static',
          app=StaticFiles(directory='ordnung/presentation/static'),
          name='static'),
]
