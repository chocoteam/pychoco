import unittest

from pychoco.model import Model


class TestTree(unittest.TestCase):

    def testTree1(self):
        model = Model()
        vs = model.intvars(6, -1, 6)
        nt = model.intvar(2, 3)
        tree = model.tree(vs, nt)
        tree.post()
        model.get_solver().set_random_search(*vs)
        while model.get_solver().solve():
            self.assertTrue(tree.is_satisfied())
        self.assertTrue(model.get_solver().get_solution_count() > 0)
