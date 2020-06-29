# -*- coding: utf-8 -*-

"""Access endpoints.
"""
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from ordnung.views import index, login, logout, unauthorized
from ordnung.views import create_goal, update_goal
from ordnung.views import month, day
from ordnung.views import (
    restore_confirm, register_confirm, restore_note,
    register_note, restore, register
)

GP = ['GET', 'POST']

routes = [

    # main --------------------------------------------------------------------

    Route('/month', month),
    Route('/month/{date}', month),
    Route('/day/{date}', day),

    # auth --------------------------------------------------------------------

    Route('/', index),
    Route('/login', login),
    Route('/logout', logout, methods=GP),
    Route('/unauthorized', unauthorized),

    # register-----------------------------------------------------------------

    Route('/register', register, methods=GP),
    Route('/register_note', register_note),
    Route('/register_confirm/{token}', register_confirm),

    Route('/restore', restore, methods=GP),
    Route('/restore_note', restore_note),
    Route('/restore_confirm/{token}', restore_confirm, methods=GP),

    # CRUD --------------------------------------------------------------------

    Route('/create_goal', create_goal, methods=GP),
    Route('/create_goal/{date}', create_goal, methods=GP),
    Route('/update_goal/{goal_id}', update_goal, methods=GP),

    # static ------------------------------------------------------------------

    Mount('../static',
          app=StaticFiles(directory='ordnung/presentation/static'),
          name='static'),
]
