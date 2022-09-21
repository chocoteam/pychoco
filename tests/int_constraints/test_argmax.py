import unittest

from pychoco.model import Model


class TestArgmax(unittest.TestCase):

    def testArgmax1(self):
        m = Model()
        variables = m.intvars(5, 0, 10)
        m.all_different(variables).post()
        idx = m.intvar(1, 5)
        m.argmax(idx, 1, variables).post()
        while m.get_solver().solve():
            vals = [v.get_value() for v in variables]
            self.assertEqual(variables[idx.get_value() - 1].get_value(), max(vals))

    def testArgmaxFail(self):
        m = Model()
        variables = [m.intvar(10, 11), m.intvar(0, 1), m.intvar(2, 3)]
        idx = m.intvar(1, 8)
        m.argmax(idx, 0, variables).post()
        self.assertFalse(m.get_solver().solve())
