import unittest

from pychoco.model import Model


class TestSetDisjoint(unittest.TestCase):

    def test1(self):
        m = Model()
        a = m.setvar(set([]), set(range(0, 5)))
        b = m.setvar(set([]), set(range(0, 5)))
        m.set_disjoint(a, b).post()
        while m.get_solver().solve():
            aa = a.get_value()
            bb = b.get_value()
            self.assertTrue(aa.isdisjoint(bb))
