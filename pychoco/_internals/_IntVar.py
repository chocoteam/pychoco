from pychoco import backend
from pychoco._internals._HandleWrapper import _HandleWrapper
from pychoco.variables.IntVar import IntVar


class _IntVar(IntVar, _HandleWrapper):
    """
    Internal class to represent a choco model.
    """

    def __init__(self, handle, model):
        super().__init__(handle)
        self._model = model

    def get_name(self):
        return backend.get_intvar_name(self.handle)

    def get_lb(self):
        return backend.get_intvar_lb(self.handle)

    def get_ub(self):
        return backend.get_intvar_ub(self.handle)

    def get_model(self):
        return self._model
