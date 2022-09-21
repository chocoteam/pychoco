import unittest

from pychoco.model import Model


class TestAtMostNValues(unittest.TestCase):

    def testAtMostNValues1(self):
        m = Model()
        variables = m.intvars(5, 0, 5)
        n_values = m.intvar(0, 2)
        m.at_most_n_values(variables, n_values).post()
        while m.get_solver().solve():
            vals = set([v.get_value() for v in variables])
            self.assertTrue(len(vals) <= n_values.get_value())

    def testAtMostNValuesFail(self):
        m = Model()
        variables = m.intvars(5, 0, 5)
        n_values = m.intvar(2)
        m.at_most_n_values(variables, n_values).post()
        m.all_different(variables).post()
        self.assertFalse(m.get_solver().solve())
