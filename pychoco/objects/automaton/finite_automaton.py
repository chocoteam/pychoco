from typing import List, Union

from pychoco import backend
from pychoco._handle_wrapper import _HandleWrapper
from pychoco._utils import make_int_array


class FiniteAutomaton(_HandleWrapper):
    """
    Class representing a finite automaton, which is used in regular constraints.
    """

    def __init__(self, regexp: Union[str, None] = None, bounds: Union[List[int], None] = None, _handle=None):
        """
        Finite automaton constructor (for regular constraints).

        :param regexp: A regexpt describing the automaton (optional).
        :param bounds: [min, max] (optional).
        """
        if _handle is not None:
            super().__init__(_handle)
        else:
            if regexp is None:
                handle = backend.create_fa()
            elif bounds is None:
                handle = backend.create_fa_regexp(regexp)
            else:
                assert len(bounds) == 2
                handle = backend.create_fa_regexp_min_max(regexp, bounds[0], bounds[1])
            super().__init__(handle)

    @property
    def nb_states(self):
        """
        :return: The number of states in this automaton.
        """
        return backend.get_nb_states(self._handle)

    @property
    def nb_symbols(self):
        """
        :return: The number of symbols in this automaton.
        """
        return backend.get_nb_symbols(self._handle)

    @property
    def initial_state(self):
        """
        :return: The initial state of this automaton.
        """
        return backend.get_initial_state(self._handle)

    def is_final(self, state: int):
        """
        Return True if state is final.

        :param state: A state.
        :return True if state is final, False otherwise.
        """
        return backend.is_final(self._handle, state)

    def add_state(self):
        """
        Add a state to this automaton.
        """
        return backend.add_state(self._handle)

    def remove_symbol(self, symbol: int):
        """
        Removes a symbol from this automaton.

        :param symbol: A symbol (int).
        """
        backend.remove_symbol(self._handle, symbol)

    def add_transition(self, source: int, destination: int, *symbols: List[int]):
        """
        Add a transition to this automaton.

        :param source: The source state.
        :param destination: The destination state.
        :param symbols: The symbols.
        """
        symbols_handle = make_int_array(symbols)
        backend.add_transition(self._handle, source, destination, symbols_handle)

    def delete_transition(self, source: int, destination: int, symbol: int):
        """
        Delete a transition from this automaton.

        :param source: The source state.
        :param destination: The destination state.
        :param symbol: The symbol.
        """
        backend.delete_transition(self._handle, source, destination, symbol)

    def set_initial_state(self, state: int):
        """
        Define the initial state of this automaton.

        :param state: The state to be defined as initial.
        """
        backend.set_initial_state(self._handle, state)

    def set_final(self, *states: List[int]):
        """
        Set states as final.

        :param states: One or several states.
        """
        states_handle = make_int_array(states)
        backend.set_final(self._handle, states_handle)

    def set_non_final(self, *states: List[int]):
        """
        Set states as non final.

        :param states: One or several states.
        """
        states_handle = make_int_array(states)
        backend.set_non_final(self._handle, states_handle)

    def minimize(self):
        """
        Minimize the automaton.
        """
        return FiniteAutomaton(_handle=backend.fa_minimize(self._handle))

    def union(self, other):
        """
        :param other Another automaton
        :return: The union of this and other.
        """
        return FiniteAutomaton(_handle=backend.fa_union(self._handle, other._handle))

    def complement(self):
        """
        :return: The complement of this automaton.
        """
        return FiniteAutomaton(_handle=backend.fa_complement(self._handle))
