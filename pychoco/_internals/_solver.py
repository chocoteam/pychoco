from typing import Union, List

from pychoco import backend
from pychoco._internals._handle_wrapper import _HandleWrapper
from pychoco._internals._intvar import _IntVar
from pychoco._internals._solution import _Solution
from pychoco._internals._utils import make_criterion_var_array, extract_solutions
from pychoco.solver import Solver


class _Solver(Solver, _HandleWrapper):
    """
    Internal class to represent a choco solver.
    """

    def __init__(self, handle, model):
        super().__init__(handle)
        self._model = model

    def find_solution(self,
                      time_limit: Union[None, int] = None,
                      node_limit: Union[None, int] = None,
                      fail_limit: Union[None, int] = None,
                      restart_limit: Union[None, int] = None,
                      backtrack_limit: Union[None, int] = None) -> _Solution:
        criterion = list()
        if time_limit is not None:
            criterion.append(backend.time_counter(self.model.handle, time_limit))
        if node_limit is not None:
            criterion.append(backend.node_counter(self.model.handle, node_limit))
        if fail_limit is not None:
            criterion.append(backend.fail_counter(self.model.handle, fail_limit))
        if restart_limit is not None:
            criterion.append(backend.restart_counter(self.handle, restart_limit))
        if backtrack_limit is not None:
            criterion.append(backend.backtrack_counter(self.handle, restart_limit))
        stop = make_criterion_var_array(*criterion)
        solution_handle = backend.find_solution(self.handle, stop)
        return _Solution(solution_handle)

    def find_all_solutions(self,
                           time_limit: Union[None, int] = None,
                           solution_limit: Union[None, int] = None,
                           node_limit: Union[None, int] = None,
                           fail_limit: Union[None, int] = None,
                           restart_limit: Union[None, int] = None,
                           backtrack_limit: Union[None, int] = None) -> List[_Solution]:
        criterion = list()
        if time_limit is not None:
            criterion.append(backend.time_counter(self.model.handle, time_limit))
        if solution_limit is not None:
            criterion.append(backend.solution_counter(self.model.handle, solution_limit))
        if node_limit is not None:
            criterion.append(backend.node_counter(self.model.handle, node_limit))
        if fail_limit is not None:
            criterion.append(backend.fail_counter(self.model.handle, fail_limit))
        if restart_limit is not None:
            criterion.append(backend.restart_counter(self.handle, restart_limit))
        if backtrack_limit is not None:
            criterion.append(backend.backtrack_counter(self.handle, restart_limit))
        stop = make_criterion_var_array(*criterion)
        solutions_list_handle = backend.find_all_solutions(self.handle, stop)
        return extract_solutions(solutions_list_handle)

    def find_optimal_solution(self,
                              objective: _IntVar,
                              maximize: bool,
                              time_limit: Union[None, int] = None,
                              solution_limit: Union[None, int] = None,
                              node_limit: Union[None, int] = None,
                              fail_limit: Union[None, int] = None,
                              restart_limit: Union[None, int] = None,
                              backtrack_limit: Union[None, int] = None) -> _Solution:
        criterion = list()
        if time_limit is not None:
            criterion.append(backend.time_counter(self.model.handle, time_limit))
        if solution_limit is not None:
            criterion.append(backend.solution_counter(self.model.handle, solution_limit))
        if node_limit is not None:
            criterion.append(backend.node_counter(self.model.handle, node_limit))
        if fail_limit is not None:
            criterion.append(backend.fail_counter(self.model.handle, fail_limit))
        if restart_limit is not None:
            criterion.append(backend.restart_counter(self.handle, restart_limit))
        if backtrack_limit is not None:
            criterion.append(backend.backtrack_counter(self.handle, restart_limit))
        stop = make_criterion_var_array(*criterion)
        solution_handle = backend.find_optimal_solution(self.handle, objective.handle, maximize, stop)
        return _Solution(solution_handle)

    def find_all_optimal_solutions(self,
                                   objective: _IntVar,
                                   maximize: bool,
                                   time_limit: Union[None, int] = None,
                                   solution_limit: Union[None, int] = None,
                                   node_limit: Union[None, int] = None,
                                   fail_limit: Union[None, int] = None,
                                   restart_limit: Union[None, int] = None,
                                   backtrack_limit: Union[None, int] = None) -> List[_Solution]:
        criterion = list()
        if time_limit is not None:
            criterion.append(backend.time_counter(self.model.handle, time_limit))
        if solution_limit is not None:
            criterion.append(backend.solution_counter(self.model.handle, solution_limit))
        if node_limit is not None:
            criterion.append(backend.node_counter(self.model.handle, node_limit))
        if fail_limit is not None:
            criterion.append(backend.fail_counter(self.model.handle, fail_limit))
        if restart_limit is not None:
            criterion.append(backend.restart_counter(self.handle, restart_limit))
        if backtrack_limit is not None:
            criterion.append(backend.backtrack_counter(self.handle, restart_limit))
        stop = make_criterion_var_array(*criterion)
        solutions_list_handle = backend.find_all_optimal_solution(self.handle, objective.handle, maximize, stop)
        return extract_solutions(solutions_list_handle)

    def show_statistics(self):
        backend.show_statistics(self.handle)

    def show_short_statistics(self):
        backend.show_short_statistics(self.handle)

    @property
    def model(self):
        return self._model
