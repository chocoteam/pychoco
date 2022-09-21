import unittest

from pychoco.model import Model


class TestAllDifferent(unittest.TestCase):

    def testAllDifferent1(self):
        m = Model()
        variables = m.intvars(3, 0, 2)
        m.all_different(variables).post()
        solutions = m.get_solver().find_all_solutions()
        self.assertEqual(len(solutions), 6)
        for s in solutions:
            self.assertNotEqual(s.get_int_val(variables[0]), s.get_int_val(variables[1]))
            self.assertNotEqual(s.get_int_val(variables[0]), s.get_int_val(variables[2]))
            self.assertNotEqual(s.get_int_val(variables[1]), s.get_int_val(variables[2]))

    def testAllDifferentFail(self):
        m = Model()
        variables = m.intvars(3, 0, 1)
        m.all_different(variables).post()
        solution = m.get_solver().find_solution()
        self.assertIsNone(solution)
