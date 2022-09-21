import unittest

from pychoco import create_model


class TestNotAllEqual(unittest.TestCase):

    def testNotAllEqual1(self):
        m = create_model()
        variables = m.intvars(3, 0, 2)
        m.not_all_equal(variables).post()
        while m.get_solver().solve():
            vals = set([v.get_value() for v in variables])
            self.assertTrue(len(vals) > 1)

    def testNotAllEqualFail(self):
        m = create_model()
        variables = [m.intvar(1, 1), m.intvar(1, 1), m.intvar(1)]
        m.not_all_equal(variables).post()
        solution = m.get_solver().find_solution()
        self.assertIsNone(solution)
