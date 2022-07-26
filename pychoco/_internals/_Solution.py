from pychoco import backend
from pychoco.Solution import Solution
from pychoco._internals._HandleWrapper import _HandleWrapper
from pychoco._internals._IntVar import _IntVar


class _Solution(Solution, _HandleWrapper):
    """
    Internal class to represent a choco solver.
    """

    def __init__(self, handle):
        super().__init__(handle)

    def get_int_val(self, x: _IntVar):
        return backend.get_int_val(self.handle, x.handle)
