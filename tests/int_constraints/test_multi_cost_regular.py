import unittest

from pychoco.model import Model
from pychoco.objects.automaton.cost_automaton import make_multi_resources
from pychoco.objects.automaton.finite_automaton import FiniteAutomaton


def make(period, seed):
    model = Model()
    sequence = model.intvars(period, 0, 2)
    bounds = [model.intvar(0, 80), model.intvar(0, 28), model.intvar(0, 28), model.intvar(0, 28)]
    auto = FiniteAutomaton()
    idx = auto.add_state()
    auto.set_initial_state(idx)
    auto.set_final(idx)
    idx = auto.add_state()
    day = 0
    auto.add_transition(auto.initial_state, idx, day)
    next_ = auto.add_state()
    night = 1
    auto.add_transition(idx, next_, day, night)
    rest = 2
    auto.add_transition(next_, auto.initial_state, rest)
    auto.add_transition(auto.initial_state, next_, night)
    cost_matrix = []
    for i in range(0, period):
        a = []
        for j in range(0, 3):
            b = []
            for k in range(0, 4):
                if k == 0:
                    if j == day:
                        b.append([3, 5, 0])
                    elif j == night:
                        b.append([8, 9, 0])
                    else:
                        b.append([0, 0, 2])
                elif k == 1:
                    if j == day:
                        b.append([1, 1, 0])
                    else:
                        b.append([0, 0, 0])
                elif k == 2:
                    if j == night:
                        b.append([1, 1, 0])
                    else:
                        b.append([0, 0, 0])
                else:
                    if j == rest:
                        b.append([1, 1, 0])
                    else:
                        b.append([0, 0, 0])
            a.append(b)
        cost_matrix.append(a)
    cost_automaton = make_multi_resources(auto, cost_matrix, bounds)
    model.multi_cost_regular(sequence, bounds, cost_automaton).post()
    model.get_solver().set_random_search(*(sequence + bounds), seed=seed)
    return model


class TestMultiCostRegular(unittest.TestCase):

    def testMultiCostRegular1(self):
        seed = 0
        for i in range(0, 200):
            model = make(5, i + seed)
            while model.get_solver().solve():
                pass
            self.assertEqual(model.get_solver().get_solution_count(), 4)

    def testMultiCostRegular2(self):
        seed = 0
        for i in range(0, 200):
            model = make(7, i + seed)
            while model.get_solver().solve():
                pass
            self.assertEqual(model.get_solver().get_solution_count(), 6)

    def testMultiCostRegular3(self):
        seed = 0
        for i in range(0, 20):
            model = make(21, i + seed)
            while model.get_solver().solve():
                pass
            self.assertEqual(model.get_solver().get_solution_count(), 85)
