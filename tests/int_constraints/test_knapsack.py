import unittest

from pychoco.model import Model


class TestKnapsack(unittest.TestCase):

    def testKnapsack1(self):
        for seed in range(0, 200):
            m = Model()
            occs = m.boolvars(35)
            es = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 8, 8, 8, 8, 4, 4, 4, 4,
                  4, 7, 7, 7, 3, 3, 3, 3, 3, 3, 3, 3]
            ws = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 3, 3, 3, 3,
                  3, 5, 5, 5, 2, 2, 2, 2, 2, 2, 2, 2]
            capa = m.intvar(0, 15)
            power = m.intvar(0, 999);
            m.knapsack(occs, capa, power, ws, es).post()
            m.get_solver().set_random_search(*occs, seed=seed)
            s = m.get_solver().find_optimal_solution(power, True)
            self.assertEqual(s.get_int_val(power), 28)
