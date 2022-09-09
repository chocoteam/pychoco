"""
pychoco - Python API for the Choco Constraint Programming solver
"""

# Implementation inspired by https://github.com/d-michail/python-jgrapht

import atexit
from typing import Union, List

from . import backend
from ._internals._cost_automaton import _create_cost_automaton
from ._internals._finite_automaton import _create_finite_automaton, _FiniteAutomaton
from ._internals._model import _create_model

backend.chocosolver_init()
del backend


def _module_cleanup_function():
    from . import backend
    backend.chocosolver_init()


atexit.register(_module_cleanup_function)
del atexit


def create_model(name: str = None):
    """
    Create a Choco model.
    
    :param name: The name of the model (optional)
    :return: A Choco model.
    """
    return _create_model(name)


def create_finite_automaton(regexp: Union[str, None] = None, bounds: Union[List[int], None] = None):
    """
    Create a finite automaton (for regular constraints).

    :param regexp: A regexpt describing the automaton (optional).
    :param bounds: [min, max] (optional).
    :return: A finite automaton object.
    """
    return _create_finite_automaton(regexp, bounds)


def create_cost_automaton(automaton: Union[_FiniteAutomaton, None] = None):
    """
    Create a cost automaton (for regular constraints).

    :param automaton: Another automaton (optional).
    :return: A cost automaton object.
    """
    return _create_cost_automaton(automaton)
