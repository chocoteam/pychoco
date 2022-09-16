"""
pychoco - Python API for the Choco Constraint Programming solver
"""

# Implementation inspired by https://github.com/d-michail/python-jgrapht

import atexit
import os
import sys
from ctypes import cdll
from typing import Union, List

if sys.platform.startswith('win32'):
    path = os.path.dirname(__file__)
    if sys.version_info[1] >= 8:
        os.add_dll_directory(path)
    cdll.LoadLibrary(os.path.join(path, "choco_capi.dll"))

from . import backend
from ._internals._cost_automaton import _create_cost_automaton
from ._internals._cost_automaton import _make_multi_resources
from ._internals._cost_automaton import _make_single_resource
from ._internals._finite_automaton import _create_finite_automaton
from ._internals._model import _create_model
from .objects.automaton.finite_automaton import FiniteAutomaton
from .variables.intvar import IntVar

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


def create_cost_automaton(automaton: Union[FiniteAutomaton, None] = None):
    """
    Create a cost automaton (for regular constraints).

    :param automaton: Another automaton (optional).
    :return: A cost automaton object.
    """
    return _create_cost_automaton(automaton)


def make_single_resource(automaton: FiniteAutomaton, costs: Union[List[List[int]], List[List[List[int]]]], inf: int,
                         sup: int):
    """
    :param automaton: A finite automaton.
    :param costs: Costs (2 or 3 dimensional int matrix).
    :param inf: Lower bound.
    :param sup: Upper bound.
    :return: A cost automaton from a finite automaton and costs.
    """
    return _make_single_resource(automaton, costs, inf, sup)


def make_multi_resources(automaton: FiniteAutomaton, costs: Union[List[List[List[int]]], List[List[List[List[int]]]]],
                         bounds: List[IntVar]):
    """
    :param automaton: A finite automaton.
    :param costs: Costs (3 or 4 dimensional int matrix).
    :param bounds: List of IntVars defining bounds.
    :return: A multi cost automaton from a finite automaton and costs.
    """
    return _make_multi_resources(automaton, costs, bounds)
