from abc import ABC, abstractmethod

from pychoco import backend
from pychoco._handle_wrapper import _HandleWrapper


class Variable(_HandleWrapper, ABC):
    """
    A variable (IntVar) is an unknown whose value of a constraint satisfaction (or optimization)
    problem. It is instantiated to a single value in any solution of the problem.
    """

    def __init__(self, handle, model):
        super().__init__(handle)
        self._model = model

    @property
    def name(self):
        """
        The name of the variable.
        """
        return backend.get_variable_name(self.handle)

    @property
    def model(self):
        """
        The model in which the variable was declared.
        """
        return self._model

    def is_instantiated(self):
        """
        :return: True if the variable is instantiated.
        """
        return backend.is_instantiated(self.handle)

    def is_view(self):
        """
        :return: True if this variable is a view
        """
        return backend.is_view(self.handle)

    @abstractmethod
    def get_type(self):
        """
        :return: The type of this variable.
        """
        pass

    def __repr__(self):
        return "Choco {} ('{}')".format(self.get_type(), self.name)
