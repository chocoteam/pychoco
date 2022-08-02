from typing import List

from pychoco import backend
from pychoco._internals._solution import _Solution
from pychoco.solution import Solution
from pychoco.variables.intvar import IntVar


def make_int_array(*ints: List[int]):
    """
    Creates a Java int[] handle from a list of Python ints
    :param intvars: A list of Python ints
    :return: A Java int[] handle.
    """
    ints_array = backend.create_int_array(len(ints))
    for i in range(0, len(ints)):
        backend.int_array_set(ints_array, ints[i], i)
    return ints_array


def make_int_var_array(*intvars: List[IntVar]):
    """
    Creates a Java IntVar[] handle from a list of Python IntVars
    :param intvars: A list of Python IntVars
    :return: A Java IntVar[] handle.
    """
    vars_array = backend.create_intvar_array(len(intvars))
    for i in range(0, len(intvars)):
        backend.intvar_array_set(vars_array, intvars[i].handle, i)
    return vars_array


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
