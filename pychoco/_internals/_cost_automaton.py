from typing import List, Union

from pychoco import backend
from pychoco._internals._finite_automaton import _FiniteAutomaton
from pychoco._internals._handle_wrapper import _HandleWrapper
from pychoco._internals._utils import make_int_array_array_array
from pychoco.objects.automaton.cost_automaton import CostAutomaton


class _CostAutomaton(_FiniteAutomaton, CostAutomaton, _HandleWrapper):

    def add_counter_state(self, layer_value_state: List[List[List[int]]], min_bound: int, max_bound: int):
        layer_value_state_handle = make_int_array_array_array(*layer_value_state)
        counter_handle = backend.create_counter_state(layer_value_state_handle, min_bound, max_bound)
        backend.cost_fa_add_counter(self.handle, counter_handle)


def _create_cost_automaton(automaton: Union[_FiniteAutomaton, None] = None):
    if automaton is None:
        handle = backend.create_cost_fa()
    else:
        handle = backend.create_cost_fa_from_fa(automaton.handle)
    return _CostAutomaton(handle)
