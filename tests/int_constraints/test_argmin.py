import unittest

from pychoco.model import Model


class TestArgmin(unittest.TestCase):

    def testArgmin1(self):
        m = Model()
        variables = m.intvars(5, 0, 10)
        m.all_different(variables).post()
        idx = m.intvar(1, 5)
        m.argmin(idx, 1, variables).post()
        while m.get_solver().solve():
            vals = [v.get_value() for v in variables]
            self.assertEqual(variables[idx.get_value() - 1].get_value(), min(vals))

    def testArgminFail(self):
        m = Model()
        variables = [m.intvar(0, 1), m.intvar(2, 4), m.intvar(2, 3)]
        idx = m.intvar(1, 8)
        m.argmin(idx, 0, variables).post()
        self.assertFalse(m.get_solver().solve())
