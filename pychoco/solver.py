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
    def _handle(self):
        return self._handle_

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
            criterion.append(backend.node_counter(self.model._handle, node_limit))
        if fail_limit is not None:
            criterion.append(backend.fail_counter(self.model._handle, fail_limit))
        if restart_limit is not None:
            criterion.append(backend.restart_counter(self._handle, restart_limit))
        if backtrack_limit is not None:
            criterion.append(backend.backtrack_counter(self._handle, restart_limit))
        stop = make_criterion_var_array(criterion)
        return bool(backend.solve(self._handle, stop))

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
            criterion.append(backend.node_counter(self.model._handle, node_limit))
        if fail_limit is not None:
            criterion.append(backend.fail_counter(self.model._handle, fail_limit))
        if restart_limit is not None:
            criterion.append(backend.restart_counter(self._handle, restart_limit))
        if backtrack_limit is not None:
            criterion.append(backend.backtrack_counter(self._handle, restart_limit))
        stop = make_criterion_var_array(criterion)
        solution_handle = backend.find_solution(self._handle, stop)
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
            criterion.append(backend.solution_counter(self.model._handle, solution_limit))
        if node_limit is not None:
            criterion.append(backend.node_counter(self.model._handle, node_limit))
        if fail_limit is not None:
            criterion.append(backend.fail_counter(self.model._handle, fail_limit))
        if restart_limit is not None:
            criterion.append(backend.restart_counter(self._handle, restart_limit))
        if backtrack_limit is not None:
            criterion.append(backend.backtrack_counter(self._handle, restart_limit))
        stop = make_criterion_var_array(criterion)
        solutions_list_handle = backend.find_all_solutions(self._handle, stop)
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
            criterion.append(backend.solution_counter(self.model._handle, solution_limit))
        if node_limit is not None:
            criterion.append(backend.node_counter(self.model._handle, node_limit))
        if fail_limit is not None:
            criterion.append(backend.fail_counter(self.model._handle, fail_limit))
        if restart_limit is not None:
            criterion.append(backend.restart_counter(self._handle, restart_limit))
        if backtrack_limit is not None:
            criterion.append(backend.backtrack_counter(self._handle, restart_limit))
        stop = make_criterion_var_array(criterion)
        solution_handle = backend.find_optimal_solution(self._handle, objective._handle, maximize, stop)
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
            criterion.append(backend.solution_counter(self.model._handle, solution_limit))
        if node_limit is not None:
            criterion.append(backend.node_counter(self.model._handle, node_limit))
        if fail_limit is not None:
            criterion.append(backend.fail_counter(self.model._handle, fail_limit))
        if restart_limit is not None:
            criterion.append(backend.restart_counter(self._handle, restart_limit))
        if backtrack_limit is not None:
            criterion.append(backend.backtrack_counter(self._handle, restart_limit))
        stop = make_criterion_var_array(criterion)
        solutions_list_handle = backend.find_all_optimal_solutions(self._handle, objective._handle, maximize, stop)
        return extract_solutions(solutions_list_handle)

    def show_statistics(self):
        """
        Configure the solver to show statistics during solving.
        """
        backend.show_statistics(self._handle)

    def show_short_statistics(self):
        """
        Configure the solver to show short statistics during solving.
        """
        backend.show_short_statistics(self._handle)

    def show_restarts(self):
        """
        Configure the solver to show the number of restarts during the search.
        """
        backend.show_restarts(self._handle)

    def show_restarts(self):
        """
        Configure the solver to show restarts during solving.
        """
        backend.show_restarts(self._handle)

    def show_decisions(self, nb_chars: int = 20):
        """
        Configure the solver to show decisions during solving.
        :param nb_chars: Number of characters to show for variable and value names.
        """
        backend.show_decisions(self._handle, nb_chars)

    def show_solutions(self):
        """
        Configure the solver to show solutions during solving.
        """
        backend.show_solutions(self._handle)

    def show_solutions(self, intvars: List[IntVar]):
        """
        Configure the solver to show solutions during solving, with the specified variables and their values.
        :param intvars: List of variables to show in solutions.
        """
        vars_array = make_intvar_array(intvars)
        backend.show_solutions(self._handle, vars_array)

    def get_solution_count(self) -> int:
        """
        :return: The number of solution found so far.
        """
        return backend.get_solution_count(self._handle)
    
    def get_time_count(self) -> float:
        """
        :return: The time count in milliseconds.
        """
        return backend.get_time_count(self._handle)

    def get_node_count(self) -> int:
        """
        :return: The node count.
        """
        return backend.get_node_count(self._handle)
    
    def get_backtrack_count(self) -> int:
        """
        :return: The backtrack count.
        """
        return backend.get_backtrack_count(self._handle)

    def get_fail_count(self) -> int:
        """
        :return: The fail count.
        """
        return backend.get_fail_count(self._handle)
    
    def get_restart_count(self) -> int:
        """
        :return: The restart count.
        """
        return backend.get_restart_count(self._handle)
    
    def get_search_state(self) -> str:
        """
        :return: the search state as a string ('NEW', 'RUNNING', 'TERMINATED', 'STOPPED', 'KILLED').
        """
        return backend.get_search_state(self._handle)

    def is_objective_optimal(self) -> bool:
        """
        :return: True if the objective is proven optimal, False otherwise.
        """
        return backend.is_objective_optimal(self._handle)

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
        backend.limit_time(self._handle, time_limit)

    def get_time_count(self):
        """
        :return: the time count (in seconds)
        """
        return backend.get_time_count(self._handle)

    def get_node_count(self):
        """
        :return: the time count (in seconds)
        """
        return backend.get_time_count(self._handle)
    def get_backtrack_count(self):
        """
        :return: the backtrack count
        """
        return backend.get_backtrack_count(self._handle)
    def get_fail_count(self):
        """
        :return: the fail count (in seconds)
        """
        return backend.get_fail_count(self._handle)
    def get_restart_count(self):
        """
        :return: the restart count (in seconds)
        """
        return backend.get_restart_count(self._handle)
    def is_objective_optimal(self):
        """
        :return: true if the objective is optimal
        """
        return backend.is_objective_optimal(self._handle)
    def get_search_state(self):
        """
        :return: the search state
        """
        return backend.get_search_state(self._handle)

    def _propagate(self):
        """
        Propagates constraints and related events through the constraint network until a fix point is find,
        or a contradiction is detected.
        Throws ContradictionException inconsistency is detected, the problem has no solution with the current set of domains and constraints.
        The propagation engine is ensured to be empty (no pending events) after this method.
        Indeed, if no contradiction occurs, a fix point is reached.
        Otherwise, a call to PropagationEngine#flush() is made.
        """
        backend.propagate(self._handle)

    def _push_state(self):
        """
        Starts a new branch in the search tree
        """
        backend.push_state(self._handle)

    def _pop_state(self):
        """
        Backtracks to the previous choice point in the search tree
        """
        backend.pop_state(self._handle)

    def __repr__(self):
        return "Choco Solver"

    def set_default_search(self):
        backend.set_default_search(self._handle)

    def set_dom_over_w_deg_search(self, *intvars):
        assert len(intvars) > 0, "No variables were declared for the search"
        print("before handle", intvars)
        var_array_handle = make_intvar_array(intvars)
        print("after handle")
        backend.set_dom_over_w_deg_search(self._handle, var_array_handle)

    def set_dom_over_w_deg_ref_search(self, *intvars):
        assert len(intvars) > 0, "No variables were declared for the search"
        print("before handle", intvars)
        var_array_handle = make_intvar_array(intvars)
        print("after handle")
        backend.set_dom_over_w_deg_ref_search(self._handle, var_array_handle)

    def set_activity_based_search(self, *intvars):
        assert len(intvars) > 0, "No variables were declared for the search"
        var_array_handle = make_intvar_array(intvars)
        backend.set_activity_based_search(self._handle, var_array_handle)

    def set_min_dom_lb_search(self, *intvars):
        assert len(intvars) > 0, "No variables were declared for the search"
        var_array_handle = make_intvar_array(intvars)
        backend.set_min_dom_lb_search(self._handle, var_array_handle)

    def set_min_dom_ub_search(self, *intvars):
        assert len(intvars) > 0, "No variables were declared for the search"
        var_array_handle = make_intvar_array(intvars)
        backend.set_min_dom_ub_search(self._handle, var_array_handle)

    def set_random_search(self, *intvars, seed: int = round(time.time())):
        assert len(intvars) > 0, "No variables were declared for the search"
        var_array_handle = make_intvar_array(intvars)
        backend.set_random_search(self._handle, var_array_handle, seed)

    def set_conflict_history_search(self, *intvars):
        assert len(intvars) > 0, "No variables were declared for the search"
        var_array_handle = make_intvar_array(intvars)
        backend.set_conflict_history_search(self._handle, var_array_handle)

    def set_input_order_lb_search(self, *intvars):
        assert len(intvars) > 0, "No variables were declared for the search"
        assert len(intvars) > 0, "No variables were declared for the search"
        var_array_handle = make_intvar_array(intvars)
        backend.set_input_order_lb_search(self._handle, var_array_handle)

    def set_input_order_ub_search(self, *intvars):
        assert len(intvars) > 0, "No variables were declared for the search"
        var_array_handle = make_intvar_array(intvars)
        backend.set_input_order_ub_search(self._handle, var_array_handle)

    def set_failure_length_based_search(self, *intvars):
        assert len(intvars) > 0, "No variables were declared for the search"
        var_array_handle = make_intvar_array(intvars)
        backend.set_failure_length_based_search(self._handle, var_array_handle)

    def set_failure_rate_based_search(self, *intvars):
        assert len(intvars) > 0, "No variables were declared for the search"
        var_array_handle = make_intvar_array(intvars)
        backend.set_failure_rate_based_search(self._handle, var_array_handle)

    def set_pick_on_dom_search(self, *intvars):
        assert len(intvars) > 0, "No variables were declared for the search"
        var_array_handle = make_intvar_array(intvars)
        backend.set_pick_on_dom_search(self._handle, var_array_handle)
    
    def set_round_robin_search(self, *intvars):
        assert len(intvars) > 0, "No variables were declared for the search"
        var_array_handle = make_intvar_array(intvars)
        backend.set_round_robin_search(self._handle, var_array_handle)

    def add_hint(self, intvar, value):
        backend.add_hint(self._handle, intvar._handle, value)

    def rem_hints(self):
        backend.rem_hints(self._handle)

    def set_nogood_recording_from_solutions(self, intvars: List[IntVar]):
        """
        Configure the solver to record nogoods from solutions.
        :param intvars: List of variables to record in nogoods.
        """
        var_array_handle = make_intvar_array(intvars)
        backend.set_nogood_recording_from_solutions(self._handle, var_array_handle)

    def set_nogood_recording_from_restarts(self):
        """
        Configure the solver to record nogoods from restarts.
        """
        backend.set_nogood_recording_from_restarts(self._handle)

    def set_geometrical_restart(self, base: int, inc: float):
        """Configure the solver to use geometrical restarts with the given base and increment.
        :param base: The base for the geometrical restart strategy.
        :param inc: The increment for the geometrical restart strategy.
        """
        backend.set_geometrical_restart(self._handle, base, inc)

    def set_luby_restart(self, base: int):
        """Configure the solver to use Luby restarts with the given base.
        :param base: The base for the Luby restart strategy.
        """
        backend.set_luby_restart(self._handle, base)
    
    def set_restart_on_solutions(self):
        """Configure the solver to restart after each solution found.
        """
        backend.set_restart_on_solutions(self._handle)
