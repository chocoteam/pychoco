import unittest

from pychoco.model import Model


class TestMin(unittest.TestCase):

    def test1(self):
        m = Model()
        intvar = m.intvar(0, 10)
        setvar = m.setvar([], range(0, 11))
        m.set_min(setvar, intvar, True).post()
        while m.get_solver().solve():
            self.assertEqual(intvar.get_value(), min(setvar.get_value()))
