from abc import ABC, abstractmethod


class Solver(ABC):
    """
    Solution to a Choco problem. This object can be used to retrieve the value of variables in the solution.
    """

    @abstractmethod
    def get_int_val(self, x):
        """
        The value of the IntVar `x` in this solution.
        :param x: An IntVar.
        :return: The value of `x` in this solution.
        """
        pass

    def __repr__(self):
        return "Choco Solution"
