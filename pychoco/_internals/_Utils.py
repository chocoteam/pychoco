from pychoco import backend


def make_int_array(*ints):
    """
    Creates a Java int[] handler from a list of Python ints
    :param intvars: A list of Python IntVars
    :return: A Java int[] handler.
    """
    ints_array = backend.create_int_array(len(ints))
    for i in range(0, len(ints)):
        backend.int_array_set(ints_array, ints[i], i)
    return ints_array


def make_int_var_array(*intvars):
    """
    Creates a Java IntVar[] handler from a list of Python IntVars
    :param intvars: A list of Python IntVars
    :return: A Java IntVar[] handler.
    """
    vars_array = backend.create_intvar_array(len(intvars))
    for i in range(0, len(intvars)):
        backend.intvar_array_set(vars_array, intvars[i].handle, i)
    return vars_array
