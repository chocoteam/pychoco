from pychoco import backend
from pychoco._internals._handle_wrapper import _HandleWrapper
from pychoco._internals._intvar import _IntVar
from pychoco.solution import Solution


class _Solution(Solution, _HandleWrapper):
    """
    Internal class to represent a choco solution.
    """

    def __init__(self, handle):
        super().__init__(handle)

    def get_int_val(self, x: _IntVar):
        return backend.get_int_val(self.handle, x.handle)
