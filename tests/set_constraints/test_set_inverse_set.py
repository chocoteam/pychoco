import unittest

from pychoco.model import Model


class TestSetInverseSet(unittest.TestCase):

    def test1(self):
        m = Model()
        setvars = [m.setvar(set([]), set(range(0, 4))) for i in range(0, 3)]
        inv_setvars = [m.setvar(set([]), set(range(0, 4))) for i in range(0, 3)]
        m.set_inverse_set(setvars, inv_setvars).post()
        while m.get_solver().solve():
            for y in range(0, len(setvars)):
                for x in setvars[y].get_value():
                    self.assertTrue(y in inv_setvars[x].get_value())
