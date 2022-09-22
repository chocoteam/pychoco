import unittest

from pychoco.model import Model


class TestSetNbEmpty(unittest.TestCase):

    def test1(self):
        m = Model()
        setvars = [m.setvar([], range(0, 3)) for i in range(0, 4)]
        intvar = m.intvar(0, 3)
        m.set_nb_empty(setvars, intvar).post()
        while m.get_solver().solve():
            nb_empty = sum([1 if len(s.get_value()) == 0 else 0 for s in setvars])
            self.assertEqual(nb_empty, intvar.get_value())
