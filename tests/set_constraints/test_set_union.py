import unittest

from pychoco.model import Model


class TestSetUnion(unittest.TestCase):

    def test1(self):
        m = Model()
        a = m.setvar(set([]), set(range(0, 5)))
        b = m.setvar(set([]), set(range(5, 10)))
        c = m.setvar(set([]), set(range(10, 15)))
        d = m.setvar(set([]), set(range(0, 15)))
        m.set_union([a, b, c], d).post()
        while m.get_solver().solve():
            aa = a.get_value()
            bb = b.get_value()
            cc = c.get_value()
            dd = d.get_value()
            self.assertSetEqual(aa.union(bb).union(cc), dd)
