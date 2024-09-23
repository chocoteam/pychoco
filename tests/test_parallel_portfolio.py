import math
import unittest

from pychoco.model import Model
from pychoco.parallel_portfolio import ParallelPortfolio


class TestParallelPortfolio(unittest.TestCase):

    def test_simple_solve(self):
        pf = ParallelPortfolio()
        for i in range(0, 5):
            m = Model()
            vars = m.intvars(10, 0, 20)
            nv = m.intvar(3, 6)
            m.n_values(vars, nv).post()
            s = m.intvar(0, 100)
            m.sum(vars, "=", s).post()
            pf.add_model(m)
        self.assertTrue(pf.solve())

    def test_optimize(self):
        pf = ParallelPortfolio()
        pf.steal_nogoods_on_restarts()
        for i in range(0, 5):
            m = Model()
            vars = m.intvars(10, 0, 100)
            nv = m.intvar(3, 4)
            m.n_values(vars, nv).post()
            s = m.intvar(0, 1000)
            m.sum(vars, "=", s).post()
            m.set_objective(s, True)
            pf.add_model(m)
        sol = pf.find_best_solution()
        best_val = sol.get_int_val(s)
        self.assertEqual(best_val, 997)

