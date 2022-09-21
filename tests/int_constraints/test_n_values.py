import unittest

from pychoco.model import Model


class TestNValues(unittest.TestCase):

    def testNValues1(self):
        m = Model()
        variables = m.intvars(5, 0, 5)
        n_values = m.intvar(0, 2)
        m.n_values(variables, n_values).post()
        while m.get_solver().solve():
            vals = set([v.get_value() for v in variables])
            self.assertTrue(len(vals) == n_values.get_value())

    def testNValuesFail(self):
        m = Model()
        variables = m.intvars(5, 0, 5)
        n_values = m.intvar(2)
        m.n_values(variables, n_values).post()
        m.all_equal(variables).post()
        self.assertFalse(m.get_solver().solve())
