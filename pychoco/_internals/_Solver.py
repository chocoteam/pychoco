from pychoco import backend
from pychoco.Solver import Solver
from pychoco._internals._HandleWrapper import _HandleWrapper
from pychoco._internals._Solution import _Solution


class _Solver(Solver, _HandleWrapper):
    """
    Internal class to represent a choco solver.
    """

    def __init__(self, handle):
        super().__init__(handle)

    def find_solution(self) -> _Solution:
        solution_handle = backend.find_solution(self.handle)
        return _Solution(solution_handle)

    def show_statistics(self):
        backend.show_statistics(self.handle)

    def show_short_statistics(self):
        backend.show_short_statistics(self.handle)
