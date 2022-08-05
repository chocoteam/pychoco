from pychoco import backend
from pychoco._internals._handle_wrapper import _HandleWrapper
from pychoco._internals._variable import _Variable
from pychoco.variables.intvar import IntVar


class _IntVar(_Variable, IntVar, _HandleWrapper):
    """
    Internal class to represent an intvar.
    """

    def __init__(self, handle, model):
        super().__init__(handle, model)

    def get_lb(self):
        return backend.get_intvar_lb(self.handle)

    def get_ub(self):
        return backend.get_intvar_ub(self.handle)

    def get_value(self):
        return backend.get_intvar_value(self.handle)
