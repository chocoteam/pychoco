from pychoco import backend
from pychoco._handle_wrapper import _HandleWrapper
from pychoco.variables.variable import Variable


class IntVar(Variable, _HandleWrapper):
    """
    An integer variable (IntVar) is an unknown whose value should be an integer.
    Therefore, the domain of an integer variable is a set of integers (representing
    possible values). This set of integers can be either represented by an interval
    (with a lower bound and an upper bound), or enumerated.
    """

    def get_lb(self):
        """
        :return: The lower bound of the variable.
        """
        return backend.get_intvar_lb(self.handle)

    def get_ub(self):
        """
        :return: The upper bound of the variable.
        """
        return backend.get_intvar_ub(self.handle)

    def get_value(self):
        """
        :return: The value of the variable (only valid if it is instantiated).
        """
        return backend.get_intvar_value(self.handle)

    def get_type(self):
        return "IntVar"
