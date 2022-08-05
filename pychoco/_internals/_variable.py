from abc import ABC

from pychoco import backend
from pychoco._internals._handle_wrapper import _HandleWrapper
from pychoco.variables.variable import Variable


class _Variable(Variable, _HandleWrapper, ABC):
    """
    Internal class to represent a variable.
    """

    def __init__(self, handle, model):
        super().__init__(handle)
        self._model = model

    @property
    def name(self):
        return backend.get_variable_name(self.handle)

    @property
    def model(self):
        return self._model

    def is_instantiated(self):
        return backend.is_instantiated(self.handle)
