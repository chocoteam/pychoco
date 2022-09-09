from abc import ABC, abstractmethod
from typing import List

from pychoco.objects.automaton.finite_automaton import FiniteAutomaton


class CostAutomaton(FiniteAutomaton, ABC):
    """
    Cost automaton.
    """

    @abstractmethod
    def add_counter_state(self, layer_value_state: List[List[List[int]]], min_bound: int, max_bound: int):
        """
        Add a counter state to this cost automaton.

        :param layer_value_state:
        :param min_bound:
        :param max_bound:
        """
        pass
