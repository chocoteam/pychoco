from abc import ABC, abstractmethod


class Variable(ABC):
    """
    A variable (IntVar) is an unknown whose value of a constraint satisfaction (or optimization)
    problem. It is instantiated to a single value in any solution of the problem.
    """

    @property
    @abstractmethod
    def name(self):
        """
        :return: The name of the variable.
        """
        pass

    @property
    @abstractmethod
    def model(self):
        """
        :return: The model in which the variable was declared.
        """
        pass

    @abstractmethod
    def is_instantiated(self):
        """
        :return: True if the variable is instantiated.
        """
        pass

    def __repr__(self):
        return "Choco Variable ('" + self.name() + "')"
