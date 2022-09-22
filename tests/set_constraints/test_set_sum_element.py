import unittest

from pychoco.model import Model


class TestSetSum(unittest.TestCase):

    def test1(self):
        m = Model()
        intvar = m.intvar(0, 100)
        setvar = m.setvar([], range(0, 10))
        weights = [1, 10, 15, 20, 2, 1, 4, 8, 65, 0]
        m.set_sum_element(setvar, weights, intvar).post()
        while m.get_solver().solve():
            self.assertEqual(sum([weights[i] for i in setvar.get_value()]), intvar.get_value())
