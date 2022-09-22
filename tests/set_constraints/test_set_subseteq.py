import unittest

from pychoco.model import Model


class TestSetSubsetEq(unittest.TestCase):

    def test1(self):
        m = Model()
        setvars = [m.setvar([], range(0, 5)) for i in range(0, 4)]
        m.set_subset_eq(setvars).post()
        while m.get_solver().solve():
            for i in range(0, 3):
                self.assertTrue(setvars[i].get_value().issubset(setvars[i + 1].get_value()))
