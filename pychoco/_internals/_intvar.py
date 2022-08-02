from pychoco import backend
from pychoco._internals._handle_wrapper import _HandleWrapper
from pychoco.variables.intvar import IntVar


class _IntVar(IntVar, _HandleWrapper):
    """
    Internal class to represent an intvar.
    """

    def __init__(self, handle, model):
        super().__init__(handle)
        self._model = model

    @property
    def name(self):
        return backend.get_intvar_name(self.handle)

    def get_lb(self):
        return backend.get_intvar_lb(self.handle)

    def get_ub(self):
        return backend.get_intvar_ub(self.handle)

    @property
    def model(self):
        return self._model
