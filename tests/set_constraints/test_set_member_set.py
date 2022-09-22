import unittest

from pychoco.model import Model


class TestSetMemberSet(unittest.TestCase):

    def test1(self):
        m = Model()
        a = m.setvar([1, 2, 3])
        b = m.setvar([2, 3, 4])
        c = m.setvar([3, 4, 5])
        d = m.setvar([6, 7, 8])
        setvars = [a, b, c, d]
        setvar = m.setvar([], range(0, 1000))
        m.set_member_set(setvars, setvar).post()
        while m.get_solver().solve():
            self.assertTrue(setvar.get_value() in [s.get_value() for s in setvars])
