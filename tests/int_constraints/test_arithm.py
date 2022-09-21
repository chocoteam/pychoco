import unittest

from pychoco.model import Model


class TestArithm(unittest.TestCase):

    def testArithm1(self):
        m = Model()
        a = m.intvar(0, 10)
        b = m.intvar(0, 10)
        c = m.intvar(10)
        m.arithm(a, "+", b, '=', c).post()
        solutions = m.get_solver().find_all_solutions()
        for s in solutions:
            self.assertEqual(s.get_int_val(a) + s.get_int_val(b), 10)

    def testArithm2(self):
        m = Model()
        a = m.intvar(0, 10)
        b = m.intvar(0, 10)
        m.arithm(a, "+", b, '=', 10).post()
        solutions = m.get_solver().find_all_solutions()
        for s in solutions:
            self.assertEqual(s.get_int_val(a) + s.get_int_val(b), 10)

    def testArithm3(self):
        m = Model()
        a = m.intvar(0, 10)
        m.arithm(a, "+", 5, '=', 10).post()
        solutions = m.get_solver().find_all_solutions()
        for s in solutions:
            self.assertEqual(s.get_int_val(a) + 5, 10)

    def testArithm4(self):
        m = Model()
        a = m.intvar(0, 10)
        b = m.intvar(0, 10)
        c = m.intvar(0, 10)
        m.arithm(a, "+", b, '=', c).post()
        solutions = m.get_solver().find_all_solutions()
        for s in solutions:
            self.assertEqual(s.get_int_val(a) + s.get_int_val(b), s.get_int_val(c))

    def testArithm5(self):
        m = Model()
        a = m.intvar(0, 10)
        b = m.intvar(0, 10)
        m.arithm(a, "=", b).post()
        solutions = m.get_solver().find_all_solutions()
        for s in solutions:
            self.assertEqual(s.get_int_val(a), s.get_int_val(b))

    def testArithm6(self):
        m = Model()
        a = m.intvar(0, 10)
        m.arithm(a, "=", 3).post()
        solutions = m.get_solver().find_all_solutions()
        for s in solutions:
            self.assertEqual(s.get_int_val(a), 3)

    def testArithm7(self):
        m = Model()
        a = m.intvar(0, 10)
        m.arithm(a, ">", 3).post()
        solutions = m.get_solver().find_all_solutions()
        for s in solutions:
            self.assertTrue(s.get_int_val(a) > 3)

    def testArithm7(self):
        m = Model()
        a = m.intvar(0, 10)
        m.arithm(a, "<", 3).post()
        solutions = m.get_solver().find_all_solutions()
        for s in solutions:
            self.assertTrue(s.get_int_val(a) < 3)

    def testArithm8(self):
        m = Model()
        a = m.intvar(0, 10)
        m.arithm(a, "<=", 3).post()
        solutions = m.get_solver().find_all_solutions()
        for s in solutions:
            self.assertTrue(s.get_int_val(a) <= 3)

    def testArithm9(self):
        m = Model()
        a = m.intvar(0, 10)
        m.arithm(a, ">=", 3).post()
        solutions = m.get_solver().find_all_solutions()
        for s in solutions:
            self.assertTrue(s.get_int_val(a) >= 3)

    def testArithm10(self):
        m = Model()
        a = m.intvar(0, 10)
        m.arithm(a, "!=", 3).post()
        solutions = m.get_solver().find_all_solutions()
        for s in solutions:
            self.assertTrue(s.get_int_val(a) != 3)

    def testArithm11(self):
        m = Model()
        a = m.intvar(0, 10)
        b = m.intvar(0, 10)
        c = m.intvar(0, 10)
        m.arithm(a, "=", b, '-', c).post()
        solutions = m.get_solver().find_all_solutions()
        for s in solutions:
            self.assertEqual(s.get_int_val(a), s.get_int_val(b) - s.get_int_val(c))

    def testArithmError(self):
        m = Model()
        a = m.intvar(0, 10)
        self.assertRaises(AssertionError, m.arithm, *[a, "=", 3, "=", 10])
        self.assertRaises(AssertionError, m.arithm, *[a, "xx", 3, "=", 10])
        self.assertRaises(AssertionError, m.arithm, *[a, "+", 3, "-", 10])
        self.assertRaises(AssertionError, m.arithm, *[a, "+", 3, "pp", 10])
