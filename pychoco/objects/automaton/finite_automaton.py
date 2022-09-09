from abc import ABC, abstractmethod
from typing import List


class FiniteAutomaton:
    pass


class FiniteAutomaton(ABC):
    """
    Class representing a finite automaton, which is used in regular constraints.
    """

    @property
    @abstractmethod
    def nb_states(self):
        """
        :return: The number of states in this automaton.
        """
        pass

    @property
    @abstractmethod
    def nb_symbols(self):
        """
        :return: The number of symbols in this automaton.
        """
        pass

    @property
    @abstractmethod
    def initial_state(self):
        """
        :return: The initial state of this automaton.
        """
        pass

    @abstractmethod
    def is_final(self, state: int):
        """
        Return True if state is final.

        :param state: A state.
        :return True if state is final, False otherwise.
        """
        pass

    @abstractmethod
    def add_state(self):
        """
        Add a state to this automaton.
        """
        pass

    @abstractmethod
    def remove_symbol(self, symbol: int):
        """
        Removes a symbol from this automaton.

        :param symbol: A symbol (int).
        """
        pass

    @abstractmethod
    def add_transition(self, source: int, destination: int, *symbols: List[int]):
        """
        Add a transition to this automaton.

        :param source: The source state.
        :param destination: The destination state.
        :param symbols: The symbols.
        """
        pass

    @abstractmethod
    def delete_transition(self, source: int, destination: int, symbol: int):
        """
        Delete a transition from this automaton.

        :param source: The source state.
        :param destination: The destination state.
        :param symbol: The symbol.
        """
        pass

    @abstractmethod
    def set_initial_state(self, state: int):
        """
        Define the initial state of this automaton.

        :param state: The state to be defined as initial.
        """
        pass

    @abstractmethod
    def set_final(self, *states: List[int]):
        """
        Set states as final.

        :param states: One or several states.
        """
        pass

    @abstractmethod
    def set_non_final(self, *states: List[int]):
        """
        Set states as non final.

        :param states: One or several states.
        """
        pass

    @abstractmethod
    def minimize(self):
        """
        Minimize the automaton.
        """
        pass

    @abstractmethod
    def union(self, other):
        """
        :param other Another automaton
        :return: The union of this and other.
        """
        pass

    @abstractmethod
    def complement(self):
        """
        :return: The complement of this automaton.
        """
        pass
