from typing import List

from pychoco import backend
from pychoco._internals._solution import _Solution
from pychoco.constraints.constraint import Constraint
from pychoco.solution import Solution
from pychoco.variables.boolvar import BoolVar
from pychoco.variables.intvar import IntVar


def make_int_array(*ints: List[int]):
    """
    Creates a Java int[] handle from a list of Python ints
    :param ints: A list of Python ints
    :return: A Java int[] handle.
    """
    ints_array = backend.create_int_array(len(ints))
    for i in range(0, len(ints)):
        backend.int_array_set(ints_array, ints[i], i)
    return ints_array


def make_int_array_array(*arrays: List[List[int]]):
    """
    Creates a Java int[][] handle from a list of Python int lists.
    :param arrays: A list of int lists.
    :return: A Java int[][] handle.
    """
    int_array_array = backend.create_int_array_array(len(arrays))
    for i in range(0, len(arrays)):
        handle = make_int_array(*arrays[i])
        backend.int_array_array_set(int_array_array, handle, i)
    return int_array_array


def make_intvar_array(*intvars: List[IntVar]):
    """
    Creates a Java IntVar[] handle from a list of Python IntVars
    :param intvars: A list of Python IntVars
    :return: A Java IntVar[] handle.
    """
    vars_array = backend.create_intvar_array(len(intvars))
    for i in range(0, len(intvars)):
        backend.intvar_array_set(vars_array, intvars[i].handle, i)
    return vars_array


def make_boolvar_array(*boolvars: List[BoolVar]):
    """
    Creates a Java BoolVar[] handle from a list of Python BoolVars
    :param intvars: A list of Python BoolVars
    :return: A Java BoolVars[] handle.
    """
    vars_array = backend.create_boolvar_array(len(boolvars))
    for i in range(0, len(boolvars)):
        backend.boolvar_array_set(vars_array, boolvars[i].handle, i)
    return vars_array


def make_constraint_array(*constraints: List[Constraint]):
    """
    Creates a Java Constraint[] handle from a list of Python Constraint
    :param intvars: A list of Python Constraint
    :return: A Java Constraint[] handle.
    """
    cons_array = backend.create_constraint_array(len(constraints))
    for i in range(0, len(constraints)):
        backend.constraint_array_set(cons_array, constraints[i].handle, i)
    return cons_array


def make_criterion_var_array(*criterion):
    """
    Creates a Java Criterion[] handler from a list of Criterion handles
    :param criterion: A list of Criterion handles
    :return: A Java Criterion[] handler.
    """
    criterion_array = backend.create_criterion_array(len(criterion))
    for i in range(0, len(criterion)):
        backend.criterion_array_set(criterion_array, criterion[i], i)
    return criterion_array


def extract_solutions(solution_list_handle) -> List[Solution]:
    """
    Convert a Java List<Solution> handler into a Python list of Solutions.
    :param solution_list_handle: Java List<Solution> handle.
    :return: a list of Solutions.
    """
    solutions = list()
    size = backend.list_size(solution_list_handle)
    for i in range(0, size):
        sol_handle = backend.list_solution_get(solution_list_handle, i)
        solutions.append(_Solution(sol_handle))
    return solutions
