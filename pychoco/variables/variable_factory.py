from abc import ABC, abstractmethod
from typing import Union, List


class VariableFactory(ABC):
    """
    Factory for creating variables.
    """

    # Integer variables #

    @abstractmethod
    def intvar(self, lb: int, ub: Union[int, None] = None, name: Union[str, None] = None):
        """
        Creates an intvar.
        :param lb: Lower bound (integer).
        :param ub: upper bound (integer). If None: the variable is a constant equals to lb.
        :param name: The name of the intvar (automatically given if None).
        :return: An intvar.
        """
        pass

    @abstractmethod
    def intvars(self, size: int, lb: Union[List[int], int], ub: Union[int, None] = None, name: Union[str, None] = None):
        """
        Creates a list of intvars.
        :param size: Number of intvars.
        :param lb: Lower bound (integer). If lb is a list of ints, constant variables are created.
        :param ub: upper bound (integer). If None: the variable is a constant equals to lb.
        :param name: Prefix name of the intvars (automatically given if None).
        :return: A list of intvars.
        """
        pass

    @abstractmethod
    def boolvar(self, value: Union[bool, None] = None, name: Union[str, None] = None):
        """
        Creates a boolvar.
        :param value: If not None, a fixed value for the variable (which is thus a constant).
        :param name: The name of the variable (optional).
        :return: A boolvar.
        """
        pass

    @abstractmethod
    def boolvars(self, size: int, value: Union[List[bool], bool, None] = None, name: Union[str, None] = None):
        """
        Creates a list of boolvars.
        :param size: Number of boolvars.
        :param value: If not None, a fixed value for the variables (which is thus a constant). This value is either
                      the same for all variables (bool), or given as a list of bools.
        :param name: The name of the variable (optional).
        :return: A list of boolvars.
        """
        pass
