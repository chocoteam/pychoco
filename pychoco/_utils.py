from typing import List, Union

from pychoco import backend

def make_int_array(ints: List[int]):
    """
    Creates a Java int[] handle from a list of Python ints
    :param ints: A list of Python ints
    :return: A Java int[] handle.
    """
    ints_array = backend.create_int_array(len(ints))
    for i in range(0, len(ints)):
        backend.int_array_set(ints_array, ints[i], i)
    return ints_array


def get_int_array(handle):
    """
    Return a Python int list from a Java int[] handle.
    :param handle: An int[] handle
    :return: A python int list.
    """
    array = []
    for i in range(0, backend.int_array_length(handle)):
        array.append(backend.int_array_get(handle, i))
    return array


def make_int_2d_array(arrays: List[List[int]]):
    """
    Creates a Java int[][] handle from a list of Python int lists.
    :param arrays: A 2d int matrix.
    :return: A Java int[][] handle.
    """
    int_2d_array = backend.create_int_2d_array(len(arrays))
    for i in range(0, len(arrays)):
        handle = make_int_array(arrays[i])
        backend.int_2d_array_set(int_2d_array, handle, i)
    return int_2d_array


def make_int_3d_array(arrays: List[List[List[int]]]):
    """
    Creates a Java int[][][] handle from a list of Python lists of lists of ints.
    :param arrays: A 3d int matrix.
    :return: A Java int[][][] handle.
    """
    int_3d_array = backend.create_int_3d_array(len(arrays))
    for i in range(0, len(arrays)):
        handle = make_int_2d_array(arrays[i])
        backend.int_3d_array_set(int_3d_array, handle, i)
    return int_3d_array


def make_int_4d_array(arrays: List[List[List[List[int]]]]):
    """
    Creates a Java int[][][][] handle from a list of Python lists of lists of ints.
    :param arrays: A 4d int matrix.
    :return: A Java int[][][][] handle.
    """
    int_4d_array = backend.create_int_4d_array(len(arrays))
    for i in range(0, len(arrays)):
        handle = make_int_3d_array(arrays[i])
        backend.int_4d_array_set(int_4d_array, handle, i)
    return int_4d_array


def make_intvar_array(intvars: List["IntVar"]):
    """
    Creates a Java IntVar[] handle from a list of Python IntVars
    :param intvars: A list of Python IntVars
    :return: A Java IntVar[] handle.
    """
    vars_array = backend.create_intvar_array(len(intvars))
    for i in range(0, len(intvars)):
        backend.intvar_array_set(vars_array, intvars[i]._handle, i)
    return vars_array


def make_intvar_2d_array(arrays: List[List["IntVar"]]):
    """
    Creates a Java IntVar[][] handle from a list of Python IntVar lists.
    :param arrays: A list of Intvar lists.
    :return: A Java IntVar[][] handle.
    """
    intvar_2d_array = backend.create_intvar_2d_array(len(arrays))
    for i in range(0, len(arrays)):
        handle = make_intvar_array(arrays[i])
        backend.intvar_2d_array_set(intvar_2d_array, handle, i)
    return intvar_2d_array


def make_boolvar_array(boolvars: List["BoolVar"]):
    """
    Creates a Java BoolVar[] handle from a list of Python BoolVars
    :param boolvars: A list of Python BoolVars
    :return: A Java BoolVars[] handle.
    """
    vars_array = backend.create_boolvar_array(len(boolvars))
    for i in range(0, len(boolvars)):
        backend.boolvar_array_set(vars_array, boolvars[i]._handle, i)
    return vars_array


def make_boolvar_2d_array(arrays: List[List["BoolVar"]]):
    """
    Creates a Java BoolVar[][] handle from a list of Python BoolVar lists.
    :param arrays: A list of BoolVar lists.
    :return: A Java BoolVar[][] handle.
    """
    boolvar_2d_array = backend.create_boolvar_2d_array(len(arrays))
    for i in range(0, len(arrays)):
        handle = make_boolvar_array(arrays[i])
        backend.boolvar_2d_array_set(boolvar_2d_array, handle, i)
    return boolvar_2d_array


def get_boolvar_array(handle, model):
    """
    Return a Python List[BoolVar] from a Java BoolVar[] handle.
    :param handle: A BoolVar[] handle.
    :param A Python model object.
    :return: A python BoolVar list.
    """
    from pychoco.variables.boolvar import BoolVar
    array = []
    for i in range(0, backend.array_length(handle)):
        var_handle = backend.intvar_array_get(handle, i)
        array.append(BoolVar(var_handle, model))
    return array


def make_setvar_array(setvars: List["SetVar"]):
    """
    Creates a Java SetVar[] handle from a list of Python SetVars
    :param setvars: A list of Python SetVars
    :return: A Java SetVar[] handle.
    """
    vars_array = backend.create_setvar_array(len(setvars))
    for i in range(0, len(setvars)):
        backend.setvar_array_set(vars_array, setvars[i]._handle, i)
    return vars_array


def make_graphvar_array(graphvars: List["GraphVar"]):
    """
    Creates a Java GraphVar[] handle from a list of Python GraphVars
    :param graphvars: A list of Python GraphVars
    :return: A Java GraphVar[] handle.
    """
    vars_array = backend.create_graphvar_array(len(graphvars))
    for i in range(0, len(graphvars)):
        backend.graphvar_array_set(vars_array, graphvars[i]._handle, i)
    return vars_array


def make_task_array(tasks: List["Task"]):
    """
    Creates a Java Task[] handle from a list of Python Tasks
    :param tasks: A list of Python Tasks
    :return: A Java Task[] handle.
    """
    task_array = backend.create_task_array(len(tasks))
    for i in range(0, len(tasks)):
        backend.task_array_set(task_array, tasks[i]._handle, i)
    return task_array


def make_constraint_array(constraints: List["Constraint"]):
    """
    Creates a Java Constraint[] handle from a list of Python Constraint
    :param constraints: A list of Python Constraint
    :return: A Java Constraint[] handle.
    """
    cons_array = backend.create_constraint_array(len(constraints))
    for i in range(0, len(constraints)):
        backend.constraint_array_set(cons_array, constraints[i]._handle, i)
    return cons_array


def make_criterion_var_array(criterion):
    """
    Creates a Java Criterion[] handler from a list of Criterion handles
    :param criterion: A list of Criterion handles
    :return: A Java Criterion[] handler.
    """
    criterion_array = backend.create_criterion_array(len(criterion))
    for i in range(0, len(criterion)):
        backend.criterion_array_set(criterion_array, criterion[i], i)
    return criterion_array


def make_supportable_array(sarray: List["Supportable"]):
    """
    Creates a Java ISupportable[] handler.
    """
    array = backend.create_isupportable_array(len(sarray))
    for i in range(0, len(sarray)):
        backend.isupportable_array_set(array, sarray[i]._handle, i)
    return array


def make_logical_array(logicals: List[Union["LogOp", "BoolVar"]]):
    """
    Creates a Java ILogical[] handler.
    """
    array = backend.create_ilogical_array(len(logicals))
    for i in range(0, len(logicals)):
        backend.ilogical_array_set(array, logicals[i]._handle, i)
    return array


def make_supportable_2d_array(arrays: List[List["Supportable"]]):
    """
    Creates a Java Supportable[][] handle.
    """
    array = backend.create_isupportable_2d_array(len(arrays))
    for i in range(0, len(arrays)):
        handle = make_supportable_array(arrays[i])
        backend.isupportable_2d_array_set(array, handle, i)
    return array


def extract_solutions(solution_list_handle) -> List["Solution"]:
    """
    Convert a Java List<Solution> handler into a Python list of Solutions.
    :param solution_list_handle: Java List<Solution> handle.
    :return: a list of Solutions.
    """
    from pychoco.solution import Solution
    solutions = list()
    size = backend.list_size(solution_list_handle)
    for i in range(0, size):
        sol_handle = backend.list_solution_get(solution_list_handle, i)
        solutions.append(Solution(sol_handle))
    return solutions
