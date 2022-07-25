"""
pychoco - Python API for the Choco Constraint Programming solver
"""

# Implementation inspired by https://github.com/d-michail/python-jgrapht

import atexit

from . import backend
from ._internals._Model import _create_model

backend.chocosolver_init()
del backend


def _module_cleanup_function():
    from . import backend
    backend.chocosolver_init()


atexit.register(_module_cleanup_function)
del atexit


def create_model(name):
    """
    Create a Choco model.
    :param name: The name of the model.
    :return: A Choco model.
    """
    return _create_model(name)
