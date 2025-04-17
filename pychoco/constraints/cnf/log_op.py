from typing import List, Union

from pychoco import backend
from pychoco._handle_wrapper import _HandleWrapper
from pychoco._utils import make_logical_array
from pychoco.variables.boolvar import BoolVar


class LogOp(_HandleWrapper):
    """
    Logical operator, to ease clause definition
    """

    def __init__(self, handle: "SwigPyObject"):
        super().__init__(handle)


def and_op(*logops: List[Union[LogOp, BoolVar]]):
    """
    Create a conjunction, results in true if all of its operands are true.
    :param logops: A list of LogOp/Boolvar.
    """
    if len(logops) == 1 and isinstance(logops[0], list):
        logs = logops[0]
    else:
        logs = logops
    list_handle = make_logical_array(logs)
    handle = backend.and_op(list_handle)
    return LogOp(handle)


def if_only_if_op(a: Union[LogOp, BoolVar], b: Union[LogOp, BoolVar]):
    """
    Create a biconditional, results in true if and only if both operands are false or both operands are true.
    :param a: operand (LogOp/Boolvar).
    :param b: operand (LogOp/Boolvar).
    """
    handle = backend.if_only_if_op(a._handle, b._handle)
    return LogOp(handle)


def if_then_else_op(a: Union[LogOp, BoolVar], b: Union[LogOp, BoolVar], c: Union[LogOp, BoolVar]):
    """
    Create an implication, results in true if a is true` and b is true or a is false and c is true.
    :param a: operand (LogOp/Boolvar).
    :param b: operand (LogOp/Boolvar).
    :param c: operand (LogOp/Boolvar).
    """
    handle = backend.if_then_else_op(a._handle, b._handle, c._handle)
    return LogOp(handle)


def implies_op(a: Union[LogOp, BoolVar], b: Union[LogOp, BoolVar]):
    """
    Create an implication, results in true if a is false or b is true.
    :param a: operand (LogOp/Boolvar).
    :param b: operand (LogOp/Boolvar).
    """
    handle = backend.implies_op(a._handle, b._handle)
    return LogOp(handle)


def reified_op(b: BoolVar, tree: Union[LogOp, BoolVar]):
    """
    create a logical connection between ``b`` and ``tree``.
    :param b: A BoolVar.
    :param tree: operand (LogOp/Boolvar).
    """
    handle = backend.reified_op(b._handle, tree._handle)
    return LogOp(handle)


def or_op(*logops: List[Union[LogOp, BoolVar]]):
    """
    Create a disjunction, results in true whenever one or more of its operands are true.
    :param logops: A list of LogOp/Boolvar.
    """
    if len(logops) == 1 and isinstance(logops[0], list):
        logs = logops[0]
    else:
        logs = logops
    list_handle = make_logical_array(logs)
    handle = backend.or_op(list_handle)
    return LogOp(handle)


def nand_op(*logops: List[Union[LogOp, BoolVar]]):
    """
    Create an alternative denial, results in if at least one of its operands is false.
    :param logops: A list of LogOp/Boolvar.
    """
    if len(logops) == 1 and isinstance(logops[0], list):
        logs = logops[0]
    else:
        logs = logops
    list_handle = make_logical_array(logs)
    handle = backend.nand_op(list_handle)
    return LogOp(handle)


def nor_op(*logops: List[Union[LogOp, BoolVar]]):
    """
    Create a joint denial, results in `true` if all of its operands are false.
    :param logops: A list of LogOp/Boolvar.
    """
    if len(logops) == 1 and isinstance(logops[0], list):
        logs = logops[0]
    else:
        logs = logops
    list_handle = make_logical_array(logs)
    handle = backend.nor_op(list_handle)
    return LogOp(handle)


def xor_op(a: Union[LogOp, BoolVar], b: Union[LogOp, BoolVar]):
    """
    Create an exclusive disjunction, results in true whenever both operands differ.
    :param a: operand (LogOp/Boolvar).
    :param b: operand (LogOp/Boolvar).
    """
    handle = backend.xor_op(a._handle, b._handle)
    return LogOp(handle)
