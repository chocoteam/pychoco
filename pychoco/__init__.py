"""
pychoco - Python API for the Choco Constraint Programming solver
"""

# Implementation inspired by https://github.com/d-michail/python-jgrapht

import atexit

from . import backend

backend.chocosolver_init()
del backend


def _module_cleanup_function():
    from . import backend
    backend.chocosolver_init()


atexit.register(_module_cleanup_function)
del atexit
