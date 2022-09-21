import unittest

from pychoco.model import Model


class TestInverseChanneling(unittest.TestCase):

    def testInverseChanneling1(self):
        m = Model()
        iv1 = m.intvars(5, 0, 5)
        iv2 = m.intvars(5, 0, 5)
        m.inverse_channeling(iv1, iv2).post()
        while m.get_solver().solve():
            for i in range(0, 5):
                self.assertEqual(iv2[iv1[i].get_value()].get_value(), i)

    def testInverseChannelingFail(self):
        m = Model()
        iv1 = m.intvars(5, 0, 5)
        iv2 = m.intvars(5, 1, 6)
        m.inverse_channeling(iv1, iv2).post()
        self.assertFalse(m.get_solver().solve())
