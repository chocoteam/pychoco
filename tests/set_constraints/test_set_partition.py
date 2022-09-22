import unittest

from pychoco.model import Model


class TestSetPartition(unittest.TestCase):

    def test1(self):
        m = Model()
        universe = m.setvar([], range(0, 10))
        a = m.setvar([], [1, 2, 3, 4])
        b = m.setvar([], [0, 1, 2, 5, 6, 7, 8])
        c = m.setvar([], [5, 6, 7, 8, 9])
        m.set_partition([a, b, c], universe).post()
        while m.get_solver().solve():
            aa = a.get_value()
            bb = b.get_value()
            cc = c.get_value()
            self.assertTrue(aa.isdisjoint(bb))
            self.assertTrue(aa.isdisjoint(cc))
            self.assertTrue(bb.isdisjoint(cc))
            union = aa.union(bb).union(cc)
            self.assertSetEqual(union, universe.get_value())
