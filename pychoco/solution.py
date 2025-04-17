from pychoco import backend
from pychoco._handle_wrapper import _HandleWrapper
from pychoco._utils import get_int_array


class Solution(_HandleWrapper):
    """
    Solution to a Choco problem. This object can be used to retrieve the value of variables in the solution.
    """

    def __init__(self, handle):
        """
        Warning: Not intended to be used by users, use a Model object to instantiate constraints instead.
        """
        super().__init__(handle)

    def get_int_val(self, x: "IntVar"):
        """
        The value of the IntVar `x` in this solution.
        :param x: An IntVar.
        :return: The value of `x` in this solution.
        """
        return backend.get_int_val(self._handle, x._handle)

    def get_set_val(self, s: "SetVar"):
        """
        The value of the SetVar `s` in this solution.
        :param s: A SetVar.
        :return: The value of `s` in this solution.
        """
        val_handle = backend.get_set_val(self._handle, s._handle)
        val = get_int_array(val_handle)
        return set(val)

    def __repr__(self):
        return "Choco Solution"
