from abc import ABC, abstractmethod
from typing import Union, List

from pychoco.search.search_strategies import SearchStrategies
from pychoco.solution import Solution
from pychoco.variables.intvar import IntVar


class Solver(SearchStrategies, ABC):
    """
    The Solver is in charge of alternating constraint-propagation with search, and possibly learning,
    in order to compute solutions. This object may be configured in various ways.
    """

    @abstractmethod
    def solve(self,
              time_limit: Union[None, int] = None,
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
        :param time_limit: Time limit for search, None => no time limit.
        :param node_limit: Number of nodes limit for search, None => no node limit.
        :param fail_limit: Number of fails limit for search, None => no fail limit.
        :param restart_limit: Number of restarts limit for search, None => no restart limit.
        :param backtrack_limit: Number of backtracks limit for search, None => no backtracks limit.
        :return: True if a solution was found.
        """
        pass

    @abstractmethod
    def find_solution(self,
                      time_limit: Union[None, int] = None,
                      node_limit: Union[None, int] = None,
                      fail_limit: Union[None, int] = None,
                      restart_limit: Union[None, int] = None,
                      backtrack_limit: Union[None, int] = None) -> Solution:
        """
        Finds a solution and retrieve it.
        :param time_limit: Time limit for search, None => no time limit.
        :param node_limit: Number of nodes limit for search, None => no node limit.
        :param fail_limit: Number of fails limit for search, None => no fail limit.
        :param restart_limit: Number of restarts limit for search, None => no restart limit.
        :param backtrack_limit: Number of backtracks limit for search, None => no backtracks limit.
        :return: The first solution found.
        """
        pass

    @abstractmethod
    def find_all_solutions(self,
                           time_limit: Union[None, int] = None,
                           solution_limit: Union[None, int] = None,
                           node_limit: Union[None, int] = None,
                           fail_limit: Union[None, int] = None,
                           restart_limit: Union[None, int] = None,
                           backtrack_limit: Union[None, int] = None) -> List[Solution]:
        """
        Finds all the solutions to a problem, eventually with respect to search limits.
        :param time_limit: Time limit for search, None => no time limit.
        :param solution_limit: Number of solutions limit for search, None => no solution limit.
        :param node_limit: Number of nodes limit for search, None => no node limit.
        :param fail_limit: Number of fails limit for search, None => no fail limit.
        :param restart_limit: Number of restarts limit for search, None => no restart limit.
        :param backtrack_limit: Number of backtracks limit for search, None => no backtracks limit.
        :return: A list of solutions.
        """
        pass

    @abstractmethod
    def find_optimal_solution(self,
                              objective: IntVar,
                              maximize: bool,
                              time_limit: Union[None, int] = None,
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
        :param time_limit: Time limit for search, None => no time limit.
        :param solution_limit: Number of solutions limit for search, None => no solution limit.
        :param node_limit: Number of nodes limit for search, None => no node limit.
        :param fail_limit: Number of fails limit for search, None => no fail limit.
        :param restart_limit: Number of restarts limit for search, None => no restart limit.
        :param backtrack_limit: Number of backtracks limit for search, None => no backtracks limit.
        :return: The optimal (or best) solution found.
        """
        pass

    @abstractmethod
    def find_all_optimal_solutions(self,
                                   objective: IntVar,
                                   maximize: bool,
                                   time_limit: Union[None, int] = None,
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
        :param time_limit: Time limit for search, None => no time limit.
        :param solution_limit: Number of solutions limit for search, None => no solution limit.
        :param node_limit: Number of nodes limit for search, None => no node limit.
        :param fail_limit: Number of fails limit for search, None => no fail limit.
        :param restart_limit: Number of restarts limit for search, None => no restart limit.
        :param backtrack_limit: Number of backtracks limit for search, None => no backtracks limit.
        :return: All optimal (or best) solutions found.
        """
        pass

    @abstractmethod
    def show_statistics(self):
        """
        Configure the solver to show statistics during solving.
        """
        pass

    @abstractmethod
    def show_short_statistics(self):
        """
        Configure the solver to show short statistics during solving.
        """
        pass

    @abstractmethod
    def get_solution_count(self) -> int:
        """
        :return: The number of solution found so far.
        """
        pass

    @property
    @abstractmethod
    def model(self):
        """
        :return: The model associated with this solver.
        """
        pass

    def __repr__(self):
        return "Choco Solver"
