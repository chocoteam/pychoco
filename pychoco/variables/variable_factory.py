from abc import ABC, abstractmethod
from typing import Union, List

from pychoco.variables.intvar import IntVar


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

    # Boolean variables #

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

    # Task variables #

    @abstractmethod
    def task(self, start: IntVar, duration: Union[int, IntVar], end: Union[None, IntVar] = None):
        """
        Creates a task container, based on a starting time `start`, a duration `duration`, and
        optionally an ending time `end`, such that: `start` + `duration` = `end`.

        A call to ensure_bound_consistency() is required before launching the resolution,
        this will not be done automatically.

        :param start: The starting time (IntVar).
        :param duration: The duration (int or IntVar).
        :param end: The ending time (IntVar, or None).
        :return: A task container.
        """
        pass

    # Set variables

    @abstractmethod
    def setvar(self, lb_or_value: set, ub: Union[set, None] = None, name: Union[str, None] = None):
        """
        Creates a set variable taking its domain in [lb, ub], or a a constant setvar if ub is None.
        For instance [{0,3},{-2,0,2,3}] means the variable must include both 0 and 3 and can additionally include -2
        and 2.

        :param lb_or_value: Initial domain lower bound (contains mandatory elements that should be present in
            every solution). If ub is None, corresponds to the constant value of this variable.
        :param ub: Initial domain upper bound (contains potential elements)
        :param name: Name of the variable (optional).
        :return: A SetVar.
        """
        pass
