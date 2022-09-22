from abc import ABC, abstractmethod
from typing import List

import backend
from _utils import make_boolvar_array, make_intvar_array, make_int_array, make_setvar_array, get_boolvar_array
from variables.boolvar import BoolVar
from variables.intvar import IntVar
from variables.setvar import SetVar


class ViewFactory(ABC):
    """
    Factory for creating views.
    """

    @property
    @abstractmethod
    def handle(self):
        pass

    # Boolean views

    def bool_not_view(self, boolvar: BoolVar):
        """
        Creates a boolean view over boolvar holding the logical negation of boolvar.
        :param boolvar: A BoolVar.
        :return: A bool_not_view.
        """
        handle = backend.bool_not_view(boolvar.handle)
        return BoolVar(handle, self)

    def set_bool_view(self, setvar: SetVar, value: int):
        """
        Creates a boolean view b over a set variable setvar such that:
        given value an integer, b = true iff setvar contains value.

        :param setvar: A SetVar.
        :param value: An int.
        :return: A set_bool_view
        """
        handle = backend.set_bool_view(setvar.handle, value)
        return BoolVar(handle, self)

    def set_bools_view(self, setvar: SetVar, size: int, offset: int = 0):
        """
        Creates an array of boolean views b over a set variable setvar such that:
        b[i - offset] = true <=> i in setvar.

        :param setvar: A SetVar.
        :param size: An int, size of the boolean view to return.
        :param offset: An int.
        :return: A list of boolean views.
        """
        handle = backend.set_bools_view(setvar.handle, size, offset)
        boolvars = get_boolvar_array(handle, self)
        return boolvars

    # Integer views

    def int_offset_view(self, intvar: IntVar, offset: int):
        """
        Creates a view based on intvar, equal to intvar + offset.

        :param intvar: An IntVar.
        :param offset: An int.
        :return: An int_offset_view.
        """
        handle = backend.int_offset_view(intvar.handle, offset)
        return IntVar(handle, self)

    def int_minus_view(self, intvar: IntVar):
        """
        Creates a view over intvar equal to -intvar. That is if intvar = [a,b], then int_minus_view(intvar) = [-b,-a].
        :param intvar: An IntVar.
        :return: An int_minus_view.
        """
        handle = backend.int_minus_view(intvar.handle)
        return IntVar(handle, self)

    def int_scale_view(self, intvar: IntVar, scale: int):
        """
        Creates a view over intvar equal to intvar * scale
        Requires scale > -2
        - if scale < -1, throws an exception;
        - if scale = -1, returns a minus view;
        - if scale = 0, returns a fixed variable;
        - if scale = 1, returns intvar;
        - otherwise, returns a scale view.

        :param intvar: An IntVar.
        :param scale: An int.
        :return: An int_scale_view.
        """
        assert scale > -2, "[int_scale_view] scale must be > -2"
        handle = backend.int_scale_view(intvar.handle, scale)
        return IntVar(handle, self)

    def int_abs_view(self, intvar: IntVar):
        """
        Creates a view over intvar such that: | intvar |.
        - if intvar is already instantiated, returns a fixed variable;
        - if the lower bound of intvar is greater or equal to 0, returns intvar;
        - if the upper bound of intvar is less or equal to 0, return a minus view;
        - otherwise, returns an absolute view.

        :param intvar: An IntVar.
        :return: An int_abs_view
        """
        handle = backend.int_abs_view(intvar.handle)
        return IntVar(handle, self)

    def int_affine_view(self, a: int, intvar: IntVar, b: int):
        """
        Creates an affine view over intvar such that: a * intvar + b.

        :param a: An int.
        :param intvar: An IntVar.
        :param b: An int.
        :return: An int_affine_view.
        """
        handle = backend.int_affine_view(a, intvar.handle, b)
        return IntVar(handle, self)

    def int_eq_view(self, intvar: IntVar, value: int):
        """
        Creates a boolean view over intvar such that: intvar == c.

        :param intvar: An IntVar.
        :param value:  An int.
        :return:  An int_eq_view.
        """
        handle = backend.int_eq_view(intvar.handle, value)
        return BoolVar(handle, self)

    def int_ne_view(self, intvar: IntVar, value: int):
        """
        Creates a boolean view over intvar such that: intvar != c.

        :param intvar: An IntVar.
        :param value:  An int.
        :return:  An int_ne_view.
        """
        handle = backend.int_ne_view(intvar.handle, value)
        return BoolVar(handle, self)

    def int_le_view(self, intvar: IntVar, value: int):
        """
        Creates a boolean view over intvar such that: intvar <= c.

        :param intvar: An IntVar.
        :param value:  An int.
        :return:  An int_le_view.
        """
        handle = backend.int_le_view(intvar.handle, value)
        return BoolVar(handle, self)

    def int_ge_view(self, intvar: IntVar, value: int):
        """
        Creates a boolean view over intvar such that: intvar >= c.

        :param intvar: An IntVar.
        :param value:  An int.
        :return:  An int_ge_view.
        """
        handle = backend.int_ge_view(intvar.handle, value)
        return BoolVar(handle, self)

    # Set views

    def bools_set_view(self, boolvars: List[BoolVar], offset: int = 0):
        """
        Create a set view over an array of boolean variables defined such that:
        boolvars[x - offset] = True <=> x in set view.
        This view is equivalent to the set_bools_channeling constraint.

        :param boolvars: A list of BoolVar.
        :param offset: An int.
        :return: A bools_set_view.
        """
        bools_handle = make_boolvar_array(boolvars)
        handle = backend.bools_set_view(bools_handle, offset)
        return SetVar(handle, self)

    def ints_set_view(self, intvars: List[IntVar], values: List[int], offset: int = 0):
        """
        Create a set view over an array of integer variables, such that:
        intvars[x - offset] = value[x - offset] <=> x in set view.

        :param intvars: A list of IntVars.
        :param values: A list of ints.
        :param offset: An int.
        :return: An ints_set_view.
        """
        assert len(intvars) == len(values), "[ints_set_view] 'intvars' and 'values' must have the same length"
        vars_handle = make_intvar_array(intvars)
        values_handle = make_int_array(values)
        handle = backend.ints_set_view(vars_handle, values_handle, offset)
        return SetVar(handle, self)

    def set_union_view(self, setvars: List[SetVar]):
        """
        Creates a set view representing the union of a list of set variables.

        :param setvars: A list of SetVars.
        :return: A set_union_view.
        """
        vars_handle = make_setvar_array(setvars)
        handle = backend.set_union_view(vars_handle)
        return SetVar(handle, self)

    def set_intersection_view(self, setvars: List[SetVar]):
        """
        Creates a set view representing the intersection of a list of set variables.

        :param setvars: A list of SetVars.
        :return: A set_intersection_view.
        """
        vars_handle = make_setvar_array(setvars)
        handle = backend.set_intersection_view(vars_handle)
        return SetVar(handle, self)

    def set_difference_view(self, setvar_1: SetVar, setvar_2: SetVar):
        """
        Creates a set view representing the set difference between setvar_1 and setvar_2:  setvar_1 \ setvar_2.

        :param setvar_1: A SetVar.
        :param setvar_2: A SetVar.
        :return: A set_difference_view.
        """
        handle = backend.set_difference_view(setvar_1.handle, setvar_2.handle)
        return SetVar(handle, self)
