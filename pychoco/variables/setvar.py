from typing import Union

from pychoco import backend
from pychoco._internals._handle_wrapper import _HandleWrapper
from pychoco._internals._utils import make_int_array, get_int_array
from pychoco._internals._variable import _Variable


class SetVar(_Variable, _HandleWrapper):
    """
    A Set Variable is defined by a domain which is a set interval [lb, ub], where:
    lb is the set of integers that must belong to every single solution.
    ub is the set of integers that may belong to at least one solution.
    In the context of SetVars, a value of the variable is a set of integers.
    """

    def __init__(self, model: "_Model", lb_or_value: set, ub: Union[set, None] = None, name: Union[str, None] = None):
        """
        SetVar constructor.

        :param model: A Choco Model.
        :param lb_or_value: A set of integers, representing either the lower bound, or the value if the
        variable is a constant (in this case ub must be None).
        :param ub: A set of integers representing the upper bound, or None if the variable is a constant.
        :param name: The name of the setvar (optional).
        """
        lb_handle = make_int_array(list(lb_or_value))
        if ub is None:
            if name is None:
                handle = backend.setvar_iv(model.handle, lb_handle)
            else:
                handle = backend.setvar_s_iv(model.handle, name, lb_handle)
        else:
            ub_handle = make_int_array(list(ub))
            if name is None:
                handle = backend.setvar_iviv(model.handle, lb_handle, ub_handle)
            else:
                handle = backend.setvar_s_iviv(model.handle, lb_handle, ub_handle)
        super().__init__(handle, model)

    def get_lb(self):
        """
        :return: The lower bound of this setvar (a set of integers).
        """
        return set(get_int_array(backend.get_setvar_lb(self.handle)))

    def get_ub(self):
        """
        :return: The upper bound of this setvar (a set of integers).
        """
        return set(get_int_array(backend.get_setvar_ub(self.handle)))

    def get_value(self):
        """
        :return: The value of this set variable (only valid if it is instantiated).
        """
        return set(get_int_array(backend.get_setvar_value(self.handle)))

    def __repr__(self):
        return "Choco SetVar ('" + self.name + "')"
