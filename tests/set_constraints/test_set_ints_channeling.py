import unittest

from pychoco.model import Model


class TestSetIntsChanneling(unittest.TestCase):

    def test1(self):
        m = Model()
        a = m.setvar(set([]), set(range(0, 5)))
        b = m.setvar(set([]), set(range(5, 10)))
        c = m.setvar(set([]), set(range(0, 10)))
        setvars = [a, b, c]
        intvars = m.intvars(10, 0, 2)
        m.set_ints_channeling(setvars, intvars).post()
        while m.get_solver().solve():
            for i in range(0, 10):
                v = intvars[i].get_value()
                self.assertTrue(i in setvars[v].get_value())
