from pychoco import backend
from pychoco._handle_wrapper import _HandleWrapper
from pychoco.variables.intvar import IntVar


class Solution(_HandleWrapper):
    """
    Solution to a Choco problem. This object can be used to retrieve the value of variables in the solution.
    """

    def __init__(self, handle):
        """
        Warning: Not intended to be used by users, use a Model object to instantiate constraints instead.
        """
        super().__init__(handle)

    def get_int_val(self, x: IntVar):
        """
        The value of the IntVar `x` in this solution.
        :param x: An IntVar.
        :return: The value of `x` in this solution.
        """
        return backend.get_int_val(self.handle, x.handle)

    def __repr__(self):
        return "Choco Solution"
