import unittest

from pychoco.model import Model


class TestSetBoolsChanneling(unittest.TestCase):

    def test1(self):
        m = Model()
        a = m.setvar(set([]), set(range(0, 5)))
        b = m.boolvars(5)
        m.set_bools_channeling(b, a).post()
        while m.get_solver().solve():
            for i in a.get_value():
                self.assertTrue(b[i].get_value())
