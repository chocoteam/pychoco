import unittest

from pychoco.model import Model


class TestSetAllDisjoint(unittest.TestCase):

    def test1(self):
        m = Model()
        a = m.setvar(set([]), set(range(0, 5)))
        b = m.setvar(set([]), set(range(0, 5)))
        c = m.setvar(set([]), set(range(0, 5)))
        m.set_all_disjoint([a, b, c]).post()
        while m.get_solver().solve():
            aa = a.get_value()
            bb = b.get_value()
            cc = c.get_value()
            self.assertTrue(aa.isdisjoint(bb))
            self.assertTrue(aa.isdisjoint(cc))
            self.assertTrue(bb.isdisjoint(cc))
