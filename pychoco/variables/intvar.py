from abc import abstractmethod, ABC

from pychoco.variables.variable import Variable


class IntVar(Variable, ABC):
    """
    An integer variable (IntVar) is an unknown whose value should be an integer.
    Therefore, the domain of an integer variable is a set of integers (representing
    possible values). This set of integers can be either represented by an interval
    (with a lower bound and an upper bound), or enumerated.
    """

    @abstractmethod
    def get_lb(self):
        """
        :return: The lower bound of the variable.
        """
        pass

    @abstractmethod
    def get_ub(self):
        """
        :return: The upper bound of the variable.
        """
        pass

    def __repr__(self):
        return "Choco IntVar ('" + self.name + "')"
