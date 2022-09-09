import unittest

from pychoco import create_model, create_cost_automaton


class TestCostRegular(unittest.TestCase):

    def testCostRegular1(self):
        m = create_model()
        n = 10
        intvars = m.intvars(10, 0, 2)
        cost = m.intvar(3, 4)
        auto = create_cost_automaton()

        start = auto.add_state()
        end = auto.add_state()
        auto.set_initial_state(start)
        auto.set_final(start)
        auto.set_final(end)
        auto.add_transition(start, start, 0, 1)
        auto.add_transition(start, end, 2)
        auto.add_transition(end, start, 2)
        auto.add_transition(end, start, 0, 1)
        costs = []
        for i in range(0, n):
            costs.append([[0, 1], [0, 1], [0, 0]])
        auto.add_counter_state(costs, 3, 4)
        m.cost_regular(intvars, cost, auto).post()
        while m.get_solver().solve():
            pass
        self.assertEqual(m.get_solver().get_solution_count(), 9280)
