import unittest

from pychoco.model import Model


class TestAllEqual(unittest.TestCase):

    def testAllEqual1(self):
        m = Model()
        variables = m.intvars(3, 0, 2)
        m.all_equal(variables).post()
        solutions = m.get_solver().find_all_solutions()
        self.assertEqual(len(solutions), 3)
        for s in solutions:
            self.assertEqual(s.get_int_val(variables[0]), s.get_int_val(variables[1]))
            self.assertEqual(s.get_int_val(variables[0]), s.get_int_val(variables[2]))
            self.assertEqual(s.get_int_val(variables[1]), s.get_int_val(variables[2]))

    def testAllEqualFail(self):
        m = Model()
        variables = [m.intvar(0, 1), m.intvar(1, 2), m.intvar(3, 4)]
        m.all_equal(variables).post()
        solution = m.get_solver().find_solution()
        self.assertIsNone(solution)
