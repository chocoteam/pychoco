import unittest

from pychoco.model import Model


class TestSetAllDiff(unittest.TestCase):

    def test1(self):
        m = Model()
        a = m.setvar(set([]), set(range(0, 5)))
        b = m.setvar(set([]), set(range(0, 5)))
        c = m.setvar(set([]), set(range(0, 5)))
        m.set_all_different([a, b, c]).post()
        while m.get_solver().solve():
            aa = a.get_value()
            bb = b.get_value()
            cc = c.get_value()
            self.assertNotEqual(aa, bb)
            self.assertNotEqual(aa, cc)
            self.assertNotEqual(bb, cc)
