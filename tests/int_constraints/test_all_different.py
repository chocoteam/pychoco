import unittest

from pychoco import create_model


class TestAllDifferent(unittest.TestCase):

    def testAllDifferent1(self):
        m = create_model()
        variables = m.intvars(3, 0, 2)
        m.all_different(*variables).post()
        solutions = m.get_solver().find_all_solutions()
        self.assertEqual(len(solutions), 6)
        for s in solutions:
            self.assertNotEqual(s.get_int_val(variables[0]), s.get_int_val(variables[1]))
            self.assertNotEqual(s.get_int_val(variables[0]), s.get_int_val(variables[2]))
            self.assertNotEqual(s.get_int_val(variables[1]), s.get_int_val(variables[2]))
