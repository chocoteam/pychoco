import unittest

from pychoco.model import Model


class TestOr(unittest.TestCase):

    def testOr1(self):
        m = Model()
        variables = m.intvars(3, 0, 4)
        c1 = m.arithm(variables[0], ">", variables[1])
        c2 = m.arithm(variables[1], ">", variables[2])
        m.or_([c1, c2]).post()
        while m.get_solver().solve():
            self.assertTrue(c1.is_satisfied() or c2.is_satisfied())

    def testOr2(self):
        m = Model()
        variables = m.boolvars(3)
        m.or_(variables).post()
        while m.get_solver().solve():
            self.assertTrue(sum([1 for v in variables if v.get_value() == 1]) > 0)

    def testOrFail1(self):
        m = Model()
        variables = m.boolvars(3)
        m.or_(variables).post()
        m.sum(variables, "=", 0).post()
        self.assertFalse(m.get_solver().solve())

    def testOrFail2(self):
        m = Model()
        variables = m.intvars(3, 0, 1)
        all_diff = m.all_different(variables)
        sum_ = m.sum(variables, ">", 10)
        m.or_([all_diff, sum_]).post()
        self.assertFalse(m.get_solver().solve())
