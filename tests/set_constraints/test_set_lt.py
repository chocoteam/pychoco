import unittest

from pychoco.model import Model


class TestSetLt(unittest.TestCase):

    def test1(self):
        m = Model()
        a = m.setvar(set(), set(range(0, 5)))
        b = m.setvar(set(), set(range(0, 5)))
        m.set_lt(a, b).post()
        while m.get_solver().solve():
            aa = [str(i) if i in a.get_value() else "" for i in range(0, 5)]
            bb = [str(i) if i in b.get_value() else "" for i in range(0, 5)]
            sa = "".join(aa)
            sb = "".join(bb)
            words = [sa, sb]
            words.sort()
            self.assertEqual(words[0], sa)
            self.assertEqual(words[1], sb)
            self.assertNotEqual(sa, sb)
