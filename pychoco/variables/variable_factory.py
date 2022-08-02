from abc import ABC, abstractmethod
from typing import Union


class VariableFactory(ABC):
    """
    Factory for creating variables.
    """

    # Integer variables #

    @abstractmethod
    def intvar(self, lb: int, ub: int, name: Union[str, None] = None):
        """
        Creates an intvar from a lower and an upper bound.
        :param lb: Lower bound (integer).
        :param ub: upper bound (integer).
        :param name: The name of the intvar (automatically given if None).
        :return: An intvar.
        """
        pass

    @abstractmethod
    def boolvar(self, value: Union[bool, None] = None, name: Union[str, None] = None):
        """
        Creates a boolvar, possibly with a fixed value.
        :param value: If not None, a boolean to instantiate this variable with.
        :param name: The name of the variable (optional).
        :return: A boolvar.
        """
        pass
