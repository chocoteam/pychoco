from pychoco import backend
from pychoco._internals._boolvar import _BoolVar
from pychoco._internals._handle_wrapper import _HandleWrapper
from pychoco.constraints.constraint import Constraint
from pychoco.utils import ESat


class _Constraint(Constraint, _HandleWrapper):
    """
    Internal class to represent a choco model.
    """

    def __init__(self, handle, model):
        super().__init__(handle)
        self._model = model

    def get_name(self):
        return backend.get_constraint_name(self.handle)

    @property
    def model(self):
        return self._model

    def post(self):
        backend.post(self.handle)

    def reify(self):
        var_handle = backend.reify(self.handle)
        return _BoolVar(var_handle, self.model)

    def is_satisfied(self):
        state = backend.is_satisfied(self.handle)
        if state == 0:
            return ESat.FALSE
        if state == 1:
            return ESat.TRUE
        return ESat.UNDEFINED
