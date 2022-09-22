import unittest

from pychoco.model import Model


class TestSetOffset(unittest.TestCase):

    def test1(self):
        m = Model()
        s1 = m.setvar([], range(0, 10))
        s2 = m.setvar([], range(0, 10))
        m.set_offset(s1, s2, 2).post()
        while m.get_solver().solve():
            value = [v - 2 for v in s2.get_value()]
            self.assertSetEqual(s1.get_value(), set(value))
