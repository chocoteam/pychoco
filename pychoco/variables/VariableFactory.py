from abc import ABC, abstractmethod


class VariableFactory(ABC):
    """
    Factory for creating variables.
    """

    # Integer variables #

    @abstractmethod
    def intvar(self, lb, ub, name=None):
        """
        Creates an intvar from a lower and an upper bound.
        :param lb: Lower bound (integer).
        :param ub: upper bound (integer).
        :param name: The name of the intvar (automatically given if None).
        :return: An intvar.
        """
        pass
