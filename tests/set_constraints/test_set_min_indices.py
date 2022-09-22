import unittest

from pychoco.model import Model


class TestMinIndices(unittest.TestCase):

    def test1(self):
        m = Model()
        intvar = m.intvar(0, 10)
        indices = m.setvar([], range(0, 11))
        weights = [2, 3, 1, 5, 6, 8, 9, 0, 11, 1, 21]
        m.set_min_indices(indices, weights, intvar, True).post()
        while m.get_solver().solve():
            self.assertEqual(intvar.get_value(), min([weights[i] for i in indices.get_value()]))
