import unittest

from pychoco.model import Model


class TestAnd(unittest.TestCase):

    def testAnd1(self):
        m = Model()
        variables = m.intvars(3, 0, 4)
        all_diff = m.all_different(variables)
        sum_ = m.sum(variables, "<=", 3)
        m.and_([all_diff, sum_]).post()
        while m.get_solver().solve():
            self.assertNotEqual(variables[0].get_value(), variables[1].get_value())
            self.assertNotEqual(variables[0].get_value(), variables[2].get_value())
            self.assertNotEqual(variables[1].get_value(), variables[2].get_value())
            self.assertTrue(all_diff.is_satisfied())
            self.assertTrue(sum_.is_satisfied())
        self.assertEqual(m.get_solver().get_solution_count(), 6)

    def testAnd2(self):
        m = Model()
        variables = m.boolvars(3)
        m.and_(variables).post()
        sols = m.get_solver().find_all_solutions()
        self.assertEqual(len(sols), 1)
        for v in variables:
            self.assertEqual(sols[0].get_int_val(v), 1)

    def testAndFail1(self):
        m = Model()
        variables = m.boolvars(3)
        m.and_(variables).post()
        m.sum(variables, "<", 3).post()
        self.assertFalse(m.get_solver().solve())

    def testAndFail2(self):
        m = Model()
        variables = m.intvars(3, 0, 3)
        all_diff = m.all_different(variables)
        sum_ = m.sum(variables, "<=", 2)
        m.and_([all_diff, sum_]).post()
        self.assertFalse(m.get_solver().solve())
