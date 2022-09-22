import unittest

from pychoco.model import Model


class TestSetNbEmpty(unittest.TestCase):

    def test1(self):
        m = Model()
        setvar = m.setvar([], range(0, 10))
        m.set_not_empty(setvar).post()
        while m.get_solver().solve():
            self.assertTrue(len(setvar.get_value()) > 0)
