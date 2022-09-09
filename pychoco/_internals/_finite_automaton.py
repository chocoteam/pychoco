from typing import List, Union

from pychoco import backend
from pychoco._internals._handle_wrapper import _HandleWrapper
from pychoco._internals._utils import make_int_array
from pychoco.objects.automaton.finite_automaton import FiniteAutomaton


class _FiniteAutomaton(FiniteAutomaton, _HandleWrapper):

    def __init__(self, handle):
        super().__init__(handle)

    @property
    def nb_states(self):
        return backend.get_nb_states(self.handle)

    @property
    def nb_symbols(self):
        return backend.get_nb_symbols(self.handle)

    @property
    def initial_state(self):
        return backend.get_initial_state(self.handle)

    def is_final(self, state: int):
        return backend.is_final(self.handle, state)

    def add_state(self):
        return backend.add_state(self.handle)

    def remove_symbol(self, symbol: int):
        backend.remove_symbol(self.handle, symbol)

    def add_transition(self, source: int, destination: int, *symbols: List[int]):
        symbols_handle = make_int_array(*symbols)
        backend.add_transition(self.handle, source, destination, symbols_handle)

    def delete_transition(self, source: int, destination: int, symbol: int):
        backend.delete_transition(self.handle, source, destination, symbol)

    def set_initial_state(self, state: int):
        backend.set_initial_state(self.handle, state)

    def set_final(self, *states: List[int]):
        states_handle = make_int_array(*states)
        backend.set_final(self.handle, states_handle)

    def set_non_final(self, *states: List[int]):
        states_handle = make_int_array(*states)
        backend.set_non_final(self.handle, states_handle)

    def minimize(self):
        backend.fa_minimize(self.handle)

    def union(self, other):
        return backend.fa_union(self.handle, other.handle)

    def complement(self):
        return backend.fa_complement(self.handle)


def _create_finite_automaton(regexp: Union[str, None] = None, bounds: Union[List[int], None] = None):
    if regexp is None:
        handle = backend.create_fa()
    elif bounds is None:
        handle = backend.create_fa_regexp(regexp)
    else:
        assert len(bounds) == 2
        handle = backend.create_fa_regexp_min_max(regexp, bounds[0], bounds[1])
    return _FiniteAutomaton(handle)
