import unittest

from pychoco.model import Model


class TestMax(unittest.TestCase):

    def test1(self):
        m = Model()
        intvar = m.intvar(0, 10)
        setvar = m.setvar([], range(0, 11))
        m.set_max(setvar, intvar, True).post()
        while m.get_solver().solve():
            self.assertEqual(intvar.get_value(), max(setvar.get_value()))
