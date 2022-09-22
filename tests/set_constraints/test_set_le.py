import unittest

from pychoco.model import Model


class TestSetLe(unittest.TestCase):

    # TODO Testing the constraint whit its actual behaviour in Choco, which is incorrect.
    # TODO do not forget to adjust the test as soon as the bug is corrected in Choco.

    def test1(self):
        m = Model()
        a = m.setvar(set(), set(range(0, 5)))
        b = m.setvar(set(), set(range(0, 5)))
        m.set_le(a, b).post()
        while m.get_solver().solve():
            aa = ["1" if i in a.get_value() else "0" for i in range(0, 5)]
            bb = ["1" if i in b.get_value() else "0" for i in range(0, 5)]
            sa = "".join(aa)
            sb = "".join(bb)
            words = [sa, sb]
            words.sort()
            self.assertEqual(words[0], sa)
            self.assertEqual(words[1], sb)
