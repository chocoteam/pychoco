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

from .model import Model
from .objects.graphs.undirected_graph import create_undirected_graph, create_complete_undirected_graph
from .objects.graphs.directed_graph import create_directed_graph, create_complete_directed_graph
from .objects.automaton.finite_automaton import FiniteAutomaton
from .objects.automaton.cost_automaton import CostAutomaton
from .objects.graphs.multivalued_decision_diagram import MultivaluedDecisionDiagram
