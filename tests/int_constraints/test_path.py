import unittest

from pychoco.model import Model


class TestPath(unittest.TestCase):

    def testPath1(self):
        model = Model()
        x = model.intvars(10, 0, 20)
        model.path(x, model.intvar(0), model.intvar(1)).post()
        model.get_solver().solve()
        self.assertEqual(1, model.get_solver().get_solution_count())

    def testPathFail(self):
        model = Model()
        x = model.intvars(10, 0, 9)
        model.path(x, model.intvar(0), model.intvar(1)).post()
        self.assertFalse(model.get_solver().solve())
