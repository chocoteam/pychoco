import unittest

from pychoco.model import Model


class TestSetSum(unittest.TestCase):

    def test1(self):
        m = Model()
        intvar = m.intvar(0, 100)
        setvar = m.setvar([], range(0, 10))
        m.set_sum(setvar, intvar).post()
        while m.get_solver().solve():
            self.assertEqual(sum(setvar.get_value()), intvar.get_value())
