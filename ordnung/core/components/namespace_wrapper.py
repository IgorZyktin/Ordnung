# -*- coding: utf-8 -*-

"""Turns complex object into primitive namespace.
"""
from argparse import Namespace
from typing import Any


def simplify(something: Any):
    """Turns complex object into primitive namespace.
    """
    attrs = {
        key: value
        for key, value in vars(something).items()
        if key.isupper()
    }
    inst = Namespace(**attrs)
    return inst
