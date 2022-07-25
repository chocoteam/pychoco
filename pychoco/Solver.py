from abc import ABC, abstractmethod


class Solver(ABC):
    """
    The Solver is in charge of alternating constraint-propagation with search, and possibly learning,
    in order to compute solutions. This object may be configured in various ways.
    """

    @abstractmethod
    def find_solution(self):
        """
        Finds a solution and retrieve it.
        :return: The first solution found.
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

    def __repr__(self):
        return "Choco Solver"
