from pychoco import backend
from pychoco._internals._HandleWrapper import _HandleWrapper
from pychoco.constraints.Constraint import Constraint


class _Constraint(Constraint, _HandleWrapper):
    """
    Internal class to represent a choco model.
    """

    def __init__(self, handle):
        super().__init__(handle)

    def get_name(self):
        return backend.get_constraint_name(self.handle)

    def post(self):
        backend.post(self.handle)
