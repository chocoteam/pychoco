from typing import List, Union

from pychoco.backend import create_int_array

from pychoco import backend
from pychoco._handle_wrapper import _HandleWrapper


class Supportable(_HandleWrapper):
    """
    Expression to be used in hybrid tuples
    """

    def __init__(self, handle: "SwigPyObject"):
        super().__init__(handle)


class SupportableCol(Supportable):

    def __init__(self, handle: "SwigPyObject"):
        super().__init__(handle)


def any_val():
    """
    Return an expression that indicates that no restriction exists on this column/variable.
    """
    handle = backend.any()
    return Supportable(handle)


def col(index: int):
    """
    Refer to a specific colum/variable.
    :param index: index of a column/variable position. The first column/variable has the index 0.
    """
    handle = backend.col(index)
    return SupportableCol(handle)


def eq(value: Union[int, SupportableCol], inc: int = 0):
    """
    Return an expression that ensures that the column/variable is equal to value.
    :param value An integer, or a column (`col(idx)` function).
    :param inc: If value refers to a column, value to be added or subtracted to col
    """
    if isinstance(value, SupportableCol):
        handle = backend.eq_col(value._handle, inc)
    else:
        handle = backend.eq(value)
    return Supportable(handle)


def ne(value: Union[int, SupportableCol], inc: int = 0):
    """
    Return an expression that ensures that the column/variable is different from value.
    :param value An integer, or a column (`col(idx)` function).
    :param inc: If value refers to a column, value to be added or subtracted to col
    """
    if isinstance(value, SupportableCol):
        handle = backend.ne_col(value._handle, inc)
    else:
        handle = backend.ne(value)
    return Supportable(handle)


def ge(value: Union[int, SupportableCol], inc: int = 0):
    """
    Return an expression that ensures that the column/variable is greater than or equal to value.
    :param value An integer, or a column (`col(idx)` function).
    :param inc: If value refers to a column, value to be added or subtracted to col
    """
    if isinstance(value, SupportableCol):
        handle = backend.ge_col(value._handle, inc)
    else:
        handle = backend.ge(value)
    return Supportable(handle)


def gt(value: Union[int, SupportableCol], inc: int = 0):
    """
    Return an expression that ensures that the column/variable is strictly greater than value.
    :param value An integer, or a column (`col(idx)` function).
    :param inc: If value refers to a column, value to be added or subtracted to col
    """
    if isinstance(value, SupportableCol):
        handle = backend.gt_col(value._handle, inc)
    else:
        handle = backend.gt(value)
    return Supportable(handle)


def le(value: Union[int, SupportableCol], inc: int = 0):
    """
    Return an expression that ensures that the column/variable is lesser than or equal to value.
    :param value An integer, or a column (`col(idx)` function).
    :param inc: If value refers to a column, value to be added or subtracted to col
    """
    if isinstance(value, SupportableCol):
        handle = backend.le_col(value._handle, inc)
    else:
        handle = backend.le(value)
    return Supportable(handle)


def lt(value: Union[int, SupportableCol], inc: int = 0):
    """
    Return an expression that ensures that the column/variable is strictly lesser than value.
    :param value An integer, or a column (`col(idx)` function).
    :param inc: If value refers to a column, value to be added or subtracted to col
    """
    if isinstance(value, SupportableCol):
        handle = backend.lt_col(value._handle, inc)
    else:
        handle = backend.lt(value)
    return Supportable(handle)


def in_values(values: List[int]):
    """
    Return an expression that ensures that the column/variable takes its value in values.
    :param values A list of ints.
    """
    values_handle = create_int_array(values)
    handle = backend.in_(values_handle)
    return Supportable(handle)


def not_in_values(values: List[int]):
    """
    Return an expression that ensures that the column/variable does not take its value in values.
    :param values A list of ints.
    """
    values_handle = create_int_array(values)
    handle = backend.nin(values_handle)
    return Supportable(handle)
