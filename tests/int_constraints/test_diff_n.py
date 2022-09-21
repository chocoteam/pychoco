import unittest

from pychoco.model import Model


class TestDiffN(unittest.TestCase):

    def testDiffN1(self):
        m = Model()
        x = m.intvars(2, 0, 2)
        y = m.intvars(2, 0, 2)
        width = m.intvars(2, 0, 2)
        height = m.intvars(2, 0, 2)
        diff_n = m.diff_n(x, y, width, height)
        diff_n.post()
        while m.get_solver().solve():
            self.assertTrue(diff_n.is_satisfied())
        self.assertTrue(m.get_solver().get_solution_count() > 0)
