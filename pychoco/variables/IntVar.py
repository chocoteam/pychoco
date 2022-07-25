from abc import ABC, abstractmethod


class IntVar(ABC):
    """
    An integer variable (IntVar) is an unknown whose value should be an integer.
    Therefore, the domain of an integer variable is a set of integers (representing
    possible values). This set of integers can be either represented by an interval
    (with a lower bound and an upper bound), or enumerated.
    """

    @abstractmethod
    def get_name(self):
        """
        :return: The name of the variable.
        """
        pass

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

    @abstractmethod
    def get_model(self):
        """
        :return: The model in which the variable was declared.
        """
        pass

    def __repr__(self):
        return "Choco IntVar ('" + self.get_name() + "')"
