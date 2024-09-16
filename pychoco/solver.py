import time
from typing import Union, List

from pychoco import backend
from pychoco._handle_wrapper import _HandleWrapper
from pychoco._utils import make_criterion_var_array, extract_solutions, make_intvar_array
from pychoco.search.search_strategies import SearchStrategies
from pychoco.solution import Solution
from pychoco.variables.intvar import IntVar


class Solver(SearchStrategies, _HandleWrapper):
    """
    The Solver is in charge of alternating constraint-propagation with search, and possibly learning,
    in order to compute solutions. This object may be configured in various ways.
    """

    def __init__(self, handle: "SwigPyObject", model: "_Model"):
        """
        Warning: Not intended to be used by users, use a Model object to instantiate constraints instead.
        """
        super().__init__(handle)
        self._model = model

    @property
    def handle(self):
        return self._handle

    def solve(self,
              time_limit: Union[None, str] = None,
              node_limit: Union[None, int] = None,
              fail_limit: Union[None, int] = None,
              restart_limit: Union[None, int] = None,
              backtrack_limit: Union[None, int] = None) -> bool:
        """
        Executes the solver as it is configured.
        Default configuration:
        - SATISFACTION : Computes a feasible solution. Use while(solve()) to enumerate all solutions.
        - OPTIMISATION : Computes a feasible solution, wrt to the objective defined. Use while solve(): to find the
        optimal solution. Indeed, each new solution improves the objective. If no new solution is
        found (and no stop criterion encountered), the last one is guaranteed to be the optimal one.
        :param time_limit: Time limit for search (e.g. "10s", "2m"), None => no time limit.
        :param node_limit: Number of nodes limit for search, None => no node limit.
        :param fail_limit: Number of fails limit for search, None => no fail limit.
        :param restart_limit: Number of restarts limit for search, None => no restart limit.
        :param backtrack_limit: Number of backtracks limit for search, None => no backtracks limit.
        :return: True if a solution was found.
        """
        criterion = list()
        if time_limit is not None:
            self.limit_time(time_limit)
        if node_limit is not None:
            criterion.append(backend.node_counter(self.model.handle, node_limit))
        if fail_limit is not None:
            criterion.append(backend.fail_counter(self.model.handle, fail_limit))
        if restart_limit is not None:
            criterion.append(backend.restart_counter(self.handle, restart_limit))
        if backtrack_limit is not None:
            criterion.append(backend.backtrack_counter(self.handle, restart_limit))
        stop = make_criterion_var_array(criterion)
        return bool(backend.solve(self.handle, stop))

    def find_solution(self,
                      time_limit: Union[None, str] = None,
                      node_limit: Union[None, int] = None,
                      fail_limit: Union[None, int] = None,
                      restart_limit: Union[None, int] = None,
                      backtrack_limit: Union[None, int] = None) -> Solution:
        """
        Finds a solution and retrieve it.
        :param time_limit: Time limit for search (e.g. "10s", "2m"), None => no time limit.
        :param node_limit: Number of nodes limit for search, None => no node limit.
        :param fail_limit: Number of fails limit for search, None => no fail limit.
        :param restart_limit: Number of restarts limit for search, None => no restart limit.
        :param backtrack_limit: Number of backtracks limit for search, None => no backtracks limit.
        :return: The first solution found.
        """
        criterion = list()
        if time_limit is not None:
            self.limit_time(time_limit)
        if node_limit is not None:
            criterion.append(backend.node_counter(self.model.handle, node_limit))
        if fail_limit is not None:
            criterion.append(backend.fail_counter(self.model.handle, fail_limit))
        if restart_limit is not None:
            criterion.append(backend.restart_counter(self.handle, restart_limit))
        if backtrack_limit is not None:
            criterion.append(backend.backtrack_counter(self.handle, restart_limit))
        stop = make_criterion_var_array(criterion)
        solution_handle = backend.find_solution(self.handle, stop)
        if solution_handle is None:
            return None
        return Solution(solution_handle)

    def find_all_solutions(self,
                           time_limit: Union[None, str] = None,
                           solution_limit: Union[None, int] = None,
                           node_limit: Union[None, int] = None,
                           fail_limit: Union[None, int] = None,
                           restart_limit: Union[None, int] = None,
                           backtrack_limit: Union[None, int] = None) -> List[Solution]:
        """
        Finds all the solutions to a problem, eventually with respect to search limits.
        :param time_limit: Time limit for search (e.g. "10s", "2m"), None => no time limit.
        :param solution_limit: Number of solutions limit for search, None => no solution limit.
        :param node_limit: Number of nodes limit for search, None => no node limit.
        :param fail_limit: Number of fails limit for search, None => no fail limit.
        :param restart_limit: Number of restarts limit for search, None => no restart limit.
        :param backtrack_limit: Number of backtracks limit for search, None => no backtracks limit.
        :return: A list of solutions.
        """
        criterion = list()
        if time_limit is not None:
            self.limit_time(time_limit)
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
        stop = make_criterion_var_array(criterion)
        solutions_list_handle = backend.find_all_solutions(self.handle, stop)
        return extract_solutions(solutions_list_handle)

    def find_optimal_solution(self,
                              objective: IntVar,
                              maximize: bool,
                              time_limit: Union[None, str] = None,
                              solution_limit: Union[None, int] = None,
                              node_limit: Union[None, int] = None,
                              fail_limit: Union[None, int] = None,
                              restart_limit: Union[None, int] = None,
                              backtrack_limit: Union[None, int] = None) -> Solution:
        """
        Finds the optimal solution (minimum or maximum) solution according to an objective variable.
        Note that if search limits were defined, the returned solution might not be the optimal, but the
        best found so far.
        :param objective: Objective variable.
        :param maximize: if True, maximizes the objective variable, otherwise minimizes it.
        :param time_limit: Time limit for search (e.g. "10s", "2m"), None => no time limit.
        :param solution_limit: Number of solutions limit for search, None => no solution limit.
        :param node_limit: Number of nodes limit for search, None => no node limit.
        :param fail_limit: Number of fails limit for search, None => no fail limit.
        :param restart_limit: Number of restarts limit for search, None => no restart limit.
        :param backtrack_limit: Number of backtracks limit for search, None => no backtracks limit.
        :return: The optimal (or best) solution found.
        """
        criterion = list()
        if time_limit is not None:
            self.limit_time(time_limit)
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
        stop = make_criterion_var_array(criterion)
        solution_handle = backend.find_optimal_solution(self.handle, objective.handle, maximize, stop)
        if solution_handle is None:
            return None
        return Solution(solution_handle)

    def find_all_optimal_solutions(self,
                                   objective: IntVar,
                                   maximize: bool,
                                   time_limit: Union[None, str] = None,
                                   solution_limit: Union[None, int] = None,
                                   node_limit: Union[None, int] = None,
                                   fail_limit: Union[None, int] = None,
                                   restart_limit: Union[None, int] = None,
                                   backtrack_limit: Union[None, int] = None) -> List[Solution]:
        """
        Finds all optimal solutions (minimum or maximum) solution according to an objective variable.
        Note that if search limits were defined, the returned solutions might not be optimal, but the
        best found so far.
        :param objective: Objective variable.
        :param maximize: if True, maximizes the objective variable, otherwise minimizes it.
        :param time_limit: Time limit for search (e.g. "10s", "2m"), None => no time limit.
        :param solution_limit: Number of solutions limit for search, None => no solution limit.
        :param node_limit: Number of nodes limit for search, None => no node limit.
        :param fail_limit: Number of fails limit for search, None => no fail limit.
        :param restart_limit: Number of restarts limit for search, None => no restart limit.
        :param backtrack_limit: Number of backtracks limit for search, None => no backtracks limit.
        :return: All optimal (or best) solutions found.
        """
        criterion = list()
        if time_limit is not None:
            self.limit_time(time_limit)
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
        stop = make_criterion_var_array(criterion)
        solutions_list_handle = backend.find_all_optimal_solutions(self.handle, objective.handle, maximize, stop)
        return extract_solutions(solutions_list_handle)

    def show_statistics(self):
        """
        Configure the solver to show statistics during solving.
        """
        backend.show_statistics(self.handle)

    def show_short_statistics(self):
        """
        Configure the solver to show short statistics during solving.
        """
        backend.show_short_statistics(self.handle)

    def show_restarts(self):
        """
        Configure the solver to show the number of restarts during the search.
        """
        backend.show_restarts(self.handle)

    def get_solution_count(self) -> int:
        """
        :return: The number of solution found so far.
        """
        return backend.get_solution_count(self.handle)

    @property
    def model(self):
        """
        :return: The model associated with this solver.
        """
        return self._model

    def limit_time(self, time_limit: str):
        """
        Limit the solving time.
        :param: String which states the duration like "WWd XXh YYm ZZs".
        """
        backend.limit_time(self.handle, time_limit)

    def _propagate(self):
        """
        Propagates constraints and related events through the constraint network until a fix point is find,
        or a contradiction is detected.
        Throws ContradictionException inconsistency is detected, the problem has no solution with the current set of domains and constraints.
        The propagation engine is ensured to be empty (no pending events) after this method.
        Indeed, if no contradiction occurs, a fix point is reached.
        Otherwise, a call to PropagationEngine#flush() is made.
        """
        backend.propagate(self.handle)

    def _push_state(self):
        """
        Starts a new branch in the search tree
        """
        backend.push_state(self.handle)

    def _pop_state(self):
        """
        Backtracks to the previous choice point in the search tree
        """
        backend.pop_state(self.handle)

    def __repr__(self):
        return "Choco Solver"
