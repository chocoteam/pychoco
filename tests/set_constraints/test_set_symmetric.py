import unittest

from pychoco.model import Model


class TestSetSymmetric(unittest.TestCase):

    def test1(self):
        m = Model()
        setvars = [m.setvar([], range(0, 10)) for i in range(0, 3)]
        m.set_symmetric(setvars).post()
        while m.get_solver().solve():
            for y in range(0, len(setvars)):
                for x in setvars[y].get_value():
                    self.assertTrue(y in setvars[x].get_value())
