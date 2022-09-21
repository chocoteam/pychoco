import unittest

from pychoco.model import Model


class TestNotAllEqual(unittest.TestCase):

    def testNotAllEqual1(self):
        m = Model()
        variables = m.intvars(3, 0, 2)
        m.not_all_equal(variables).post()
        while m.get_solver().solve():
            vals = set([v.get_value() for v in variables])
            self.assertTrue(len(vals) > 1)

    def testNotAllEqualFail(self):
        m = Model()
        variables = [m.intvar(1, 1), m.intvar(1, 1), m.intvar(1)]
        m.not_all_equal(variables).post()
        solution = m.get_solver().find_solution()
        self.assertIsNone(solution)
