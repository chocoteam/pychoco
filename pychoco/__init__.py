"""
pychoco - Python API for the Choco Constraint Programming solver
"""

# Implementation inspired by https://github.com/d-michail/python-jgrapht

import atexit
import os
import sys

# On Windows (Python 3.8+), DLL search paths are no longer inherited from the
# loading module's directory. Register the package directory explicitly and
# pre-load choco_capi.dll so that all its transitive dependencies are resolved
# before _backend.pyd is imported.
if sys.platform == 'win32':
    import ctypes as _ctypes
    _pkg_dir = os.path.dirname(os.path.abspath(__file__))
    # Store the handle: if it were GC'd the directory would leave the search path.
    _dll_dir = os.add_dll_directory(_pkg_dir)
    # Explicitly load the native library.  If this fails it raises a clear
    # OSError (e.g. "[WinError 126] module not found") rather than the
    # misleading "circular import" error that Python 3.11+ would otherwise show.
    _choco_dll = _ctypes.CDLL(os.path.join(_pkg_dir, 'choco_capi.dll'))
    del _ctypes, _pkg_dir

from . import backend

backend.chocosolver_init()
del backend


def _module_cleanup_function():
    from . import backend
    backend.chocosolver_cleanup()


atexit.register(_module_cleanup_function)
del atexit

from .model import Model
from .objects.graphs.undirected_graph import create_undirected_graph, create_complete_undirected_graph
from .objects.graphs.directed_graph import create_directed_graph, create_complete_directed_graph
from .objects.automaton.finite_automaton import FiniteAutomaton
from .objects.automaton.cost_automaton import CostAutomaton
from .objects.graphs.multivalued_decision_diagram import MultivaluedDecisionDiagram
