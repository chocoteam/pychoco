from typing import List, Union

from pychoco import backend
from pychoco._utils import make_int_3d_array, make_intvar_array, make_int_4d_array, make_int_2d_array
from pychoco.objects.automaton.finite_automaton import FiniteAutomaton
from pychoco.variables.intvar import IntVar


class CostAutomaton(FiniteAutomaton):
    """
    Cost automaton.
    """

    def __init__(self, automaton: Union[FiniteAutomaton, None] = None, _handle=None):
        """
        Cost automaton constructor.

        :param automaton: Another automaton (optional).
        """
        if _handle is not None:
            super().__init__(_handle=_handle)
        else:
            if automaton is None:
                handle = backend.create_cost_fa()
            else:
                handle = backend.create_cost_fa_from_fa(automaton._handle)
            super().__init__(_handle=handle)

    def add_counter_state(self, layer_value_state: List[List[List[int]]], min_bound: int, max_bound: int):
        """
        Add a counter state to this cost automaton.

        :param layer_value_state:
        :param min_bound:
        :param max_bound:
        """
        layer_value_state_handle = make_int_3d_array(layer_value_state)
        counter_handle = backend.create_counter_state(layer_value_state_handle, min_bound, max_bound)
        backend.cost_fa_add_counter(self._handle, counter_handle)


def make_single_resource(automaton: FiniteAutomaton, costs: Union[List[List[int]], List[List[List[int]]]], inf: int,
                         sup: int):
    """
    :param automaton: A finite automaton.
    :param costs: Costs (2 or 3 dimensional int matrix).
    :param inf: Lower bound.
    :param sup: Upper bound.
    :return: A cost automaton from a finite automaton and costs.
    """
    assert len(costs) > 0
    c1 = costs[0]
    assert len(c1) > 0
    c2 = c1[0]
    if isinstance(c2, list):
        assert len(c2) > 0
        handle = backend.make_single_resource_iii(automaton._handle, make_int_3d_array(costs), inf, sup)
    else:
        handle = backend.make_single_resource_ii(automaton._handle, make_int_2d_array(costs), inf, sup)
    return CostAutomaton(_handle=handle)


def make_multi_resources(automaton: FiniteAutomaton, costs: Union[List[List[List[int]]], List[List[List[List[int]]]]],
                         bounds: List[IntVar]):
    """
    :param automaton: A finite automaton.
    :param costs: Costs (3 or 4 dimensional int matrix).
    :param bounds: List of IntVars defining bounds.
    :return: A multi cost automaton from a finite automaton and costs.
    """
    assert len(costs) > 0
    c1 = costs[0]
    assert len(c1) > 0
    c2 = c1[0]
    assert len(c2) > 0
    c3 = c2[0]
    if isinstance(c3, list):
        assert len(c3) > 0
        handle = backend.make_multi_resources_iiii(automaton._handle, make_int_4d_array(costs),
                                                   make_intvar_array(bounds))
    else:
        handle = backend.make_multi_resources_iii(automaton._handle, make_int_3d_array(costs),
                                                  make_intvar_array(bounds))
    return CostAutomaton(_handle=handle)
